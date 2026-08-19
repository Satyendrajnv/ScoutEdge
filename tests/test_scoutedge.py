"""
Unit Test Suite for ScoutEdge Core Intelligence Systems
"""

import sys
import os
import unittest

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.rating.ser import SEREngine
from scoutedge.growth.pgi import PGIEngine
from scoutedge.readiness.edgecare import EdgeCareEngine
from scoutedge.resume.live_resume import LiveResumeBuilder
from scoutedge.decision.engine import DecisionEngine
from scoutedge.core.pipeline import ScoutEdgePipeline


class TestSEREngine(unittest.TestCase):
    def setUp(self):
        self.engine = SEREngine()

    def test_calculate_rating_empty(self):
        result = self.engine.calculate_rating([], [])
        self.assertEqual(result.overall_rating, 50.0)
        self.assertIn("Insufficient signal volume", result.key_drivers)

    def test_calculate_rating_with_signals(self):
        perf_signals = [
            PerformanceSignal(
                signal_id="p1",
                athlete_id="ath_1",
                timestamp="2026-08-01",
                match_id="m1",
                minutes_played=90,
                raw_stats={"pass_accuracy": 88.0, "tackles_won": 82.0, "key_passes": 75.0},
                opponent_tier_weight=1.1,
            )
        ]
        scout_signals = [
            ScoutSignal(
                signal_id="s1",
                athlete_id="ath_1",
                scout_id="scout_9",
                timestamp="2026-08-01",
                technical_score=85.0,
                tactical_score=80.0,
                physical_score=88.0,
                mental_score=82.0,
            )
        ]
        result = self.engine.calculate_rating(perf_signals, scout_signals)
        self.assertGreater(result.overall_rating, 75.0)
        self.assertGreater(result.confidence_score, 0.3)


class TestPGIEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PGIEngine()

    def test_calculate_growth(self):
        ser_output = SEREngine().calculate_rating([], [])
        result = self.engine.calculate_growth([ser_output], age_years=19.5)
        self.assertEqual(result.development_stage, "Early Development")
        self.assertGreater(result.growth_ceiling_projection, ser_output.overall_rating)


class TestEdgeCareEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EdgeCareEngine()

    def test_calculate_readiness(self):
        signals = [
            ReadinessSignal(
                signal_id="r1",
                athlete_id="ath_1",
                timestamp="2026-08-18",
                acute_workload_7d=350.0,
                chronic_workload_28d=1400.0,  # Weekly avg = 350 -> ACWR = 1.0
                sleep_quality_score=85.0,
                fatigue_level=20.0,
            )
        ]
        result = self.engine.calculate_readiness(signals)
        self.assertEqual(result.acwr_ratio, 1.0)
        self.assertEqual(result.injury_risk_category, "Low")
        self.assertEqual(result.recommended_minutes, 90)


class TestScoutEdgePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ScoutEdgePipeline()

    def test_end_to_end_pipeline(self):
        profile = AthleteProfile(
            athlete_id="ath_100",
            name="Alex Morgan",
            sport="Soccer",
            primary_position="Central Midfield",
            birth_date="2005-04-12",
            height_cm=182.0,
            weight_kg=75.0,
            current_team="ScoutEdge Academy FC",
        )

        perf = [
            PerformanceSignal(
                signal_id="p1",
                athlete_id="ath_100",
                timestamp="2026-08-10",
                match_id="m10",
                minutes_played=90,
                raw_stats={"pass_accuracy": 92.0, "interceptions": 85.0},
                opponent_tier_weight=1.05,
            )
        ]

        scout = [
            ScoutSignal(
                signal_id="s1",
                athlete_id="ath_100",
                scout_id="sc_1",
                timestamp="2026-08-10",
                technical_score=88.0,
                tactical_score=86.0,
                physical_score=84.0,
                mental_score=90.0,
            )
        ]

        readiness = [
            ReadinessSignal(
                signal_id="r1",
                athlete_id="ath_100",
                timestamp="2026-08-18",
                acute_workload_7d=320.0,
                chronic_workload_28d=1280.0,
                sleep_quality_score=90.0,
                fatigue_level=15.0,
            )
        ]

        eval_result = self.pipeline.process_athlete(profile, perf, scout, readiness, age_years=21.0)
        self.assertEqual(eval_result.athlete_id, "ath_100")
        self.assertGreater(eval_result.fit_score, 70.0)
        self.assertIn("Sign", eval_result.recommendation)


if __name__ == "__main__":
    unittest.main()
