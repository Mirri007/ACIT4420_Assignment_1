"""Example usage for the Smart Fitness Session Analyzer.

This script demonstrates the normal workflow: generate a scenario, create an
analyzer instance, and print a human-readable session report.
"""

from data_generator import available_scenarios, generate_fitness_data
from fitness_analyzer import FitnessSessionAnalyzer


def main():
    # Show all supported scenarios before running the analysis.
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
    print("\nSession report")
    print(analyzer.generate_report())


if __name__ == "__main__":
    main()

