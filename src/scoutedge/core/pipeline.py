"""
ScoutEdge Core Intelligence Pipeline Orchestrator
"""

from typing import List, Optional
from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
    EvaluationResult,
)
from scoutedge.rating.ser import SEREngine
from scoutedge.growth.pgi import PGIEngine
from scoutedge.readiness.edgecare import EdgeCareEngine
from scoutedge.resume.live_resume import LiveResumeBuilder
from scoutedge.decision.engine import DecisionEngine


class ScoutEdgePipeline:
    """
    ScoutEdge Intelligence Pipeline Manager

    Orchestrates signal ingestion across performance stats, scout observations,
    and physical readiness signals, executing rating, growth, readiness,
    resume, and decision subsystems in sequence.
    """

    def __init__(self):
        self.ser_engine = SEREngine()
        self.pgi_engine = PGIEngine()
        self.edgecare_engine = EdgeCareEngine()
        self.resume_builder = LiveResumeBuilder()
        self.decision_engine = DecisionEngine()

    def process_athlete(
        self,
        profile: AthleteProfile,
        performance_signals: List[PerformanceSignal],
        scout_signals: List[ScoutSignal],
        readiness_signals: List[ReadinessSignal],
        age_years: float = 21.0,
    ) -> EvaluationResult:
        """
        Executes end-to-end intelligence synthesis for a given athlete profile.
        """
        # 1. Calculate SE-R Rating
        se_r_output = self.ser_engine.calculate_rating(
            performance_signals, scout_signals, profile.primary_position
        )

        # 2. Calculate Player Growth Index (PGI)
        pgi_output = self.pgi_engine.calculate_growth([se_r_output], age_years)

        # 3. Calculate EdgeCare Readiness
        edgecare_output = self.edgecare_engine.calculate_readiness(readiness_signals)

        # 4. Generate Live Resume Record
        live_resume = self.resume_builder.build_resume(
            profile, se_r_output, pgi_output, edgecare_output
        )

        # 5. Synthesize Decision Recommendation
        evaluation = self.decision_engine.evaluate(
            profile, se_r_output, pgi_output, edgecare_output, live_resume
        )

        return evaluation
