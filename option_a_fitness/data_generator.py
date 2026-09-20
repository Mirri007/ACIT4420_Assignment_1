"""Simulated data for the Smart Fitness Session Analyzer assignment.

This module deliberately returns raw dictionaries and lists. It does not define
the student's domain classes, perform classification, or reveal target labels.
"""

import random


FITNESS_SCENARIOS = (
    "resting",
    "moderate_activity",
    "high_activity",
    "recovery",
    "poor_quality",
)


def _clamp(value, lower, upper):
    return max(lower, min(upper, value))


def _rounded(value, digits=2):
    return round(value, digits)


def available_scenarios():
    """Return the documented scenario names."""
    return FITNESS_SCENARIOS


def generate_fitness_data(
    participant_id="P001",
    scenario="random",
    seed=None,
    number_of_windows=12,
):
    """Return ``(participant_profile, observations)``.

    Parameters
    ----------
    participant_id : str
        Identifier included in the generated participant profile.
    scenario : str
        One of the names returned by :func:`available_scenarios`, or ``random``.
    seed : int or None
        Repeating a call with the same arguments and seed reproduces the data.
    number_of_windows : int
        Number of observation dictionaries to generate (minimum 6).
    """
    if not isinstance(participant_id, str) or not participant_id.strip():
        raise ValueError("participant_id must be a non-empty string")
    if not isinstance(number_of_windows, int) or number_of_windows < 6:
        raise ValueError("number_of_windows must be an integer of at least 6")

    rng = random.Random(seed)
    if scenario == "random":
        scenario = rng.choice(FITNESS_SCENARIOS)
    if scenario not in FITNESS_SCENARIOS:
        choices = ", ".join(FITNESS_SCENARIOS)
        raise ValueError("Unknown scenario. Choose from: " + choices)

    baseline_hr = rng.randint(58, 82)
    baseline_skin = rng.uniform(1.0, 2.5)
    baseline_temperature = rng.uniform(31.5, 33.2)

    profile = {
        "participant_id": participant_id,
        "baseline_heart_rate": baseline_hr,
        "baseline_skin_response": _rounded(baseline_skin),
        "baseline_temperature": _rounded(baseline_temperature),
    }

    observations = []
    for timestamp in range(number_of_windows):
        progress = timestamp / (number_of_windows - 1)

        if scenario == "resting":
            hr_offset = rng.gauss(2, 3)
            activity = rng.uniform(0.03, 0.20)
            skin_offset = rng.gauss(0.03, 0.08)
            temperature_offset = rng.gauss(0, 0.08)
        elif scenario == "moderate_activity":
            hr_offset = rng.gauss(28, 6)
            activity = rng.uniform(0.38, 0.66)
            skin_offset = rng.gauss(0.35, 0.12)
            temperature_offset = rng.gauss(0.25, 0.10)
        elif scenario == "high_activity":
            hr_offset = rng.gauss(58, 9)
            activity = rng.uniform(0.68, 0.95)
            skin_offset = rng.gauss(0.65, 0.18)
            temperature_offset = rng.gauss(0.55, 0.15)
        elif scenario == "recovery":
            # Measurements begin high and trend toward the personal baseline.
            decline = 1.0 - progress
            hr_offset = rng.gauss(8 + 55 * decline, 4)
            activity = _clamp(rng.gauss(0.10 + 0.75 * decline, 0.05), 0, 1)
            skin_offset = rng.gauss(0.08 + 0.55 * decline, 0.10)
            temperature_offset = rng.gauss(0.05 + 0.45 * decline, 0.08)
        else:  # poor_quality
            hr_offset = rng.gauss(20, 18)
            activity = rng.uniform(0.05, 0.85)
            skin_offset = rng.gauss(0.25, 0.25)
            temperature_offset = rng.gauss(0.15, 0.25)

        observation = {
            "timestamp": timestamp,
            "heart_rate": int(round(_clamp(baseline_hr + hr_offset, 35, 205))),
            "skin_response": _rounded(max(0, baseline_skin + skin_offset)),
            "temperature": _rounded(_clamp(baseline_temperature + temperature_offset, 25, 42)),
            "activity_level": _rounded(_clamp(activity, 0, 1)),
            "signal_quality": _rounded(rng.uniform(0.82, 0.99)),
        }

        if scenario == "poor_quality":
            observation["signal_quality"] = _rounded(rng.uniform(0.05, 0.55))
            # Include different realistic data-quality problems.
            issue = timestamp % 4
            if issue == 0:
                observation["heart_rate"] = None
            elif issue == 1:
                observation["heart_rate"] = 265
            elif issue == 2:
                observation["activity_level"] = -0.20
            else:
                observation["skin_response"] = None

        observations.append(observation)

    return profile, observations

