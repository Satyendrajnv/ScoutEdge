#!/usr/bin/env python3
"""
ScoutEdge Squad Replacement & Opportunity Matching Demo
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
from scoutedge.matching.engine import SquadNeedProfile, OpportunityMatcher, SquadGapAnalyzer
from scoutedge.tools.generator import SyntheticDataGenerator


def main():
    print("=" * 65)
    print("     SCOUTEDGE SQUAD REPLACEMENT & OPPORTUNITY MATCHING DEMO")
    print("=" * 65)

    # 1. Generate Synthetic Candidate Pool (20 Athletes)
    print("\n[+] Ingesting Candidate Talent Pool (20 Athletes)...")
    generator = SyntheticDataGenerator(seed=88)
    pipeline = ScoutEdgePipeline()

    cohort = generator.generate_cohort(count=20, num_matches_per_athlete=3)
    candidate_pool = []

    for item in cohort:
        profile = item["profile"]
        eval_result = pipeline.process_athlete(
            profile,
            item["performance_signals"],
            item["scout_signals"],
            item["readiness_signals"],
            item["age_years"],
        )
        candidate_pool.append((profile, eval_result, item["age_years"]))

    # 2. Define Squad Need Profile for a Departing Starter
    print("\n[+] Defining Squad Replacement Target Criteria:")
    squad_need = SquadNeedProfile(
        target_position="Attacking Midfield",
        min_se_r=75.0,
        min_pgi=70.0,
        max_injury_risk="Moderate",
        max_age_years=25.0,
        required_traits=["High pressure resistance", "Spatial control in halfspaces"],
    )

    print(f"  • Target Position:  {squad_need.target_position}")
    print(f"  • Minimum SE-R™:    {squad_need.min_se_r} / 100")
    print(f"  • Minimum PGI™:     {squad_need.min_pgi} / 100")
    print(f"  • Max Age Threshold:{squad_need.max_age_years} years")

    # 3. Execute Opportunity Matcher
    matcher = OpportunityMatcher()
    shortlist = matcher.rank_candidates(candidate_pool, squad_need)

    print("\n" + "=" * 65)
    print("        RANKED TACTICAL RECRUITMENT SHORTLIST")
    print("=" * 65)

    for rank, candidate in enumerate(shortlist, start=1):
        print(f"\n[#{rank}] {candidate.athlete_name} ({candidate.current_team})")
        print(f"    • Compatibility Tier: {candidate.compatibility_tier.upper()}")
        print(f"    • Match Score:        {candidate.match_score} / 100")
        print(f"    • Gap Closure:        {candidate.gap_closure_percentage}%")
        print(f"    • SE-R™ Rating:       {candidate.evaluation.se_r.overall_rating} (Percentile: {candidate.evaluation.se_r.percentile_rank}%)")
        print(f"    • PGI™ Growth Index:  {candidate.evaluation.pgi.pgi_score} ({candidate.evaluation.pgi.development_stage})")
        print(f"    • EdgeCare™ Risk:     {candidate.evaluation.edgecare.injury_risk_category} (ACWR: {candidate.evaluation.edgecare.acwr_ratio})")
        print("    • Match Drivers:")
        for driver in candidate.match_reasons:
            print(f"       ✓ {driver}")

    print("\n=" * 65)
    print("        OPPORTUNITY MATCHING DEMO COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()
