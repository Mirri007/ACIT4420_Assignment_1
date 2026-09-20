"""Minimal demonstration of the instructor-supplied recording generator."""

from data_generator import available_scenarios, generate_recording_data


def main():
    print("Available scenarios:", available_scenarios())

    profile, observations = generate_recording_data(
        speaker_id="SP001",
        scenario="noise_affected",
        seed=42,
        number_of_windows=10,
    )

    print("\nSpeaker profile")
    print(profile)
    print("\nFirst three observations")
    for observation in observations[:3]:
        print(observation)

    # Your program should convert these dictionaries into your own objects,
    # validate them, analyze the complete session, and produce a report.


if __name__ == "__main__":
    main()

