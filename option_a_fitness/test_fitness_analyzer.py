import unittest

from fitness_analyzer import FitnessSessionAnalyzer
from data_generator import generate_fitness_data


class FitnessSessionAnalyzerTests(unittest.TestCase):
    def test_recovery_session_is_classified_as_recovery(self):
        profile, observations = generate_fitness_data(
            participant_id="P010",
            scenario="recovery",
            seed=7,
            number_of_windows=10,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(result.session_summary["classification"], "recovery")
        self.assertGreater(len(result.valid_observations), 0)

    def test_poor_quality_session_flags_invalid_points(self):
        profile, observations = generate_fitness_data(
            participant_id="P021",
            scenario="poor_quality",
            seed=3,
            number_of_windows=8,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(result.session_summary["classification"], "poor_quality")
        self.assertGreater(result.session_summary["rejected_observations"], 0)


if __name__ == "__main__":
    unittest.main()
