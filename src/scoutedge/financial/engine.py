"""
Financial Value & Contract Efficiency Engine Implementation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional

from scoutedge.models import AthleteProfile, EvaluationResult


@dataclass
class FinancialContractModel:
    market_value_eur: float           # Estimated transfer market value in EUR
    weekly_wage_eur: float            # Weekly gross wage in EUR
    contract_years_remaining: float   # Years left on current contract
    release_clause_eur: Optional[float] = None


@dataclass
class ValueEfficiencyOutput:
    value_for_money_index: float      # Scale 0.0 to 100.0
    wage_efficiency_score: float      # Scale 0.0 to 100.0
    rating_per_million_value: float   # SE-R points per €1M
    valuation_category: str            # Undervalued Opportunity, Fair Market Value, Premium / Overpriced Risk
    projected_3yr_resale_upside_pct: float
    financial_reasons: List[str] = field(default_factory=list)


class ValueEfficiencyEngine:
    """
    ValueEfficiencyEngine

    Calculates performance-to-market-value efficiency, wage output alignment,
    resale ROI projections, and classifies financial recruitment value.
    """

    def evaluate_financials(
        self,
        profile: AthleteProfile,
        evaluation: EvaluationResult,
        contract: FinancialContractModel,
        age_years: float = 22.5,
    ) -> ValueEfficiencyOutput:
        """Evaluates financial efficiency and ROI potential for candidate athlete."""
        se_r = evaluation.se_r.overall_rating
        pgi = evaluation.pgi.pgi_score
        market_val_m = max(contract.market_value_eur / 1000000.0, 0.1)
        annual_wage_k = (contract.weekly_wage_eur * 52.0) / 1000.0

        # 1. Rating per €1M Market Value
        rating_per_m = round(se_r / market_val_m, 2)

        # 2. Value-for-Money Index Calculation (Base 50.0)
        # Expected market value benchmark based on SE-R rating (Exponential curve)
        expected_val_m = max((se_r / 15.0) ** 2.2, 0.5)
        value_ratio = expected_val_m / market_val_m

        vfm_index = round(min(max(value_ratio * 50.0, 0.0), 100.0), 2)

        # 3. Wage Efficiency Score (Base 50.0)
        expected_wage_k = max(se_r * 1.5, 10.0)
        wage_ratio = expected_wage_k / max(annual_wage_k, 1.0)
        wage_efficiency = round(min(max(wage_ratio * 50.0, 0.0), 100.0), 2)

        # 4. 3-Year Resale Upside Projection
        if age_years < 22:
            resale_upside = round((pgi - se_r) * 1.8 + 15.0, 1)
        elif age_years < 26:
            resale_upside = round((pgi - se_r) * 1.2 + 5.0, 1)
        else:
            resale_upside = round(max((pgi - se_r) * 0.5 - 10.0, -30.0), 1)

        # 5. Valuation Classification
        reasons = []
        if vfm_index >= 70.0:
            category = "Undervalued Opportunity"
            reasons.append(f"High performance-to-cost ratio ({rating_per_m} SE-R pts per €1M)")
        elif vfm_index >= 45.0:
            category = "Fair Market Value"
            reasons.append("Market value accurately aligns with SE-R™ rating output")
        else:
            category = "Premium / Overpriced Risk"
            reasons.append("Caution: Premium price tag relative to current performance output")

        if wage_efficiency >= 65.0:
            reasons.append("Highly efficient wage structure")
        elif wage_efficiency < 35.0:
            reasons.append("High wage demands relative to rating baseline")

        if resale_upside > 20.0:
            reasons.append(f"High 3-year resale ROI projection (+{resale_upside}%)")

        if contract.contract_years_remaining <= 1.0:
            reasons.append("Contract expiring soon (< 1 year remaining) - Leverage opportunity")

        return ValueEfficiencyOutput(
            value_for_money_index=vfm_index,
            wage_efficiency_score=wage_efficiency,
            rating_per_million_value=rating_per_m,
            valuation_category=category,
            projected_3yr_resale_upside_pct=resale_upside,
            financial_reasons=reasons,
        )
