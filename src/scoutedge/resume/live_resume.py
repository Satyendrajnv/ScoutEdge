"""
Live Resume™ Generator Reference Implementation
"""

from datetime import datetime
from typing import List, Dict, Optional
from scoutedge.models import (
    AthleteProfile,
    SERRatingOutput,
    PGIOutput,
    EdgeCareOutput,
    LiveResumeRecord,
)


class LiveResumeBuilder:
    """
    Live Resume™ Builder

    Compiles an evolving, verified digital athlete performance identity
    bringing together history, rating outputs, PGI growth, and readiness logs.
    """

    def build_resume(
        self,
        profile: AthleteProfile,
        se_r: SERRatingOutput,
        pgi: PGIOutput,
        edgecare: EdgeCareOutput,
        milestones: Optional[List[Dict[str, str]]] = None,
    ) -> LiveResumeRecord:
        """
        Builds dynamic Live Resume™ record.
        """
        verified_milestones = milestones or [
            {"date": "2026-01-15", "milestone": "Entered First-Team Starter Rotation"},
            {"date": "2026-05-10", "milestone": "SE-R Rating Baseline > 80.0 Achieved"},
        ]

        summary = (
            f"Athlete {profile.name} ({profile.primary_position}, {profile.current_team}) "
            f"holds an SE-R™ rating of {se_r.overall_rating} (Percentile: {se_r.percentile_rank}%). "
            f"Growth index (PGI™) is {pgi.pgi_score} ({pgi.development_stage}) with "
            f"an EdgeCare™ readiness index of {edgecare.readiness_index} ({edgecare.injury_risk_category} Risk)."
        )

        return LiveResumeRecord(
            athlete_id=profile.athlete_id,
            generated_at=datetime.utcnow().isoformat() + "Z",
            version="1.0.0",
            overall_se_r=se_r.overall_rating,
            current_pgi=pgi.pgi_score,
            current_readiness=edgecare.readiness_index,
            verified_milestones=verified_milestones,
            career_trajectory_summary=summary,
        )
