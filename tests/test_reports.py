"""
Unit Tests for ScoutEdge Executive Report Exporter Subsystem
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.reports.exporter import ScoutReportExporter


class TestReportExporter(unittest.TestCase):
    def setUp(self):
        self.pipeline = ScoutEdgePipeline()
        self.exporter = ScoutReportExporter()

        self.profile = AthleteProfile(
            athlete_id="ath_report_101",
            name="Florian Wirtz",
            sport="Soccer",
            primary_position="Attacking Midfield",
            birth_date="2003-05-03",
            height_cm=177.0,
            weight_kg=71.0,
            current_team="Rhine Valley FC",
            league_tier="Bundesliga",
        )

        perf = [
            PerformanceSignal(
                signal_id="p1",
                athlete_id="ath_report_101",
                timestamp="2026-08-10",
                match_id="m1",
                minutes_played=90,
                raw_stats={"key_passes": 95.0, "dribbles": 90.0},
            )
        ]

        scout = [
            ScoutSignal(
                signal_id="s1",
                athlete_id="ath_report_101",
                scout_id="sc1",
                timestamp="2026-08-10",
                technical_score=92.0,
                tactical_score=90.0,
                physical_score=85.0,
                mental_score=91.0,
            )
        ]

        readiness = [
            ReadinessSignal(
                signal_id="r1",
                athlete_id="ath_report_101",
                timestamp="2026-08-18",
                acute_workload_7d=320.0,
                chronic_workload_28d=1280.0,
                sleep_quality_score=92.0,
                fatigue_level=12.0,
            )
        ]

        self.eval_result = self.pipeline.process_athlete(
            self.profile, perf, scout, readiness, age_years=23.2
        )

    def test_export_markdown(self):
        md = self.exporter.export_markdown(self.profile, self.eval_result)
        self.assertIn("# SCOUTEDGE EXECUTIVE SCOUTING DOSSIER", md)
        self.assertIn("Florian Wirtz", md)
        self.assertIn("SE-R™ Performance Rating", md)
        self.assertIn("Recommendation", md)

    def test_export_html(self):
        html = self.exporter.export_html(self.profile, self.eval_result)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("ScoutEdge Dossier — Florian Wirtz", html)
        self.assertIn("recommendation-title", html)
        self.assertIn("SE-R™ Performance Rating", html)

    def test_export_summary_text(self):
        txt = self.exporter.export_summary_text(self.profile, self.eval_result)
        self.assertIn("SCOUTEDGE REPORT: Florian Wirtz", txt)
        self.assertIn("SE-R Rating", txt)
        self.assertIn("RECOMMENDATION", txt)


if __name__ == "__main__":
    unittest.main()
