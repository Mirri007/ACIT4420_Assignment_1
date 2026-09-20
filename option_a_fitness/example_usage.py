"""Example usage for the Smart Fitness Session Analyzer."""

from data_generator import available_scenarios, generate_fitness_data
from fitness_analyzer import FitnessSessionAnalyzer


def main():
    print("Available scenarios:", available_scenarios())

    profile, observations = generate_fitness_data(
        participant_id="P001",
        scenario="recovery",
        seed=42,
        number_of_windows=10,
    )

    analyzer = FitnessSessionAnalyzer(profile, observations)
    print("\nParticipant profile")
    print(profile)
    print("\nSession summary")
    print(analyzer.session_summary)
    print("\nRejected observations")
    print(analyzer.rejected_observations)


if __name__ == "__main__":
    main()

