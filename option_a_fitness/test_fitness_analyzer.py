import unittest

from fitness_analyzer import FitnessSessionAnalyzer
from data_generator import generate_fitness_data


# These tests cover the required exercise scenarios and verify that the session
# is classified correctly based on realistic input patterns.
class FitnessSessionAnalyzerTests(unittest.TestCase):
    def test_resting_session_is_classified_as_resting(self):
        profile, observations = generate_fitness_data(
            participant_id="P010",
            scenario="resting",
            seed=11,
            number_of_windows=10,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(
            result.session_summary["classification"],
            "resting",
            "Resting data should remain near the participant baseline.",
        )
        self.assertGreater(len(result.valid_observations), 0)

    def test_moderate_activity_session_is_classified_as_moderate_activity(self):
        profile, observations = generate_fitness_data(
            participant_id="P011",
            scenario="moderate_activity",
            seed=17,
            number_of_windows=10,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(
            result.session_summary["classification"],
            "moderate_activity",
            "Moderate activity should produce a middle-range classification.",
        )
        self.assertGreater(len(result.valid_observations), 0)

    def test_high_activity_session_is_classified_as_high_activity(self):
        profile, observations = generate_fitness_data(
            participant_id="P012",
            scenario="high_activity",
            seed=23,
            number_of_windows=10,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(
            result.session_summary["classification"],
            "high_activity",
            "High activity should be classified as sustained high exertion.",
        )
        self.assertGreater(len(result.valid_observations), 0)

    def test_recovery_session_is_classified_as_recovery(self):
        profile, observations = generate_fitness_data(
            participant_id="P013",
            scenario="recovery",
            seed=7,
            number_of_windows=10,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(
            result.session_summary["classification"],
            "recovery",
            "Recovery should be detected when heart rate and activity fall toward baseline.",
        )
        self.assertGreater(len(result.valid_observations), 0)

    def test_poor_quality_session_flags_invalid_points(self):
        profile, observations = generate_fitness_data(
            participant_id="P021",
            scenario="poor_quality",
            seed=3,
            number_of_windows=8,
        )

        result = FitnessSessionAnalyzer(profile, observations)
        self.assertEqual(
            result.session_summary["classification"],
            "poor_quality",
            "Poor-quality data should be rejected if too many observations are invalid.",
        )
        self.assertGreater(result.session_summary["rejected_observations"], 0)


if __name__ == "__main__":
    unittest.main()
