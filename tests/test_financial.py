"""
Unit Tests for ScoutEdge Financial Value & Contract Efficiency Subsystem
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.financial.engine import (
    FinancialContractModel,
    ValueEfficiencyEngine,
)


class TestFinancialEfficiency(unittest.TestCase):
    def setUp(self):
        self.pipeline = ScoutEdgePipeline()
        self.engine = ValueEfficiencyEngine()

        self.profile = AthleteProfile(
            athlete_id="ath_fin_01",
            name="Xavi Simons",
            sport="Soccer",
            primary_position="Attacking Midfield",
            birth_date="2003-04-21",
            height_cm=179.0,
            weight_kg=72.0,
            current_team="Leipzig FC",
        )

        perf = [
            PerformanceSignal(
                signal_id="p1",
                athlete_id="ath_fin_01",
                timestamp="2026-08-01",
                match_id="m1",
                minutes_played=90,
                raw_stats={"key_passes": 90.0, "dribbles": 88.0},
            )
        ]
        scout = [
            ScoutSignal(
                signal_id="s1",
                athlete_id="ath_fin_01",
                scout_id="sc1",
                timestamp="2026-08-01",
                technical_score=90.0,
                tactical_score=88.0,
                physical_score=84.0,
                mental_score=88.0,
            )
        ]
        readiness = [
            ReadinessSignal(
                signal_id="r1",
                athlete_id="ath_fin_01",
                timestamp="2026-08-18",
                acute_workload_7d=320.0,
                chronic_workload_28d=1280.0,
                sleep_quality_score=90.0,
                fatigue_level=15.0,
            )
        ]

        self.eval_result = self.pipeline.process_athlete(
            self.profile, perf, scout, readiness, age_years=23.0
        )

    def test_undervalued_contract_evaluation(self):
        # High SE-R rating (88+), low market value (€8M) -> Undervalued Opportunity
        contract = FinancialContractModel(
            market_value_eur=8_000_000.0,
            weekly_wage_eur=25_000.0,
            contract_years_remaining=1.0,
        )

        output = self.engine.evaluate_financials(
            self.profile, self.eval_result, contract, age_years=21.5
        )

        self.assertEqual(output.valuation_category, "Undervalued Opportunity")
        self.assertGreater(output.value_for_money_index, 70.0)
        self.assertGreater(output.rating_per_million_value, 8.0)
        self.assertIn("High performance-to-cost ratio", output.financial_reasons[0])

    def test_overpriced_contract_evaluation(self):
        # Low SE-R rating (50), high market value (€120M) -> Overpriced Risk
        profile_low = AthleteProfile(
            athlete_id="ath_fin_02",
            name="Overpriced Target",
            sport="Soccer",
            primary_position="Winger",
            birth_date="1998-01-01",
            height_cm=180.0,
            weight_kg=75.0,
            current_team="Mega Club",
        )
        eval_low = self.pipeline.process_athlete(profile_low, [], [], [], age_years=28.0)

        contract = FinancialContractModel(
            market_value_eur=120_000_000.0,
            weekly_wage_eur=300_000.0,
            contract_years_remaining=4.0,
        )

        output = self.engine.evaluate_financials(profile_low, eval_low, contract, age_years=28.0)
        self.assertEqual(output.valuation_category, "Premium / Overpriced Risk")
        self.assertLess(output.value_for_money_index, 40.0)


if __name__ == "__main__":
    unittest.main()
