#!/usr/bin/env python3
"""
ScoutEdge Spatial Tracking & Zonal Impact Analysis Demo
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import AthleteProfile, ScoutSignal, ReadinessSignal
from scoutedge.spatial.analyzer import SpatialControlEngine, SpatialEvent
from scoutedge.core.pipeline import ScoutEdgePipeline


def main():
    print("=" * 60)
    print("   SCOUTEDGE SPATIAL TRACKING & ZONAL IMPACT DEMO")
    print("=" * 60)

    # 1. Define Athlete
    athlete = AthleteProfile(
        athlete_id="ath_spatial_99",
        name="Jamal Musiala-Vance",
        sport="Soccer",
        primary_position="Attacking Midfield",
        birth_date="2003-02-26",
        height_cm=184.0,
        weight_kg=72.0,
        current_team="FC Bavaria",
        league_tier="Division 1",
    )
    print(f"\n[+] Ingesting 2D Pitch Coordinate Events for {athlete.name}...")

    # 2. Simulated 2D Pitch Coordinate Tracking Events (0-100 x/y scale)
    events = [
        SpatialEvent("e1", 120.0, 45.0, 30.0, "reception", True),
        SpatialEvent("e2", 125.0, 45.0, 30.0, "dribble", True, end_x=65.0, end_y=35.0),
        SpatialEvent("e3", 130.0, 65.0, 35.0, "pass", True, end_x=85.0, end_y=45.0),
        SpatialEvent("e4", 340.0, 78.0, 35.0, "reception", True),
        SpatialEvent("e5", 342.0, 78.0, 35.0, "dribble", True, end_x=89.0, end_y=52.0),
        SpatialEvent("e6", 345.0, 89.0, 52.0, "shot", True),
    ]

    # 3. Analyze Spatial Control
    spatial_engine = SpatialControlEngine()
    spatial_metrics = spatial_engine.analyze_events(events)

    print("\n--- TACTICAL SPATIAL METRICS ---")
    print(f"• Total 2D Events Analyzed:    {spatial_metrics.total_events}")
    print(f"• High Threat Zone Touches:    {spatial_metrics.high_threat_zone_touches}")
    print(f"• Progressive Distance Vector: {spatial_metrics.progressive_passing_distance_m} meters")
    print(f"• Dangerous Space Control:    {spatial_metrics.dangerous_space_control_score} / 100")
    print(f"• Pressure Resistance Score:   {spatial_metrics.pressure_resistance_score} / 100")

    # 4. Convert Spatial Tracking Data into Performance Signal for SE-R™ Pipeline
    spatial_perf_signal = spatial_engine.convert_to_performance_signal(
        athlete_id=athlete.athlete_id,
        match_id="m_spatial_2026",
        timestamp="2026-08-18",
        events=events,
        opponent_tier_weight=1.2,
    )

    scout_signals = [
        ScoutSignal(
            signal_id="s1",
            athlete_id=athlete.athlete_id,
            scout_id="sc_tactical",
            timestamp="2026-08-18",
            technical_score=95.0,
            tactical_score=92.0,
            physical_score=86.0,
            mental_score=90.0,
            qualitative_notes="Elite spatial perception in the halfspaces under heavy pressure.",
        )
    ]

    readiness_signals = [
        ReadinessSignal(
            signal_id="r1",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-18",
            acute_workload_7d=340.0,
            chronic_workload_28d=1360.0,
            sleep_quality_score=90.0,
            fatigue_level=15.0,
        )
    ]

    # 5. Run Full ScoutEdge Intelligence Pipeline
    pipeline = ScoutEdgePipeline()
    result = pipeline.process_athlete(
        athlete, [spatial_perf_signal], scout_signals, readiness_signals, age_years=23.4
    )

    print("\n--- SCOUTEDGE INTELLIGENCE SYNTHESIS ---")
    print(f"• SE-R™ Performance Rating: {result.se_r.overall_rating} (Percentile: {result.se_r.percentile_rank}%)")
    print(f"• PGI™ Player Growth Score: {result.pgi.pgi_score} ({result.pgi.development_stage})")
    print(f"• EdgeCare™ Readiness:      {result.edgecare.readiness_index} (ACWR: {result.edgecare.acwr_ratio})")
    print(f"• Final Fit Score:          {result.fit_score} / 100")
    print(f"• Recommendation:           {result.recommendation.upper()}")

    print("\n=" * 60)
    print("      SPATIAL TRACKING DEMO COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
