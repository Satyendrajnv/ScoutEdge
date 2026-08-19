"""
Lightweight REST API Gateway Server for ScoutEdge Intelligence
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Tuple, Dict, Any

from scoutedge import __version__
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.api.schemas import (
    serialize_evaluation_result,
    parse_athlete_profile,
    parse_performance_signals,
    parse_scout_signals,
    parse_readiness_signals,
)


class ScoutEdgeHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler implementing ScoutEdge REST API endpoints.
    """

    pipeline = ScoutEdgePipeline()

    def _send_json_response(self, status_code: int, payload: Dict[str, Any]):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ["/api/v1/health", "/health", "/"]:
            self._send_json_response(
                200,
                {
                    "status": "healthy",
                    "service": "ScoutEdge REST API Gateway",
                    "version": __version__,
                    "endpoints": [
                        "GET /api/v1/health",
                        "POST /api/v1/evaluate",
                        "POST /api/v1/rating/ser",
                        "POST /api/v1/readiness/edgecare",
                    ],
                },
            )
        else:
            self._send_json_response(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            body = json.loads(post_data.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json_response(400, {"error": "Invalid JSON body payload"})
            return

        if path == "/api/v1/evaluate":
            profile = parse_athlete_profile(body.get("athlete", {}))
            perf_signals = parse_performance_signals(body.get("performance_signals", []))
            scout_signals = parse_scout_signals(body.get("scout_signals", []))
            readiness_signals = parse_readiness_signals(body.get("readiness_signals", []))
            age_years = float(body.get("age_years", 21.0))

            result = self.pipeline.process_athlete(
                profile, perf_signals, scout_signals, readiness_signals, age_years
            )
            self._send_json_response(200, serialize_evaluation_result(result))

        elif path == "/api/v1/rating/ser":
            perf_signals = parse_performance_signals(body.get("performance_signals", []))
            scout_signals = parse_scout_signals(body.get("scout_signals", []))
            position = body.get("position", "General")

            ser_output = self.pipeline.ser_engine.calculate_rating(
                perf_signals, scout_signals, position
            )
            self._send_json_response(
                200,
                {
                    "overall_rating": ser_output.overall_rating,
                    "technical_rating": ser_output.technical_rating,
                    "physical_rating": ser_output.physical_rating,
                    "tactical_rating": ser_output.tactical_rating,
                    "confidence_score": ser_output.confidence_score,
                    "percentile_rank": ser_output.percentile_rank,
                    "key_drivers": ser_output.key_drivers,
                },
            )

        elif path == "/api/v1/readiness/edgecare":
            readiness_signals = parse_readiness_signals(body.get("readiness_signals", []))
            edgecare_output = self.pipeline.edgecare_engine.calculate_readiness(
                readiness_signals
            )
            self._send_json_response(
                200,
                {
                    "readiness_index": edgecare_output.readiness_index,
                    "acwr_ratio": edgecare_output.acwr_ratio,
                    "injury_risk_category": edgecare_output.injury_risk_category,
                    "recommended_minutes": edgecare_output.recommended_minutes,
                    "sustainability_score": edgecare_output.sustainability_score,
                },
            )

        else:
            self._send_json_response(404, {"error": "Endpoint not found", "path": path})


class ScoutEdgeHTTPServer(HTTPServer):
    allow_reuse_address = True


def create_scoutedge_app(host: str = "0.0.0.0", port: int = 8000) -> HTTPServer:
    """Factory helper creating configured ScoutEdge HTTP server."""
    server_address = (host, port)
    return ScoutEdgeHTTPServer(server_address, ScoutEdgeHTTPRequestHandler)


if __name__ == "__main__":
    print("Starting ScoutEdge REST API Gateway on http://0.0.0.0:8000...")
    httpd = create_scoutedge_app(port=8000)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down ScoutEdge API server.")
        httpd.server_close()
