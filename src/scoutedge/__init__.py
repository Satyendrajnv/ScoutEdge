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
from scoutedge.api.server import create_scoutedge_app
from scoutedge.tools.generator import SyntheticDataGenerator
from scoutedge.tools.benchmark import PipelineBenchmark
from scoutedge.cli.main import main as cli_main
from scoutedge.reports.exporter import ScoutReportExporter
from scoutedge.spatial.analyzer import PitchZoneAnalyzer, SpatialControlEngine
from scoutedge.matching.engine import (
    SquadNeedProfile,
    CandidateMatchResult,
    OpportunityMatcher,
    SquadGapAnalyzer,
)

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
    "create_scoutedge_app",
    "SyntheticDataGenerator",
    "PipelineBenchmark",
    "cli_main",
    "ScoutReportExporter",
    "PitchZoneAnalyzer",
    "SpatialControlEngine",
    "SquadNeedProfile",
    "CandidateMatchResult",
    "OpportunityMatcher",
    "SquadGapAnalyzer",
]
