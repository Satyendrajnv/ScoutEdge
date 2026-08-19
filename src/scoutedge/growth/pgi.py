"""
PGI™ (Player Growth Index) Reference Implementation
"""

from typing import List
from scoutedge.models import SERRatingOutput, PGIOutput


class PGIEngine:
    """
    Player Growth Index Engine (PGI™)

    Evaluates longitudinal rating trajectories over time to project developmental velocity,
    growth ceilings, and potential indices.
    """

    def calculate_growth(
        self,
        historical_ratings: List[SERRatingOutput],
        age_years: float,
    ) -> PGIOutput:
        """
        Calculates PGI™ index based on rating history and age-band curves.
        """
        if not historical_ratings:
            return PGIOutput(
                pgi_score=50.0,
                progression_velocity=0.0,
                growth_ceiling_projection=65.0,
                development_stage="Emerging",
                growth_factors=["Baseline initial evaluation"],
            )

        ratings = [r.overall_rating for r in historical_ratings]
        current_rating = ratings[-1]

        # Calculate progression velocity (delta over evaluations)
        velocity = 0.0
        if len(ratings) > 1:
            velocity = (ratings[-1] - ratings[0]) / max(len(ratings) - 1, 1)

        # Age-band potential projection multiplier
        if age_years < 20:
            stage = "Early Development"
            ceiling_multiplier = 1.25
        elif age_years < 24:
            stage = "Emerging Potential"
            ceiling_multiplier = 1.15
        elif age_years < 29:
            stage = "Peak Output"
            ceiling_multiplier = 1.05
        else:
            stage = "Experienced Veteran"
            ceiling_multiplier = 1.00

        projected_ceiling = min(current_rating * ceiling_multiplier, 99.0)

        # PGI Score computation
        pgi = (current_rating * 0.5) + (velocity * 10.0) + (projected_ceiling * 0.3)
        pgi = min(max(pgi, 1.0), 99.0)

        factors = []
        if velocity > 2.0:
            factors.append("Accelerated rating trajectory over recent matches")
        if age_years < 22:
            factors.append("High upside age-curve dynamic")
        if not factors:
            factors.append("Steady developmental baseline")

        return PGIOutput(
            pgi_score=round(pgi, 2),
            progression_velocity=round(velocity, 2),
            growth_ceiling_projection=round(projected_ceiling, 2),
            development_stage=stage,
            growth_factors=factors,
        )
