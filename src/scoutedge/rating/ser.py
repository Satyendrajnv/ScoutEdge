"""
SE-R™ (ScoutEdge Rating Engine) Reference Implementation
"""

from typing import List, Optional
from scoutedge.models import PerformanceSignal, ScoutSignal, SERRatingOutput


class SEREngine:
    """
    ScoutEdge Rating Engine (SE-R™)

    Evaluates performance statistics and structured scout observations to derive
    standardized, position-adjusted athlete performance ratings.
    """

    def __init__(self, baseline_weight: float = 0.6, scout_weight: float = 0.4):
        self.baseline_weight = baseline_weight
        self.scout_weight = scout_weight

    def calculate_rating(
        self,
        performance_signals: List[PerformanceSignal],
        scout_signals: List[ScoutSignal],
        position: str = "General",
    ) -> SERRatingOutput:
        """
        Calculates SE-R™ ratings from performance and scouting signals.
        """
        if not performance_signals and not scout_signals:
            return SERRatingOutput(
                overall_rating=50.0,
                technical_rating=50.0,
                physical_rating=50.0,
                tactical_rating=50.0,
                confidence_score=0.1,
                percentile_rank=50.0,
                key_drivers=["Insufficient signal volume"],
            )

        # 1. Performance Statistical Rating
        perf_score = 50.0
        if performance_signals:
            raw_scores = []
            for p in performance_signals:
                # Weighted metric aggregation
                stat_avg = sum(p.raw_stats.values()) / max(len(p.raw_stats), 1)
                raw_scores.append(stat_avg * p.opponent_tier_weight)
            perf_score = min(max(sum(raw_scores) / len(raw_scores), 0.0), 100.0)

        # 2. Scout Signal Rating
        scout_tech = 50.0
        scout_tact = 50.0
        scout_phys = 50.0

        if scout_signals:
            scout_tech = sum(s.technical_score for s in scout_signals) / len(scout_signals)
            scout_tact = sum(s.tactical_score for s in scout_signals) / len(scout_signals)
            scout_phys = sum(s.physical_score for s in scout_signals) / len(scout_signals)

        scout_avg = (scout_tech + scout_tact + scout_phys) / 3.0

        # 3. Hybrid Synthesis
        if performance_signals and scout_signals:
            overall = (perf_score * self.baseline_weight) + (scout_avg * self.scout_weight)
        elif performance_signals:
            overall = perf_score
        else:
            overall = scout_avg

        confidence = min((len(performance_signals) * 0.15) + (len(scout_signals) * 0.25), 1.0)
        percentile = min(max(overall * 0.95 + 2.5, 1.0), 99.0)

        drivers = []
        if scout_tech > 75:
            drivers.append("High technical proficiency observed by scouts")
        if perf_score > 75:
            drivers.append("Exceptional statistical performance output")
        if not drivers:
            drivers.append("Balanced baseline performance profile")

        return SERRatingOutput(
            overall_rating=round(overall, 2),
            technical_rating=round(scout_tech, 2),
            physical_rating=round(scout_phys, 2),
            tactical_rating=round(scout_tact, 2),
            confidence_score=round(confidence, 2),
            percentile_rank=round(percentile, 1),
            key_drivers=drivers,
        )
