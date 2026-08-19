"""
Bulk Pipeline Benchmarking Utility for ScoutEdge
"""

import time
from typing import List, Dict, Any, Optional

from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.models import EvaluationResult


class PipelineBenchmark:
    """
    Executes high-throughput batch evaluation benchmarks on synthetic athlete datasets,
    computing processing speed (evaluations/sec), execution latency, rating percentiles,
    and recommendation distribution statistics.
    """

    def __init__(self, pipeline: Optional[ScoutEdgePipeline] = None):
        self.pipeline = pipeline or ScoutEdgePipeline()

    def run_benchmark(self, cohort: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Runs bulk evaluation over athlete cohort and returns benchmark statistics."""
        num_athletes = len(cohort)
        results: List[EvaluationResult] = []

        start_time = time.perf_counter()

        for item in cohort:
            res = self.pipeline.process_athlete(
                profile=item["profile"],
                performance_signals=item["performance_signals"],
                scout_signals=item["scout_signals"],
                readiness_signals=item["readiness_signals"],
                age_years=item["age_years"],
            )
            results.append(res)

        end_time = time.perf_counter()
        total_time_sec = end_time - start_time
        evals_per_sec = num_athletes / max(total_time_sec, 0.0001)

        # Statistics computation
        fit_scores = [r.fit_score for r in results]
        se_r_scores = [r.se_r.overall_rating for r in results]
        recommendations = {}

        for r in results:
            rec = r.recommendation
            recommendations[rec] = recommendations.get(rec, 0) + 1

        avg_fit_score = sum(fit_scores) / max(len(fit_scores), 1)
        avg_se_r = sum(se_r_scores) / max(len(se_r_scores), 1)

        return {
            "num_athletes_evaluated": num_athletes,
            "total_execution_time_sec": round(total_time_sec, 4),
            "throughput_evaluations_per_sec": round(evals_per_sec, 2),
            "average_latency_ms": round((total_time_sec / max(num_athletes, 1)) * 1000.0, 3),
            "metric_averages": {
                "average_se_r_rating": round(avg_se_r, 2),
                "average_fit_score": round(avg_fit_score, 2),
            },
            "recommendation_distribution": recommendations,
        }
