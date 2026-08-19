"""
ScoutEdge REST API Request & Response Serializers
"""

from typing import Dict, List, Any
from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
    EvaluationResult,
    SERRatingOutput,
    PGIOutput,
    EdgeCareOutput,
)


def serialize_evaluation_result(result: EvaluationResult) -> Dict[str, Any]:
    """Serializes EvaluationResult object into JSON-compatible dictionary."""
    return {
        "athlete_id": result.athlete_id,
        "timestamp": result.timestamp,
        "fit_score": result.fit_score,
        "recommendation": result.recommendation,
        "explainability_reasons": result.explainability_reasons,
        "se_r": {
            "overall_rating": result.se_r.overall_rating,
            "technical_rating": result.se_r.technical_rating,
            "physical_rating": result.se_r.physical_rating,
            "tactical_rating": result.se_r.tactical_rating,
            "confidence_score": result.se_r.confidence_score,
            "percentile_rank": result.se_r.percentile_rank,
            "key_drivers": result.se_r.key_drivers,
        },
        "pgi": {
            "pgi_score": result.pgi.pgi_score,
            "progression_velocity": result.pgi.progression_velocity,
            "growth_ceiling_projection": result.pgi.growth_ceiling_projection,
            "development_stage": result.pgi.development_stage,
            "growth_factors": result.pgi.growth_factors,
        },
        "edgecare": {
            "readiness_index": result.edgecare.readiness_index,
            "acwr_ratio": result.edgecare.acwr_ratio,
            "injury_risk_category": result.edgecare.injury_risk_category,
            "recommended_minutes": result.edgecare.recommended_minutes,
            "sustainability_score": result.edgecare.sustainability_score,
        },
        "live_resume": {
            "athlete_id": result.live_resume.athlete_id,
            "generated_at": result.live_resume.generated_at,
            "version": result.live_resume.version,
            "overall_se_r": result.live_resume.overall_se_r,
            "current_pgi": result.live_resume.current_pgi,
            "current_readiness": result.live_resume.current_readiness,
            "verified_milestones": result.live_resume.verified_milestones,
            "career_trajectory_summary": result.live_resume.career_trajectory_summary,
        },
    }


def parse_athlete_profile(data: Dict[str, Any]) -> AthleteProfile:
    """Parses JSON dictionary into AthleteProfile model."""
    return AthleteProfile(
        athlete_id=data.get("athlete_id", "ath_unknown"),
        name=data.get("name", "Unknown Athlete"),
        sport=data.get("sport", "General Sports"),
        primary_position=data.get("primary_position", "General"),
        birth_date=data.get("birth_date", "2000-01-01"),
        height_cm=float(data.get("height_cm", 180.0)),
        weight_kg=float(data.get("weight_kg", 75.0)),
        current_team=data.get("current_team", "Free Agent"),
        league_tier=data.get("league_tier", "Tier-1"),
    )


def parse_performance_signals(signals_data: List[Dict[str, Any]]) -> List[PerformanceSignal]:
    """Parses list of dictionaries into PerformanceSignal objects."""
    result = []
    for d in signals_data:
        result.append(
            PerformanceSignal(
                signal_id=d.get("signal_id", "sig_p"),
                athlete_id=d.get("athlete_id", ""),
                timestamp=d.get("timestamp", ""),
                match_id=d.get("match_id", "m1"),
                minutes_played=int(d.get("minutes_played", 90)),
                raw_stats=d.get("raw_stats", {}),
                opponent_tier_weight=float(d.get("opponent_tier_weight", 1.0)),
            )
        )
    return result


def parse_scout_signals(signals_data: List[Dict[str, Any]]) -> List[ScoutSignal]:
    """Parses list of dictionaries into ScoutSignal objects."""
    result = []
    for d in signals_data:
        result.append(
            ScoutSignal(
                signal_id=d.get("signal_id", "sig_s"),
                athlete_id=d.get("athlete_id", ""),
                scout_id=d.get("scout_id", "scout"),
                timestamp=d.get("timestamp", ""),
                technical_score=float(d.get("technical_score", 50.0)),
                tactical_score=float(d.get("tactical_score", 50.0)),
                physical_score=float(d.get("physical_score", 50.0)),
                mental_score=float(d.get("mental_score", 50.0)),
                qualitative_notes=d.get("qualitative_notes", ""),
            )
        )
    return result


def parse_readiness_signals(signals_data: List[Dict[str, Any]]) -> List[ReadinessSignal]:
    """Parses list of dictionaries into ReadinessSignal objects."""
    result = []
    for d in signals_data:
        result.append(
            ReadinessSignal(
                signal_id=d.get("signal_id", "sig_r"),
                athlete_id=d.get("athlete_id", ""),
                timestamp=d.get("timestamp", ""),
                acute_workload_7d=float(d.get("acute_workload_7d", 300.0)),
                chronic_workload_28d=float(d.get("chronic_workload_28d", 1200.0)),
                sleep_quality_score=float(d.get("sleep_quality_score", 80.0)),
                fatigue_level=float(d.get("fatigue_level", 20.0)),
                availability_status=d.get("availability_status", "Available"),
            )
        )
    return result
