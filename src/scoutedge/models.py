"""
Core Data Contracts and Signal Schemas for ScoutEdge
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional


@dataclass
class AthleteProfile:
    athlete_id: str
    name: str
    sport: str
    primary_position: str
    birth_date: str
    height_cm: float
    weight_kg: float
    current_team: str
    league_tier: str = "Tier-1"


@dataclass
class PerformanceSignal:
    signal_id: str
    athlete_id: str
    timestamp: str
    match_id: str
    minutes_played: int
    raw_stats: Dict[str, float] = field(default_factory=dict)
    opponent_tier_weight: float = 1.0


@dataclass
class ScoutSignal:
    signal_id: str
    athlete_id: str
    scout_id: str
    timestamp: str
    technical_score: float  # Scale 1-100
    tactical_score: float   # Scale 1-100
    physical_score: float   # Scale 1-100
    mental_score: float     # Scale 1-100
    qualitative_notes: str = ""


@dataclass
class ReadinessSignal:
    signal_id: str
    athlete_id: str
    timestamp: str
    acute_workload_7d: float
    chronic_workload_28d: float
    sleep_quality_score: float  # Scale 0-100
    fatigue_level: float        # Scale 0-100
    availability_status: str = "Available"  # Available, Limited, Out


@dataclass
class SERRatingOutput:
    overall_rating: float       # Scale 0-100
    technical_rating: float
    physical_rating: float
    tactical_rating: float
    confidence_score: float
    percentile_rank: float
    key_drivers: List[str] = field(default_factory=list)


@dataclass
class PGIOutput:
    pgi_score: float            # Scale 0-100
    progression_velocity: float # Rate of growth over period
    growth_ceiling_projection: float
    development_stage: str       # Early, Emerging, Peak, Elite
    growth_factors: List[str] = field(default_factory=list)


@dataclass
class EdgeCareOutput:
    readiness_index: float      # Scale 0-100
    acwr_ratio: float           # Acute:Chronic Workload Ratio
    injury_risk_category: str   # Low, Moderate, High
    recommended_minutes: int
    sustainability_score: float


@dataclass
class LiveResumeRecord:
    athlete_id: str
    generated_at: str
    version: str
    overall_se_r: float
    current_pgi: float
    current_readiness: float
    verified_milestones: List[Dict[str, str]] = field(default_factory=list)
    career_trajectory_summary: str = ""


@dataclass
class EvaluationResult:
    athlete_id: str
    timestamp: str
    se_r: SERRatingOutput
    pgi: PGIOutput
    edgecare: EdgeCareOutput
    live_resume: LiveResumeRecord
    fit_score: float            # Overall recommendation score 0-100
    recommendation: str         # Sign, Monitor, Develop, Pass
    explainability_reasons: List[str] = field(default_factory=list)
