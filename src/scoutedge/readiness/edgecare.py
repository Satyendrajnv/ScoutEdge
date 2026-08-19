"""
EdgeCare™ (Readiness & Workload Intelligence) Reference Implementation
"""

from typing import List
from scoutedge.models import ReadinessSignal, EdgeCareOutput


class EdgeCareEngine:
    """
    EdgeCare™ Engine

    Calculates athlete workload continuity, Acute:Chronic Workload Ratios (ACWR),
    injury risk category, and match readiness scores.
    """

    def calculate_readiness(
        self,
        signals: List[ReadinessSignal],
    ) -> EdgeCareOutput:
        """
        Calculates EdgeCare™ readiness index from physical and workload signals.
        """
        if not signals:
            return EdgeCareOutput(
                readiness_index=75.0,
                acwr_ratio=1.0,
                injury_risk_category="Low",
                recommended_minutes=90,
                sustainability_score=80.0,
            )

        latest = signals[-1]
        acute = latest.acute_workload_7d
        chronic = max(latest.chronic_workload_28d, 1.0)

        # ACWR Ratio = 7-day workload / (28-day workload / 4)
        chronic_weekly = chronic / 4.0
        acwr = acute / max(chronic_weekly, 1.0)

        # Risk Classification (Sweet spot: 0.8 - 1.3)
        if 0.8 <= acwr <= 1.3:
            risk = "Low"
            readiness_base = 90.0
            rec_mins = 90
        elif 1.3 < acwr <= 1.5:
            risk = "Moderate"
            readiness_base = 75.0
            rec_mins = 65
        else:
            risk = "High"
            readiness_base = 55.0
            rec_mins = 45

        # Penalize if fatigue level is high or sleep quality low
        readiness = readiness_base - (latest.fatigue_level * 0.2) + (latest.sleep_quality_score * 0.1)
        readiness = min(max(readiness, 0.0), 100.0)

        sustainability = max(100.0 - (abs(acwr - 1.0) * 30.0), 40.0)

        return EdgeCareOutput(
            readiness_index=round(readiness, 2),
            acwr_ratio=round(acwr, 2),
            injury_risk_category=risk,
            recommended_minutes=rec_mins,
            sustainability_score=round(sustainability, 2),
        )
