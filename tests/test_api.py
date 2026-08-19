"""
Unit Tests for ScoutEdge REST API Gateway
"""

import sys
import os
import json
import unittest
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.api.server import create_scoutedge_app


class TestScoutEdgeAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_scoutedge_app(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        url = f"{self.base_url}/api/v1/health"
        with urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "healthy")
            self.assertIn("ScoutEdge REST API", data["service"])

    def test_evaluate_endpoint(self):
        url = f"{self.base_url}/api/v1/evaluate"
        payload = {
            "athlete": {
                "athlete_id": "ath_api_1",
                "name": "Marcus Rashford",
                "primary_position": "Forward",
            },
            "performance_signals": [
                {
                    "signal_id": "p1",
                    "minutes_played": 90,
                    "raw_stats": {"goals": 80.0, "shots_on_target": 85.0},
                    "opponent_tier_weight": 1.1,
                }
            ],
            "scout_signals": [
                {
                    "signal_id": "s1",
                    "technical_score": 88.0,
                    "tactical_score": 82.0,
                    "physical_score": 90.0,
                    "mental_score": 85.0,
                }
            ],
            "readiness_signals": [
                {
                    "signal_id": "r1",
                    "acute_workload_7d": 300.0,
                    "chronic_workload_28d": 1200.0,
                    "sleep_quality_score": 85.0,
                    "fatigue_level": 15.0,
                }
            ],
        }

        req = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["athlete_id"], "ath_api_1")
            self.assertGreater(data["fit_score"], 70.0)
            self.assertIn("se_r", data)
            self.assertIn("edgecare", data)
            self.assertIn("pgi", data)

    def test_ser_rating_endpoint(self):
        url = f"{self.base_url}/api/v1/rating/ser"
        payload = {
            "position": "Winger",
            "performance_signals": [
                {"signal_id": "p1", "raw_stats": {"pace": 90.0, "crosses": 80.0}}
            ],
        }
        req = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("overall_rating", data)
            self.assertIn("percentile_rank", data)


if __name__ == "__main__":
    unittest.main()
