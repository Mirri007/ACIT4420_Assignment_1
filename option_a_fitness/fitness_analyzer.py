"""Domain objects and analysis for the Smart Fitness Session Analyzer."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean


@dataclass(frozen=True)
class ParticipantProfile:
    participant_id: str
    baseline_heart_rate: int
    baseline_skin_response: float
    baseline_temperature: float

    @classmethod
    def from_dict(cls, raw_profile):
        if not isinstance(raw_profile, dict):
            raise TypeError("profile must be a dictionary")

        participant_id = raw_profile.get("participant_id")
        baseline_heart_rate = raw_profile.get("baseline_heart_rate")
        baseline_skin_response = raw_profile.get("baseline_skin_response")
        baseline_temperature = raw_profile.get("baseline_temperature")

        if not isinstance(participant_id, str) or not participant_id.strip():
            raise ValueError("participant_id must be a non-empty string")
        if not isinstance(baseline_heart_rate, int) or baseline_heart_rate <= 0:
            raise ValueError("baseline_heart_rate must be a positive integer")
        if not isinstance(baseline_skin_response, (int, float)):
            raise ValueError("baseline_skin_response must be numeric")
        if not isinstance(baseline_temperature, (int, float)):
            raise ValueError("baseline_temperature must be numeric")

        return cls(
            participant_id=participant_id,
            baseline_heart_rate=baseline_heart_rate,
            baseline_skin_response=float(baseline_skin_response),
            baseline_temperature=float(baseline_temperature),
        )


@dataclass
class FitnessObservation:
    timestamp: int
    heart_rate: float
    skin_response: float
    temperature: float
    activity_level: float
    signal_quality: float
    issues: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw_observation):
        if not isinstance(raw_observation, dict):
            raise TypeError("observation must be a dictionary")

        return cls(
            timestamp=raw_observation.get("timestamp"),
            heart_rate=raw_observation.get("heart_rate"),
            skin_response=raw_observation.get("skin_response"),
            temperature=raw_observation.get("temperature"),
            activity_level=raw_observation.get("activity_level"),
            signal_quality=raw_observation.get("signal_quality"),
        )

    @property
    def is_valid(self):
        return not self.issues


class FitnessSessionAnalyzer:
    """Validate one fitness session and infer the session type."""

    def __init__(self, profile, observations):
        self.profile = ParticipantProfile.from_dict(profile)
        self.raw_observations = list(observations)
        self.valid_observations = []
        self.rejected_observations = []

        for raw_observation in self.raw_observations:
            observation = FitnessObservation.from_dict(raw_observation)
            issues = self._validate_observation(observation)
            observation.issues = issues
            if issues:
                self.rejected_observations.append(observation)
            else:
                self.valid_observations.append(observation)

        self.session_summary = self._build_summary()

    @staticmethod
    def _is_number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def _validate_observation(self, observation):
        issues = []

        if not isinstance(observation.timestamp, int) or observation.timestamp < 0:
            issues.append("timestamp must be a non-negative integer")

        if observation.heart_rate is None or not self._is_number(observation.heart_rate):
            issues.append("heart_rate must be numeric")
        elif not 35 <= observation.heart_rate <= 205:
            issues.append("heart_rate out of expected range")

        if observation.skin_response is None or not self._is_number(observation.skin_response):
            issues.append("skin_response must be numeric")
        elif observation.skin_response < 0:
            issues.append("skin_response cannot be negative")

        if observation.temperature is None or not self._is_number(observation.temperature):
            issues.append("temperature must be numeric")
        elif not 25 <= observation.temperature <= 42:
            issues.append("temperature out of expected range")

        if observation.activity_level is None or not self._is_number(observation.activity_level):
            issues.append("activity_level must be numeric")
        elif not 0 <= observation.activity_level <= 1:
            issues.append("activity_level out of expected range")

        if observation.signal_quality is None or not self._is_number(observation.signal_quality):
            issues.append("signal_quality must be numeric")
        elif not 0 <= observation.signal_quality <= 1:
            issues.append("signal_quality out of expected range")

        return issues

    def _build_summary(self):
        total = len(self.raw_observations)
        rejected = len(self.rejected_observations)

        if not self.valid_observations:
            return {
                "participant_id": self.profile.participant_id,
                "classification": "poor_quality",
                "valid_observations": 0,
                "rejected_observations": rejected,
                "total_observations": total,
                "average_heart_rate": None,
                "average_activity": None,
                "average_signal_quality": None,
            }

        valid_heart_rates = [obs.heart_rate for obs in self.valid_observations]
        valid_activity = [obs.activity_level for obs in self.valid_observations]
        valid_signal = [obs.signal_quality for obs in self.valid_observations]

        average_heart_rate = mean(valid_heart_rates)
        average_activity = mean(valid_activity)
        average_signal_quality = mean(valid_signal)

        first_heart_rate = self.valid_observations[0].heart_rate
        last_heart_rate = self.valid_observations[-1].heart_rate
        trend = last_heart_rate - first_heart_rate

        if rejected > 0 and (rejected / total) >= 0.25:
            classification = "poor_quality"
        elif average_signal_quality < 0.6:
            classification = "poor_quality"
        elif trend <= -12 and first_heart_rate >= self.profile.baseline_heart_rate + 10 and last_heart_rate <= self.profile.baseline_heart_rate + 8:
            classification = "recovery"
        elif average_activity >= 0.68 and average_heart_rate >= self.profile.baseline_heart_rate + 35:
            classification = "high_activity"
        elif average_activity >= 0.35 or average_heart_rate >= self.profile.baseline_heart_rate + 15:
            classification = "moderate_activity"
        elif average_activity <= 0.2 and average_heart_rate <= self.profile.baseline_heart_rate + 10:
            classification = "resting"
        else:
            classification = "moderate_activity"

        return {
            "participant_id": self.profile.participant_id,
            "classification": classification,
            "valid_observations": len(self.valid_observations),
            "rejected_observations": rejected,
            "total_observations": total,
            "average_heart_rate": round(average_heart_rate, 2),
            "average_activity": round(average_activity, 2),
            "average_signal_quality": round(average_signal_quality, 2),
        }

    def generate_report(self):
        summary = dict(self.session_summary)
        summary["baseline_heart_rate"] = self.profile.baseline_heart_rate
        summary["baseline_skin_response"] = self.profile.baseline_skin_response
        summary["baseline_temperature"] = self.profile.baseline_temperature
        summary["rejected_details"] = [
            {
                "timestamp": obs.timestamp,
                "issues": obs.issues,
            }
            for obs in self.rejected_observations
        ]
        return summary
