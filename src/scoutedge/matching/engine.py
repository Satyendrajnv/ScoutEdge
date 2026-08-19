"""
Squad Replacement & Opportunity Matching Engine Implementation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional

from scoutedge.models import AthleteProfile, EvaluationResult


@dataclass
class SquadNeedProfile:
    target_position: str
    min_se_r: float = 70.0
    min_pgi: float = 65.0
    max_injury_risk: str = "Moderate"  # Low, Moderate, High
    max_age_years: float = 27.0
    target_league_tier: str = "Tier-1"
    required_traits: List[str] = field(default_factory=list)


@dataclass
class CandidateMatchResult:
    athlete_id: str
    athlete_name: str
    primary_position: str
    current_team: str
    match_score: float             # 0.0 to 100.0
    gap_closure_percentage: float  # Percent of tactical needs fulfilled
    compatibility_tier: str       # High Fit, Tactical Fit, Secondary Target, Low Alignment
    evaluation: EvaluationResult
    match_reasons: List[str] = field(default_factory=list)


class OpportunityMatcher:
    """
    Opportunity Matcher

    Evaluates candidate athlete profiles and intelligence outputs against
    squad need profiles, producing ranked talent shortlists and match explainability.
    """

    def calculate_match_score(
        self, evaluation: EvaluationResult, squad_need: SquadNeedProfile, age_years: float = 22.0
    ) -> Tuple[float, float, List[str]]:
        """Calculates match score, gap closure %, and explainability drivers."""
        drivers = []
        score = 0.0

        # 1. Position Alignment (Must match or be primary sub-position)
        score += 25.0

        # 2. Performance Rating Match (SE-R)
        se_r_score = min(max((evaluation.se_r.overall_rating / max(squad_need.min_se_r, 50.0)) * 30.0, 0.0), 35.0)
        score += se_r_score
        if evaluation.se_r.overall_rating >= squad_need.min_se_r:
            drivers.append(f"Exceeds minimum SE-R™ rating requirement ({evaluation.se_r.overall_rating} >= {squad_need.min_se_r})")

        # 3. Growth Ceiling Match (PGI)
        pgi_score = min(max((evaluation.pgi.pgi_score / max(squad_need.min_pgi, 50.0)) * 20.0, 0.0), 25.0)
        score += pgi_score
        if evaluation.pgi.pgi_score >= squad_need.min_pgi:
            drivers.append(f"Strong PGI™ growth index alignment ({evaluation.pgi.pgi_score} >= {squad_need.min_pgi})")

        # 4. Workload Safety Check
        if evaluation.edgecare.injury_risk_category == "Low":
            score += 15.0
            drivers.append("Low workload injury risk profile (EdgeCare™)")
        elif evaluation.edgecare.injury_risk_category == "Moderate":
            score += 8.0
        else: # High Risk
            score -= 10.0
            drivers.append("Warning: High ACWR workload risk profile")

        # 5. Age Requirement
        if age_years <= squad_need.max_age_years:
            score += 5.0

        match_score = round(min(max(score, 0.0), 100.0), 2)
        gap_closure = round(min(match_score * 1.05, 100.0), 1)

        return match_score, gap_closure, drivers

    def rank_candidates(
        self,
        candidate_evaluations: List[Tuple[AthleteProfile, EvaluationResult, float]],
        squad_need: SquadNeedProfile,
    ) -> List[CandidateMatchResult]:
        """Ranks pool of candidate athletes against tactical squad need profile."""
        results: List[CandidateMatchResult] = []

        for profile, evaluation, age in candidate_evaluations:
            # Filter position if incompatible
            if squad_need.target_position.lower() not in profile.primary_position.lower():
                continue

            match_score, gap_closure, drivers = self.calculate_match_score(evaluation, squad_need, age)

            if match_score >= 80.0:
                tier = "High Priority Fit"
            elif match_score >= 70.0:
                tier = "Tactical Target"
            elif match_score >= 55.0:
                tier = "Secondary Option"
            else:
                tier = "Low Alignment"

            results.append(
                CandidateMatchResult(
                    athlete_id=profile.athlete_id,
                    athlete_name=profile.name,
                    primary_position=profile.primary_position,
                    current_team=profile.current_team,
                    match_score=match_score,
                    gap_closure_percentage=gap_closure,
                    compatibility_tier=tier,
                    evaluation=evaluation,
                    match_reasons=drivers,
                )
            )

        # Sort by match score descending
        results.sort(key=lambda r: r.match_score, reverse=True)
        return results


class SquadGapAnalyzer:
    """
    Squad Gap Analyzer

    Evaluates direct replacement targets for departing or injured starter players.
    """

    def __init__(self, matcher: Optional[OpportunityMatcher] = None):
        self.matcher = matcher or OpportunityMatcher()

    def find_replacements_for_player(
        self,
        departing_profile: AthleteProfile,
        departing_eval: EvaluationResult,
        candidate_pool: List[Tuple[AthleteProfile, EvaluationResult, float]],
    ) -> List[CandidateMatchResult]:
        """Finds and ranks candidate replacements to fill a specific departing player's gap."""
        need = SquadNeedProfile(
            target_position=departing_profile.primary_position,
            min_se_r=max(departing_eval.se_r.overall_rating * 0.9, 60.0),
            min_pgi=max(departing_eval.pgi.pgi_score * 0.85, 55.0),
            max_injury_risk="Moderate",
            max_age_years=28.0,
            target_league_tier=departing_profile.league_tier,
        )

        return self.matcher.rank_candidates(candidate_pool, need)
