"""
Spatial Tracking & Pitch Zonal Impact Analysis Implementation
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional

from scoutedge.models import PerformanceSignal

# Standard 18-Zone Pitch Grid Definition (3x6 Grid)
# Thirds: Defensive (0-33.3), Middle (33.3-66.6), Attacking (66.6-100)
# Channels: Left (0-20), Left-Halfspace (20-40), Center (40-60), Right-Halfspace (60-80), Right (80-100)

ZONES = {
    "D_L": "Defensive Left",
    "D_LH": "Defensive Left-Halfspace",
    "D_C": "Defensive Center",
    "D_RH": "Defensive Right-Halfspace",
    "D_R": "Defensive Right",
    "M_L": "Middle Left",
    "M_LH": "Middle Left-Halfspace",
    "M_C": "Middle Center",
    "M_RH": "Middle Right-Halfspace",
    "M_R": "Middle Right",
    "A_L": "Attacking Left",
    "A_LH": "Attacking Left-Halfspace",
    "A_C": "Attacking Center",
    "A_RH": "Attacking Right-Halfspace",
    "A_R": "Attacking Right",
    "BOX_D": "Defensive Penalty Box",
    "BOX_A": "Attacking Penalty Box",
    "HALF_LINE": "Halfway Control Line",
}


@dataclass
class SpatialEvent:
    event_id: str
    timestamp_sec: float
    x: float  # Normalized 0.0 to 100.0 (Pitch length: 0=Defensive Goal, 100=Attacking Goal)
    y: float  # Normalized 0.0 to 100.0 (Pitch width: 0=Left Touchline, 100=Right Touchline)
    event_type: str  # pass, dribble, shot, tackle, interception, reception
    success: bool = True
    end_x: Optional[float] = None
    end_y: Optional[float] = None


@dataclass
class SpatialMetrics:
    total_events: int
    zonal_occupancy: Dict[str, int]
    high_threat_zone_touches: int
    progressive_passing_distance_m: float
    dangerous_space_control_score: float  # Scale 0-100
    pressure_resistance_score: float       # Scale 0-100


class PitchZoneAnalyzer:
    """
    Pitch Zone Analyzer

    Classifies 2D event coordinates (x, y) into tactical pitch zones and penalty box zones.
    """

    @staticmethod
    def get_zone_code(x: float, y: float) -> str:
        """Determines tactical zone code for given normalized (x, y) coordinates."""
        x = min(max(x, 0.0), 100.0)
        y = min(max(y, 0.0), 100.0)

        # Check Attacking Box (x > 83.5, 21.1 < y < 78.9)
        if x > 83.5 and 21.1 < y < 78.9:
            return "BOX_A"

        # Check Defensive Box (x < 16.5, 21.1 < y < 78.9)
        if x < 16.5 and 21.1 < y < 78.9:
            return "BOX_D"

        # Determine Third
        if x < 33.3:
            third = "D"
        elif x < 66.6:
            third = "M"
        else:
            third = "A"

        # Determine Channel
        if y < 20.0:
            channel = "L"
        elif y < 40.0:
            channel = "LH"
        elif y < 60.0:
            channel = "C"
        elif y < 80.0:
            channel = "RH"
        else:
            channel = "R"

        return f"{third}_{channel}"


class SpatialControlEngine:
    """
    Spatial Control Engine

    Ingests spatial event streams and calculates tactical spatial metrics,
    dangerous space control scores, and converts tracking data into SE-R™ PerformanceSignals.
    """

    def __init__(self, pitch_length_m: float = 105.0, pitch_width_m: float = 68.0):
        self.pitch_length_m = pitch_length_m
        self.pitch_width_m = pitch_width_m
        self.analyzer = PitchZoneAnalyzer()

    def analyze_events(self, events: List[SpatialEvent]) -> SpatialMetrics:
        """Analyzes spatial event streams to derive tactical spatial metrics."""
        if not events:
            return SpatialMetrics(
                total_events=0,
                zonal_occupancy={},
                high_threat_zone_touches=0,
                progressive_passing_distance_m=0.0,
                dangerous_space_control_score=50.0,
                pressure_resistance_score=50.0,
            )

        zonal_counts: Dict[str, int] = {}
        high_threat_touches = 0
        total_progression_m = 0.0
        successful_events = 0

        for ev in events:
            zone = self.analyzer.get_zone_code(ev.x, ev.y)
            zonal_counts[zone] = zonal_counts.get(zone, 0) + 1

            if ev.success:
                successful_events += 1

            # High threat zones: Attacking Halfspaces, Attacking Center, Attacking Box
            if zone in ["BOX_A", "A_C", "A_LH", "A_RH"]:
                high_threat_touches += 1

            # Progressive distance calculation for passes/dribbles
            if ev.end_x is not None and ev.end_x > ev.x:
                dx_m = ((ev.end_x - ev.x) / 100.0) * self.pitch_length_m
                total_progression_m += dx_m

        # Dangerous space control score computation (0-100)
        high_threat_ratio = high_threat_touches / max(len(events), 1)
        danger_score = min(max((high_threat_ratio * 150.0) + (total_progression_m * 0.1), 0.0), 100.0)

        # Pressure resistance score (0-100)
        success_rate = (successful_events / max(len(events), 1)) * 100.0
        pressure_score = min(max((success_rate * 0.7) + (danger_score * 0.3), 0.0), 100.0)

        return SpatialMetrics(
            total_events=len(events),
            zonal_occupancy=zonal_counts,
            high_threat_zone_touches=high_threat_touches,
            progressive_passing_distance_m=round(total_progression_m, 2),
            dangerous_space_control_score=round(danger_score, 2),
            pressure_resistance_score=round(pressure_score, 2),
        )

    def convert_to_performance_signal(
        self,
        athlete_id: str,
        match_id: str,
        timestamp: str,
        events: List[SpatialEvent],
        opponent_tier_weight: float = 1.0,
    ) -> PerformanceSignal:
        """Converts spatial metrics into SE-R™ compatible PerformanceSignal object."""
        metrics = self.analyze_events(events)

        raw_stats = {
            "spatial_control_score": metrics.dangerous_space_control_score,
            "pressure_resistance_score": metrics.pressure_resistance_score,
            "high_threat_touches": float(metrics.high_threat_zone_touches),
            "progressive_distance_m": metrics.progressive_passing_distance_m,
        }

        return PerformanceSignal(
            signal_id=f"sig_spatial_{match_id}_{athlete_id}",
            athlete_id=athlete_id,
            timestamp=timestamp,
            match_id=match_id,
            minutes_played=90,
            raw_stats=raw_stats,
            opponent_tier_weight=opponent_tier_weight,
        )
