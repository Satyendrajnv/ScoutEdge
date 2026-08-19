"""
ScoutEdge Command Line Interface (CLI) Entrypoint
"""

import sys
import os
import json
import argparse
from typing import List, Optional

from scoutedge import __version__
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.tools.generator import SyntheticDataGenerator
from scoutedge.tools.benchmark import PipelineBenchmark
from scoutedge.api.server import create_scoutedge_app
from scoutedge.api.schemas import (
    parse_athlete_profile,
    parse_performance_signals,
    parse_scout_signals,
    parse_readiness_signals,
)


def render_score_bar(score: float, width: int = 20) -> str:
    """Renders ASCII progress bar for numeric scores (0-100)."""
    filled = int(round((score / 100.0) * width))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score:5.1f}/100"


def handle_version(args: argparse.Namespace):
    print(f"ScoutEdge Sports Intelligence Infrastructure v{__version__}")
    print("EdgeSphere Sports Intelligence Private Limited")


def handle_eval(args: argparse.Namespace):
    pipeline = ScoutEdgePipeline()

    if args.demo or not args.file:
        print("[+] Running ScoutEdge Evaluation on Demo Athlete Profile...")
        generator = SyntheticDataGenerator(seed=77)
        profile, age = generator.generate_athlete(1)
        perf, scout, readiness = generator.generate_signals(profile.athlete_id, num_matches=3)
    else:
        if not os.path.exists(args.file):
            print(f"Error: File not found at '{args.file}'", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r") as f:
            data = json.load(f)
        profile = parse_athlete_profile(data.get("athlete", {}))
        perf = parse_performance_signals(data.get("performance_signals", []))
        scout = parse_scout_signals(data.get("scout_signals", []))
        readiness = parse_readiness_signals(data.get("readiness_signals", []))
        age = float(data.get("age_years", 21.0))

    result = pipeline.process_athlete(profile, perf, scout, readiness, age)

    print("\n" + "=" * 65)
    print(f"          SCOUTEDGE ATHLETE EVALUATION REPORT")
    print("=" * 65)
    print(f"  Athlete Name:      {profile.name}")
    print(f"  Position / Team:   {profile.primary_position} | {profile.current_team}")
    print(f"  League Tier:       {profile.league_tier}")
    print("-" * 65)
    print(f"  SE-R™ Rating:      {render_score_bar(result.se_r.overall_rating)} (Percentile: {result.se_r.percentile_rank}%)")
    print(f"  PGI™ Growth:       {render_score_bar(result.pgi.pgi_score)} Stage: {result.pgi.development_stage}")
    print(f"  EdgeCare™ Mins:    {render_score_bar(result.edgecare.readiness_index)} Risk: {result.edgecare.injury_risk_category} (ACWR: {result.edgecare.acwr_ratio})")
    print(f"  Overall Fit Score: {render_score_bar(result.fit_score)}")
    print("-" * 65)
    print(f"  FINAL RECOMMENDATION: >>> {result.recommendation.upper()} <<<")
    print("-" * 65)
    print("  Explainability Evidence Reasons:")
    for reason in result.explainability_reasons:
        print(f"   ✓ {reason}")
    print("=" * 65 + "\n")


def handle_benchmark(args: argparse.Namespace):
    count = args.count
    print(f"[+] Starting ScoutEdge Bulk Benchmark on {count} Synthetic Athletes...")
    generator = SyntheticDataGenerator(seed=101)
    cohort = generator.generate_cohort(count=count, num_matches_per_athlete=3)

    benchmark = PipelineBenchmark()
    stats = benchmark.run_benchmark(cohort)

    print("\n" + "=" * 65)
    print("          SCOUTEDGE PIPELINE BENCHMARK REPORT")
    print("=" * 65)
    print(f"  Total Athletes Evaluated:   {stats['num_athletes_evaluated']}")
    print(f"  Total Execution Time:       {stats['total_execution_time_sec']} seconds")
    print(f"  Throughput Speed:           {stats['throughput_evaluations_per_sec']} evaluations/second")
    print(f"  Average Latency per Record: {stats['average_latency_ms']} ms")
    print("-" * 65)
    print(f"  Average SE-R™ Rating:       {stats['metric_averages']['average_se_r_rating']:.1f}/100")
    print(f"  Average Fit Score:          {stats['metric_averages']['average_fit_score']:.1f}/100")
    print("-" * 65)
    print("  Decision Recommendation Breakdown:")
    for rec, num in stats["recommendation_distribution"].items():
        pct = (num / count) * 100.0
        print(f"   • {rec:<35}: {num:>4} ({pct:4.1f}%)")
    print("=" * 65 + "\n")


def handle_server(args: argparse.Namespace):
    host = args.host
    port = args.port
    print(f"Starting ScoutEdge REST API Server on http://{host}:{port}...")
    server = create_scoutedge_app(host=host, port=port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down ScoutEdge API server.")
        server.server_close()


def main():
    parser = argparse.ArgumentParser(
        prog="scoutedge",
        description="ScoutEdge Sports Intelligence CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # subcommand: version
    subparsers.add_parser("version", help="Show ScoutEdge CLI version")

    # subcommand: eval
    parser_eval = subparsers.add_parser("eval", help="Evaluate athlete payload")
    parser_eval.add_argument("--file", "-f", type=str, help="Path to JSON payload file")
    parser_eval.add_argument("--demo", action="store_true", help="Run with demo athlete dataset")

    # subcommand: benchmark
    parser_bench = subparsers.add_parser("benchmark", help="Run bulk cohort performance benchmark")
    parser_bench.add_argument("--count", "-c", type=int, default=1000, help="Number of synthetic athletes (default: 1000)")

    # subcommand: server
    parser_server = subparsers.add_parser("server", help="Launch REST API server gateway")
    parser_server.add_argument("--host", type=str, default="0.0.0.0", help="Binding host (default: 0.0.0.0)")
    parser_server.add_argument("--port", type=int, default=8000, help="Binding port (default: 8000)")

    args = parser.parse_args()

    if args.command == "version":
        handle_version(args)
    elif args.command == "eval":
        handle_eval(args)
    elif args.command == "benchmark":
        handle_benchmark(args)
    elif args.command == "server":
        handle_server(args)
    else:
        # Default behavior if no subcommand: run eval --demo
        handle_eval(argparse.Namespace(demo=True, file=None))


if __name__ == "__main__":
    main()
