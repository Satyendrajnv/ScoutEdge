"""
Unit Tests for ScoutEdge Squad Replacement & Opportunity Matching Subsystem
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.models import (
    AthleteProfile,
    PerformanceSignal,
    ScoutSignal,
    ReadinessSignal,
)
from scoutedge.core.pipeline import ScoutEdgePipeline
from scoutedge.matching.engine import (
    SquadNeedProfile,
    OpportunityMatcher,
    SquadGapAnalyzer,
)


class TestOpportunityMatching(unittest.TestCase):
    def setUp(self):
        self.pipeline = ScoutEdgePipeline()
        self.matcher = OpportunityMatcher()
        self.gap_analyzer = SquadGapAnalyzer(self.matcher)

        # Candidate 1: High Quality Midfielder
        self.prof1 = AthleteProfile(
            athlete_id="ath_m1",
            name="Lucas Paqueta",
            sport="Soccer",
            primary_position="Attacking Midfield",
            birth_date="2003-01-01",
            height_cm=180.0,
            weight_kg=75.0,
            current_team="Capital City FC",
        )
        eval1 = self.pipeline.process_athlete(
            self.prof1,
            [PerformanceSignal("p1", "ath_m1", "2026-08-01", "m1", 90, {"key_passes": 92.0})],
            [ScoutSignal("s1", "ath_m1", "sc1", "2026-08-01", 90.0, 88.0, 85.0, 89.0)],
            [ReadinessSignal("r1", "ath_m1", "2026-08-18", 320.0, 1280.0, 90.0, 15.0)],
            age_years=23.5,
        )

        # Candidate 2: Secondary Midfielder
        self.prof2 = AthleteProfile(
            athlete_id="ath_m2",
            name="Ethan Vance",
            sport="Soccer",
            primary_position="Attacking Midfield",
            birth_date="2005-01-01",
            height_cm=176.0,
            weight_kg=70.0,
            current_team="Reserve FC",
        )
        eval2 = self.pipeline.process_athlete(
            self.prof2,
            [PerformanceSignal("p2", "ath_m2", "2026-08-01", "m1", 90, {"key_passes": 70.0})],
            [ScoutSignal("s2", "ath_m2", "sc1", "2026-08-01", 72.0, 70.0, 75.0, 72.0)],
            [ReadinessSignal("r2", "ath_m2", "2026-08-18", 300.0, 1200.0, 80.0, 25.0)],
            age_years=21.0,
        )

        # Candidate 3: Defender (Incompatible Position)
        self.prof3 = AthleteProfile(
            athlete_id="ath_d1",
            name="Ruben Dias",
            sport="Soccer",
            primary_position="Center Back",
            birth_date="2001-01-01",
            height_cm=187.0,
            weight_kg=82.0,
            current_team="Defense FC",
        )
        eval3 = self.pipeline.process_athlete(
            self.prof3,
            [PerformanceSignal("p3", "ath_d1", "2026-08-01", "m1", 90, {"tackles": 90.0})],
            [ScoutSignal("s3", "ath_d1", "sc1", "2026-08-01", 85.0, 88.0, 90.0, 88.0)],
            [ReadinessSignal("r3", "ath_d1", "2026-08-18", 350.0, 1400.0, 85.0, 20.0)],
            age_years=25.0,
        )

        self.candidate_pool = [
            (self.prof1, eval1, 23.5),
            (self.prof2, eval2, 21.0),
            (self.prof3, eval3, 25.0),
        ]

    def test_rank_candidates(self):
        squad_need = SquadNeedProfile(
            target_position="Attacking Midfield",
            min_se_r=75.0,
            min_pgi=65.0,
            max_age_years=26.0,
        )

        shortlist = self.matcher.rank_candidates(self.candidate_pool, squad_need)

        # Defender should be filtered out
        self.assertEqual(len(shortlist), 2)
        # Top candidate should be Lucas Paqueta
        self.assertEqual(shortlist[0].athlete_name, "Lucas Paqueta")
        self.assertGreater(shortlist[0].match_score, shortlist[1].match_score)
        self.assertEqual(shortlist[0].compatibility_tier, "High Priority Fit")

    def test_squad_gap_analyzer(self):
        departing_profile, departing_eval, age = self.candidate_pool[0]
        replacements = self.gap_analyzer.find_replacements_for_player(
            departing_profile, departing_eval, self.candidate_pool
        )
        self.assertGreater(len(replacements), 0)
        self.assertEqual(replacements[0].primary_position, "Attacking Midfield")


if __name__ == "__main__":
    unittest.main()
