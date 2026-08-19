#!/usr/bin/env python3
"""
ScoutEdge Executive Report Generation Demo
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.reports.exporter import ScoutReportExporter


def main():
    print("=" * 60)
    print("       SCOUTEDGE REPORT EXPORTER DEMO")
    print("=" * 60)

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Define Athlete Profile
    athlete = AthleteProfile(
        athlete_id="ath_demo_77",
        name="Kylian Mbappe-Vance",
        sport="Football",
        primary_position="Left Winger",
        birth_date="2003-12-20",
        height_cm=178.0,
        weight_kg=73.0,
        current_team="Capital City Elite",
        league_tier="Division 1 Professional",
    )

    perf_signals = [
        PerformanceSignal(
            signal_id="p1",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-10",
            match_id="m100",
            minutes_played=90,
            raw_stats={"dribbles": 94.0, "shots_on_target": 90.0, "sprints": 96.0},
            opponent_tier_weight=1.2,
        )
    ]

    scout_signals = [
        ScoutSignal(
            signal_id="s1",
            athlete_id=athlete.athlete_id,
            scout_id="lead_scout_1",
            timestamp="2026-08-10",
            technical_score=94.0,
            tactical_score=88.0,
            physical_score=96.0,
            mental_score=90.0,
            qualitative_notes="World-class acceleration and finishing in 1v1 situations.",
        )
    ]

    readiness_signals = [
        ReadinessSignal(
            signal_id="r1",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-18",
            acute_workload_7d=360.0,
            chronic_workload_28d=1440.0,  # ACWR = 1.0
            sleep_quality_score=92.0,
            fatigue_level=10.0,
            availability_status="Available",
        )
    ]

    # 2. Run Intelligence Pipeline
    pipeline = ScoutEdgePipeline()
    result = pipeline.process_athlete(
        athlete, perf_signals, scout_signals, readiness_signals, age_years=22.6
    )

    # 3. Export Reports
    exporter = ScoutReportExporter()

    # Markdown
    md_content = exporter.export_markdown(athlete, result)
    md_path = os.path.join(output_dir, "scouting_dossier.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"[✓] Exported Markdown Dossier: {md_path}")

    # HTML Report
    html_content = exporter.export_html(athlete, result)
    html_path = os.path.join(output_dir, "executive_report.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    print(f"[✓] Exported HTML Executive Report: {html_path}")

    # Text Summary
    txt_content = exporter.export_summary_text(athlete, result)
    txt_path = os.path.join(output_dir, "executive_summary.txt")
    with open(txt_path, "w") as f:
        f.write(txt_content)
    print(f"[✓] Exported Text Summary: {txt_path}")

    print("\n--- PLAIN TEXT SUMMARY PREVIEW ---")
    print(txt_content)

    print("\n=" * 60)
    print("        REPORT GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
