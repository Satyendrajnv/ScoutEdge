"""
ScoutEdge Intelligence Infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An open, modular AI-powered intelligence framework for sports talent evaluation,
longitudinal growth tracking, athlete readiness, and explainable decision synthesis.
"""

__version__ = "0.1.0"
__author__ = "EdgeSphere Sports Intelligence Private Limited"

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
from scoutedge.core.pipeline import ScoutEdgePipeline

__all__ = [
    "AthleteProfile",
    "PerformanceSignal",
    "ScoutSignal",
    "ReadinessSignal",
    "EvaluationResult",
    "SEREngine",
    "PGIEngine",
    "EdgeCareEngine",
    "LiveResumeBuilder",
    "DecisionEngine",
    "ScoutEdgePipeline",
]
