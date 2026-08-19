#!/usr/bin/env python3
"""
ScoutEdge Demonstration Script
~~~~~~~~~~~~~~~~────────~~~~~~
Demonstrates end-to-end athlete signal ingestion, rating calculation (SE-R™),
growth index projection (PGI™), readiness evaluation (EdgeCare™), Live Resume™
compilation, and explainable recruitment recommendation synthesis.
"""

import sys
import os
import json

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.core.pipeline import ScoutEdgePipeline


def main():
    print("=" * 60)
    print("      SCOUTEDGE SPORTS INTELLIGENCE PIPELINE DEMO")
    print("=" * 60)

    # 1. Define Athlete Profile
    athlete = AthleteProfile(
        athlete_id="ath_2026_09",
        name="Julian Vance",
        sport="Football / Soccer",
        primary_position="Attacking Midfield",
        birth_date="2005-03-14",
        height_cm=178.5,
        weight_kg=72.0,
        current_team="Apex Youth Academy",
        league_tier="U21 National Division",
    )
    print(f"\n[+] Ingesting Athlete Profile: {athlete.name} ({athlete.primary_position})")

    # 2. Performance Stats Signals
    perf_signals = [
        PerformanceSignal(
            signal_id="sig_p01",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-05",
            match_id="m_101",
            minutes_played=90,
            raw_stats={"pass_accuracy": 89.5, "key_passes": 86.0, "dribbles_completed": 84.0},
            opponent_tier_weight=1.1,
        ),
        PerformanceSignal(
            signal_id="sig_p02",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-12",
            match_id="m_108",
            minutes_played=88,
            raw_stats={"pass_accuracy": 91.0, "key_passes": 88.0, "dribbles_completed": 82.0},
            opponent_tier_weight=1.15,
        ),
    ]

    # 3. Scout Field Signals
    scout_signals = [
        ScoutSignal(
            signal_id="sig_s01",
            athlete_id=athlete.athlete_id,
            scout_id="scout_lead_04",
            timestamp="2026-08-12",
            technical_score=88.0,
            tactical_score=85.0,
            physical_score=82.0,
            mental_score=89.0,
            qualitative_notes="Exceptional spatial awareness and vision under pressure.",
        )
    ]

    # 4. Readiness & Workload Signals
    readiness_signals = [
        ReadinessSignal(
            signal_id="sig_r01",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-18",
            acute_workload_7d=340.0,
            chronic_workload_28d=1360.0,  # ACWR = 1.0 (Optimal)
            sleep_quality_score=88.0,
            fatigue_level=18.0,
            availability_status="Available",
        )
    ]

    # 5. Run ScoutEdge Intelligence Pipeline
    pipeline = ScoutEdgePipeline()
    result = pipeline.process_athlete(
        profile=athlete,
        performance_signals=perf_signals,
        scout_signals=scout_signals,
        readiness_signals=readiness_signals,
        age_years=21.4,
    )

    # 6. Display Intelligence Synthesis Results
    print("\n--- SCOUTEDGE INTELLIGENCE OUTPUT ---")
    print(f"• SE-R™ Rating:         {result.se_r.overall_rating} / 100 (Percentile: {result.se_r.percentile_rank}%)")
    print(f"• PGI™ Growth Score:    {result.pgi.pgi_score} / 100 (Stage: {result.pgi.development_stage})")
    print(f"• EdgeCare™ Readiness:  {result.edgecare.readiness_index} / 100 (ACWR: {result.edgecare.acwr_ratio}, Risk: {result.edgecare.injury_risk_category})")
    print(f"• Decision Fit Score:   {result.fit_score} / 100")
    print(f"• Final Recommendation: {result.recommendation.upper()}")

    print("\n--- EXPLAINABILITY REASON CODES ---")
    for reason in result.explainability_reasons:
        print(f"  ✓ {reason}")

    print("\n--- LIVE RESUME™ RECORD ---")
    print(f"Summary: {result.live_resume.career_trajectory_summary}")

    print("\n=" * 60)
    print("       SCOUTEDGE PIPELINE EXECUTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
