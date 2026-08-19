#!/usr/bin/env python3
"""
ScoutEdge REST API Client Demonstration
"""

import sys
import os
import json
import time
import threading
from urllib.request import urlopen, Request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.api.server import create_scoutedge_app


def run_demo_client():
    server = create_scoutedge_app(host="127.0.0.1", port=0)
    port = server.server_address[1]
    base_url = f"http://127.0.0.1:{port}"

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(0.5)

    print("=" * 60)
    print("      SCOUTEDGE REST API CLIENT DEMO")
    print("=" * 60)

    # 1. Healthcheck Request
    print("\n[1] GET /api/v1/health")
    with urlopen(f"{base_url}/api/v1/health") as resp:
        health_data = json.loads(resp.read().decode("utf-8"))
        print(f"Status Code: {resp.status}")
        print(json.dumps(health_data, indent=2))

    # 2. Evaluate Athlete POST Payload
    print("\n[2] POST /api/v1/evaluate")
    payload = {
        "athlete": {
            "athlete_id": "ath_rest_88",
            "name": "Dominic Solanke",
            "sport": "Soccer",
            "primary_position": "Striker",
            "birth_date": "2002-09-14",
            "height_cm": 187.0,
            "weight_kg": 80.0,
            "current_team": "Premier Division FC",
        },
        "performance_signals": [
            {
                "signal_id": "p_01",
                "minutes_played": 90,
                "raw_stats": {"goals": 90.0, "shots_on_target": 88.0, "conversion_rate": 84.0},
                "opponent_tier_weight": 1.2,
            }
        ],
        "scout_signals": [
            {
                "signal_id": "s_01",
                "technical_score": 89.0,
                "tactical_score": 86.0,
                "physical_score": 92.0,
                "mental_score": 88.0,
                "qualitative_notes": "Dominant target man with clinical finishing ability.",
            }
        ],
        "readiness_signals": [
            {
                "signal_id": "r_01",
                "acute_workload_7d": 350.0,
                "chronic_workload_28d": 1400.0,
                "sleep_quality_score": 90.0,
                "fatigue_level": 12.0,
                "availability_status": "Available",
            }
        ],
        "age_years": 23.8,
    }

    req = Request(
        f"{base_url}/api/v1/evaluate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(req) as resp:
        eval_output = json.loads(resp.read().decode("utf-8"))
        print(f"Status Code: {resp.status}")
        print(f"• Athlete ID:      {eval_output['athlete_id']}")
        print(f"• SE-R™ Rating:    {eval_output['se_r']['overall_rating']} (Percentile: {eval_output['se_r']['percentile_rank']}%)")
        print(f"• PGI™ Growth:     {eval_output['pgi']['pgi_score']} ({eval_output['pgi']['development_stage']})")
        print(f"• EdgeCare™ ACWR:  {eval_output['edgecare']['acwr_ratio']} (Risk: {eval_output['edgecare']['injury_risk_category']})")
        print(f"• Fit Score:       {eval_output['fit_score']}")
        print(f"• Recommendation:  {eval_output['recommendation'].upper()}")
        print(f"• Reasons:         {', '.join(eval_output['explainability_reasons'])}")

    print("\n=" * 60)
    print("      SCOUTEDGE REST API DEMO COMPLETED")
    print("=" * 60)

    server.shutdown()
    server.server_close()


if __name__ == "__main__":
    run_demo_client()
