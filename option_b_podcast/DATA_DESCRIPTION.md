# Option B: Data description

## Generator call

```python
profile, observations = generate_recording_data(
    speaker_id="SP001",
    scenario="energetic",
    seed=42,
    number_of_windows=12,
)
```

The function returns one speaker-profile dictionary and a list of acoustic
observation dictionaries. It does not return the expected classification.

## Profile fields

| Field | Description | Unit |
|---|---|---|
| `speaker_id` | Simulated speaker identifier | none |
| `usual_pitch` | Speaker's usual average pitch | Hz |
| `usual_energy` | Speaker's usual normalized energy | 0-1 |
| `usual_speech_rate` | Speaker's usual speaking rate | approximate words/minute |
| `usual_pause_ratio` | Usual proportion of a window containing pauses | 0-1 |

## Observation fields

| Field | Description | Expected range |
|---|---|---|
| `timestamp` | Ordered observation number | integer, 0 or greater |
| `speech_present` | Whether usable speech was detected | Boolean |
| `pitch` | Average pitch in the speech window | normally 45-450 Hz |
| `energy` | Normalized vocal energy | 0-1 |
| `speech_rate` | Estimated speaking rate | normally 30-260 |
| `pause_ratio` | Proportion of pauses | 0-1 |
| `background_noise` | Normalized environmental-noise estimate | 0-1 |
| `signal_quality` | Reliability indicator | 0-1 |

When speech is absent, speech-related values are `None`. Insufficient-data
scenarios may intentionally include invalid measurements for validation.

## Reproducibility

The same function arguments and seed produce the same data. Different seeds
produce different speaker profiles and observations.

