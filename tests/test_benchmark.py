"""
Unit Tests for Synthetic Data Generator and Benchmark Subsystem
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.tools.generator import SyntheticDataGenerator
from scoutedge.tools.benchmark import PipelineBenchmark


class TestBenchmarkTools(unittest.TestCase):
    def setUp(self):
        self.generator = SyntheticDataGenerator(seed=123)
        self.benchmark = PipelineBenchmark()

    def test_synthetic_data_generation(self):
        profile, age = self.generator.generate_athlete(1)
        self.assertEqual(profile.athlete_id, "ath_synth_0001")
        self.assertTrue(17.0 <= age <= 29.0)

        perf, scout, readiness = self.generator.generate_signals(profile.athlete_id, num_matches=2)
        self.assertEqual(len(perf), 2)
        self.assertEqual(len(scout), 2)
        self.assertEqual(len(readiness), 1)

    def test_cohort_benchmark(self):
        cohort = self.generator.generate_cohort(count=50, num_matches_per_athlete=2)
        self.assertEqual(len(cohort), 50)

        stats = self.benchmark.run_benchmark(cohort)
        self.assertEqual(stats["num_athletes_evaluated"], 50)
        self.assertGreater(stats["throughput_evaluations_per_sec"], 10.0)
        self.assertIn("recommendation_distribution", stats)


if __name__ == "__main__":
    unittest.main()
