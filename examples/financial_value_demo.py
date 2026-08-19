#!/usr/bin/env python3
"""
ScoutEdge Financial Value & Contract Efficiency Demo
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
from scoutedge.financial.engine import FinancialContractModel, ValueEfficiencyEngine


def main():
    print("=" * 65)
    print("     SCOUTEDGE FINANCIAL VALUE & CONTRACT EFFICIENCY DEMO")
    print("=" * 65)

    # 1. Define Athlete Profile
    athlete = AthleteProfile(
        athlete_id="ath_fin_demo",
        name="Arda Guler-Vance",
        sport="Soccer",
        primary_position="Attacking Midfield",
        birth_date="2005-02-25",
        height_cm=176.0,
        weight_kg=69.0,
        current_team="Iberia Sports Club",
        league_tier="Division 1",
    )

    perf = [
        PerformanceSignal(
            signal_id="p1",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-10",
            match_id="m10",
            minutes_played=90,
            raw_stats={"key_passes": 92.0, "dribbles": 89.0, "shot_creation": 91.0},
            opponent_tier_weight=1.15,
        )
    ]

    scout = [
        ScoutSignal(
            signal_id="s1",
            athlete_id=athlete.athlete_id,
            scout_id="scout_exec",
            timestamp="2026-08-10",
            technical_score=92.0,
            tactical_score=88.0,
            physical_score=82.0,
            mental_score=90.0,
            qualitative_notes="Elite vision and set-piece specialist with immense upside.",
        )
    ]

    readiness = [
        ReadinessSignal(
            signal_id="r1",
            athlete_id=athlete.athlete_id,
            timestamp="2026-08-18",
            acute_workload_7d=330.0,
            chronic_workload_28d=1320.0,
            sleep_quality_score=90.0,
            fatigue_level=12.0,
        )
    ]

    # 2. Run Intelligence Pipeline
    pipeline = ScoutEdgePipeline()
    result = pipeline.process_athlete(athlete, perf, scout, readiness, age_years=21.5)

    # 3. Evaluate Financial Contract Details
    contract = FinancialContractModel(
        market_value_eur=12_500_000.0,      # €12.5M
        weekly_wage_eur=35_000.0,           # €35,000 / week
        contract_years_remaining=1.0,       # 1 year left on contract
        release_clause_eur=20_000_000.0,
    )

    fin_engine = ValueEfficiencyEngine()
    fin_output = fin_engine.evaluate_financials(athlete, result, contract, age_years=21.5)

    print(f"\n[+] Athlete: {athlete.name} ({athlete.primary_position}, {athlete.current_team})")
    print(f"  • SE-R™ Rating:        {result.se_r.overall_rating} / 100")
    print(f"  • Market Value:        €{contract.market_value_eur / 1e6:.1f}M")
    print(f"  • Weekly Wage:         €{contract.weekly_wage_eur:,.0f} / week")
    print(f"  • Contract Remaining:  {contract.contract_years_remaining} years")

    print("\n--- FINANCIAL EFFICIENCY INTELLIGENCE ---")
    print(f"• Valuation Classification:   {fin_output.valuation_category.upper()}")
    print(f"• Value-for-Money Index:     {fin_output.value_for_money_index} / 100")
    print(f"• Rating per €1M Value:       {fin_output.rating_per_million_value} SE-R pts / €1M")
    print(f"• Wage Efficiency Score:      {fin_output.wage_efficiency_score} / 100")
    print(f"• Projected 3-Yr Resale ROI:  +{fin_output.projected_3yr_resale_upside_pct}%")

    print("\n--- FINANCIAL REASON CODES ---")
    for reason in fin_output.financial_reasons:
        print(f"  ✓ {reason}")

    print("\n=" * 65)
    print("      FINANCIAL VALUE EVALUATION COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()
