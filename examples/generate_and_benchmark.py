#!/usr/bin/env python3
"""
ScoutEdge Synthetic Data Generation & Bulk Pipeline Benchmarking Demo
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.tools.generator import SyntheticDataGenerator
from scoutedge.tools.benchmark import PipelineBenchmark


def main():
    print("=" * 60)
    print("   SCOUTEDGE SYNTHETIC DATA & BULK PIPELINE BENCHMARK")
    print("=" * 60)

    num_athletes = 1000
    print(f"\n[+] Generating {num_athletes} synthetic athlete profiles & signals...")
    generator = SyntheticDataGenerator(seed=42)
    cohort = generator.generate_cohort(count=num_athletes, num_matches_per_athlete=3)
    print(f"[✓] Cohort generation complete ({len(cohort)} datasets created).")

    print(f"\n[+] Executing bulk intelligence pipeline benchmark...")
    benchmark = PipelineBenchmark()
    stats = benchmark.run_benchmark(cohort)

    print("\n--- PIPELINE BENCHMARK RESULTS ---")
    print(f"• Evaluated Athletes:        {stats['num_athletes_evaluated']}")
    print(f"• Total Execution Time:      {stats['total_execution_time_sec']} seconds")
    print(f"• Throughput:                {stats['throughput_evaluations_per_sec']} evaluations/second")
    print(f"• Average Latency per Record:{stats['average_latency_ms']} ms")

    print("\n--- COHORT METRIC AVERAGES ---")
    print(f"• Average SE-R™ Rating:      {stats['metric_averages']['average_se_r_rating']} / 100")
    print(f"• Average Fit Score:         {stats['metric_averages']['average_fit_score']} / 100")

    print("\n--- RECOMMENDATION DISTRIBUTION ---")
    for rec, count in stats["recommendation_distribution"].items():
        pct = (count / num_athletes) * 100.0
        print(f"  • {rec:<35}: {count:>4} athletes ({pct:4.1f}%)")

    # Export a small sample JSON payload
    sample_path = os.path.join(os.path.dirname(__file__), "synthetic_sample.json")
    sample_data = {
        "athlete_id": cohort[0]["profile"].athlete_id,
        "name": cohort[0]["profile"].name,
        "primary_position": cohort[0]["profile"].primary_position,
        "age_years": cohort[0]["age_years"],
    }
    with open(sample_path, "w") as f:
        json.dump(sample_data, f, indent=2)
    print(f"\n[✓] Sample dataset exported to: {sample_path}")

    print("\n=" * 60)
    print("          BENCHMARK EXECUTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
