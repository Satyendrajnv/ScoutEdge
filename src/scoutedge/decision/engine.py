"""
Decision Intelligence Engine Reference Implementation
"""

from typing import List
from scoutedge.models import (
    AthleteProfile,
    SERRatingOutput,
    PGIOutput,
    EdgeCareOutput,
    LiveResumeRecord,
    EvaluationResult,
)


class DecisionEngine:
    """
    Decision Intelligence Engine

    Synthesizes multi-subsystem signals (SE-R™, PGI™, EdgeCare™, Live Resume™)
    into explainable recommendations for evaluation, recruitment, and shortlisting.
    """

    def evaluate(
        self,
        profile: AthleteProfile,
        se_r: SERRatingOutput,
        pgi: PGIOutput,
        edgecare: EdgeCareOutput,
        live_resume: LiveResumeRecord,
    ) -> EvaluationResult:
        """
        Synthesizes signals into a unified evaluation and recommendation output.
        """
        # Weighted Fit Score Formula
        fit_score = (
            (se_r.overall_rating * 0.45) +
            (pgi.pgi_score * 0.35) +
            (edgecare.readiness_index * 0.20)
        )

        reasons = []
        if se_r.overall_rating >= 80.0:
            reasons.append(f"High performance rating (SE-R™: {se_r.overall_rating})")
        if pgi.pgi_score >= 80.0:
            reasons.append(f"Accelerated development trajectory (PGI™: {pgi.pgi_score})")
        if edgecare.injury_risk_category == "Low":
            reasons.append("Low workload injury risk (EdgeCare™)")
        elif edgecare.injury_risk_category == "High":
            reasons.append("Caution: Elevated workload risk flags detected")

        # Recommendation logic
        if fit_score >= 80.0 and edgecare.injury_risk_category != "High":
            recommendation = "Sign / High Priority Target"
        elif fit_score >= 70.0:
            recommendation = "Shortlist & Monitor Development"
        elif fit_score >= 55.0:
            recommendation = "Develop in Academy / Secondary Squad"
        else:
            recommendation = "Pass / Low Alignment"

        return EvaluationResult(
            athlete_id=profile.athlete_id,
            timestamp=live_resume.generated_at,
            se_r=se_r,
            pgi=pgi,
            edgecare=edgecare,
            live_resume=live_resume,
            fit_score=round(fit_score, 2),
            recommendation=recommendation,
            explainability_reasons=reasons,
        )
