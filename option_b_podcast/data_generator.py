"""Simulated data for the Podcast Voice and Recording Analyzer assignment.

The returned values represent features that another system has already extracted
from speech. This module contains no recordings, transcripts, classification, or
target labels.
"""

import random


RECORDING_SCENARIOS = (
    "consistent",
    "energetic",
    "deliberate",
    "noise_affected",
    "insufficient_data",
)


def _clamp(value, lower, upper):
    return max(lower, min(upper, value))


def _rounded(value, digits=2):
    return round(value, digits)


def available_scenarios():
    """Return the documented scenario names."""
    return RECORDING_SCENARIOS


def generate_recording_data(
    speaker_id="SP001",
    scenario="random",
    seed=None,
    number_of_windows=12,
):
    """Return ``(speaker_profile, observations)`` as dictionaries and a list."""
    if not isinstance(speaker_id, str) or not speaker_id.strip():
        raise ValueError("speaker_id must be a non-empty string")
    if not isinstance(number_of_windows, int) or number_of_windows < 6:
        raise ValueError("number_of_windows must be an integer of at least 6")

    rng = random.Random(seed)
    if scenario == "random":
        scenario = rng.choice(RECORDING_SCENARIOS)
    if scenario not in RECORDING_SCENARIOS:
        choices = ", ".join(RECORDING_SCENARIOS)
        raise ValueError("Unknown scenario. Choose from: " + choices)

    usual_pitch = rng.uniform(105, 205)
    usual_energy = rng.uniform(0.25, 0.50)
    usual_rate = rng.randint(95, 145)
    usual_pause = rng.uniform(0.18, 0.36)

    profile = {
        "speaker_id": speaker_id,
        "usual_pitch": _rounded(usual_pitch, 1),
        "usual_energy": _rounded(usual_energy),
        "usual_speech_rate": usual_rate,
        "usual_pause_ratio": _rounded(usual_pause),
    }

    observations = []
    for timestamp in range(number_of_windows):
        speech_present = True
        noise = rng.uniform(0.04, 0.18)
        quality = rng.uniform(0.84, 0.99)

        if scenario == "consistent":
            pitch = rng.gauss(usual_pitch, 4)
            energy = rng.gauss(usual_energy, 0.025)
            speech_rate = rng.gauss(usual_rate, 4)
            pause_ratio = rng.gauss(usual_pause, 0.025)
        elif scenario == "energetic":
            pitch = rng.gauss(usual_pitch * 1.13, 6)
            energy = rng.gauss(usual_energy + 0.18, 0.04)
            speech_rate = rng.gauss(usual_rate + 22, 6)
            pause_ratio = rng.gauss(usual_pause - 0.09, 0.025)
        elif scenario == "deliberate":
            pitch = rng.gauss(usual_pitch * 0.97, 5)
            energy = rng.gauss(usual_energy - 0.06, 0.035)
            speech_rate = rng.gauss(usual_rate - 25, 5)
            pause_ratio = rng.gauss(usual_pause + 0.16, 0.035)
        elif scenario == "noise_affected":
            pitch = rng.gauss(usual_pitch * 1.07, 10)
            energy = rng.gauss(usual_energy + 0.20, 0.06)
            speech_rate = rng.gauss(usual_rate + 8, 8)
            pause_ratio = rng.gauss(usual_pause, 0.06)
            noise = rng.uniform(0.68, 0.96)
            quality = rng.uniform(0.38, 0.72)
        else:  # insufficient_data
            pitch = rng.gauss(usual_pitch, 12)
            energy = rng.gauss(usual_energy, 0.08)
            speech_rate = rng.gauss(usual_rate, 14)
            pause_ratio = rng.gauss(usual_pause, 0.10)
            speech_present = timestamp % 3 == 0
            quality = rng.uniform(0.05, 0.52)
            noise = rng.uniform(0.25, 0.90)

        observation = {
            "timestamp": timestamp,
            "speech_present": speech_present,
            "pitch": _rounded(_clamp(pitch, 45, 450), 1),
            "energy": _rounded(_clamp(energy, 0, 1)),
            "speech_rate": int(round(_clamp(speech_rate, 30, 260))),
            "pause_ratio": _rounded(_clamp(pause_ratio, 0, 1)),
            "background_noise": _rounded(_clamp(noise, 0, 1)),
            "signal_quality": _rounded(_clamp(quality, 0, 1)),
        }

        if not speech_present:
            observation["pitch"] = None
            observation["energy"] = None
            observation["speech_rate"] = None
            observation["pause_ratio"] = None
        elif scenario == "insufficient_data" and timestamp % 4 == 0:
            # A deliberately invalid ratio tests student validation.
            observation["pause_ratio"] = 1.25

        observations.append(observation)

    return profile, observations

