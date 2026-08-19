"""
Synthetic Data Generator for ScoutEdge Athlete Cohorts
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)

POSITIONS = ["Attacking Midfield", "Central Midfield", "Striker", "Winger", "Center Back", "Full Back", "Goalkeeper"]
TEAMS = ["Apex Youth Academy", "ScoutEdge United", "Metro Sports FC", "Catalyst Athletic", "Vanguard City"]
LEAGUES = ["U19 Elite League", "U21 National Division", "Division 2 Professional", "Premier League Reserve"]

FIRST_NAMES = ["Julian", "Marcus", "Lucas", "Mateo", "Gabriel", "Kylian", "Liam", "Noah", "Oliver", "Ethan"]
LAST_NAMES = ["Vance", "Solanke", "Silva", "Rashford", "Bellingham", "Pedri", "Haaland", "Saka", "Musiala", "Wirtz"]


class SyntheticDataGenerator:
    """
    Generates synthetic athlete profiles, multi-match performance statistics,
    scout observation notes, and readiness signals with natural random variance.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def generate_athlete(self, athlete_index: int) -> Tuple[AthleteProfile, float]:
        """Generates single random athlete profile and age in years."""
        first = self.rng.choice(FIRST_NAMES)
        last = self.rng.choice(LAST_NAMES)
        name = f"{first} {last}_{athlete_index}"
        pos = self.rng.choice(POSITIONS)
        team = self.rng.choice(TEAMS)
        league = self.rng.choice(LEAGUES)

        # Birth date generation (Age 17 to 28)
        age_years = round(self.rng.uniform(17.0, 28.5), 1)
        birth_year = 2026 - int(age_years)
        birth_month = self.rng.randint(1, 12)
        birth_day = self.rng.randint(1, 28)
        birth_date = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"

        height = round(self.rng.uniform(172.0, 194.0), 1)
        weight = round(self.rng.uniform(68.0, 88.0), 1)

        profile = AthleteProfile(
            athlete_id=f"ath_synth_{athlete_index:04d}",
            name=name,
            sport="Soccer",
            primary_position=pos,
            birth_date=birth_date,
            height_cm=height,
            weight_kg=weight,
            current_team=team,
            league_tier=league,
        )
        return profile, age_years

    def generate_signals(
        self, athlete_id: str, num_matches: int = 3
    ) -> Tuple[List[PerformanceSignal], List[ScoutSignal], List[ReadinessSignal]]:
        """Generates historical performance, scout observation, and readiness signals."""
        perf_signals = []
        scout_signals = []
        readiness_signals = []

        base_date = datetime(2026, 8, 1)

        for m in range(num_matches):
            match_date = (base_date + timedelta(days=m * 7)).strftime("%Y-%m-%d")

            # Performance stats
            perf = PerformanceSignal(
                signal_id=f"p_sig_{athlete_id}_{m}",
                athlete_id=athlete_id,
                timestamp=match_date,
                match_id=f"m_{m+100}",
                minutes_played=self.rng.randint(65, 90),
                raw_stats={
                    "pass_accuracy": round(self.rng.uniform(70.0, 95.0), 1),
                    "tackles_won": round(self.rng.uniform(60.0, 90.0), 1),
                    "key_passes": round(self.rng.uniform(50.0, 92.0), 1),
                },
                opponent_tier_weight=round(self.rng.uniform(0.9, 1.25), 2),
            )
            perf_signals.append(perf)

            # Scout signals
            scout = ScoutSignal(
                signal_id=f"s_sig_{athlete_id}_{m}",
                athlete_id=athlete_id,
                scout_id=f"scout_{self.rng.randint(1, 10)}",
                timestamp=match_date,
                technical_score=round(self.rng.uniform(60.0, 95.0), 1),
                tactical_score=round(self.rng.uniform(60.0, 95.0), 1),
                physical_score=round(self.rng.uniform(65.0, 95.0), 1),
                mental_score=round(self.rng.uniform(60.0, 95.0), 1),
                qualitative_notes="Demonstrates strong tactical adaptability and physical workrate.",
            )
            scout_signals.append(scout)

        # Readiness signal (last 7/28 days)
        acute = round(self.rng.uniform(280.0, 450.0), 1)
        chronic = round(acute * self.rng.uniform(3.5, 4.5), 1)  # ACWR ratio around 0.9 - 1.2
        readiness = ReadinessSignal(
            signal_id=f"r_sig_{athlete_id}",
            athlete_id=athlete_id,
            timestamp=datetime(2026, 8, 18).strftime("%Y-%m-%d"),
            acute_workload_7d=acute,
            chronic_workload_28d=chronic,
            sleep_quality_score=round(self.rng.uniform(70.0, 98.0), 1),
            fatigue_level=round(self.rng.uniform(10.0, 35.0), 1),
            availability_status="Available",
        )
        readiness_signals.append(readiness)

        return perf_signals, scout_signals, readiness_signals

    def generate_cohort(
        self, count: int = 1000, num_matches_per_athlete: int = 3
    ) -> List[Dict[str, Any]]:
        """Generates cohort of synthetic athlete datasets."""
        cohort = []
        for i in range(1, count + 1):
            profile, age = self.generate_athlete(i)
            perf, scout, readiness = self.generate_signals(profile.athlete_id, num_matches_per_athlete)
            cohort.append(
                {
                    "profile": profile,
                    "age_years": age,
                    "performance_signals": perf,
                    "scout_signals": scout,
                    "readiness_signals": readiness,
                }
            )
        return cohort
