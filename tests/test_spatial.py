"""
Unit Tests for ScoutEdge Spatial Tracking & Zonal Impact Subsystem
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.spatial.analyzer import (
    PitchZoneAnalyzer,
    SpatialControlEngine,
    SpatialEvent,
)


class TestSpatialTracking(unittest.TestCase):
    def setUp(self):
        self.analyzer = PitchZoneAnalyzer()
        self.engine = SpatialControlEngine()

    def test_zone_classification(self):
        self.assertEqual(self.analyzer.get_zone_code(10.0, 10.0), "D_L")
        self.assertEqual(self.analyzer.get_zone_code(50.0, 50.0), "M_C")
        self.assertEqual(self.analyzer.get_zone_code(75.0, 30.0), "A_LH")
        self.assertEqual(self.analyzer.get_zone_code(90.0, 50.0), "BOX_A")
        self.assertEqual(self.analyzer.get_zone_code(10.0, 50.0), "BOX_D")

    def test_spatial_control_analysis(self):
        events = [
            SpatialEvent("e1", 10.0, 50.0, 50.0, "pass", True, end_x=70.0, end_y=30.0),
            SpatialEvent("e2", 25.0, 75.0, 30.0, "reception", True),
            SpatialEvent("e3", 40.0, 88.0, 50.0, "shot", True),
        ]
        metrics = self.engine.analyze_events(events)

        self.assertEqual(metrics.total_events, 3)
        self.assertGreater(metrics.high_threat_zone_touches, 0)
        self.assertGreater(metrics.progressive_passing_distance_m, 15.0)
        self.assertGreater(metrics.dangerous_space_control_score, 40.0)

    def test_performance_signal_conversion(self):
        events = [
            SpatialEvent("e1", 10.0, 75.0, 30.0, "pass", True, end_x=90.0, end_y=50.0),
        ]
        signal = self.engine.convert_to_performance_signal(
            athlete_id="ath_spatial_1", match_id="m_100", timestamp="2026-08-19", events=events
        )
        self.assertEqual(signal.athlete_id, "ath_spatial_1")
        self.assertIn("spatial_control_score", signal.raw_stats)
        self.assertIn("pressure_resistance_score", signal.raw_stats)


if __name__ == "__main__":
    unittest.main()
