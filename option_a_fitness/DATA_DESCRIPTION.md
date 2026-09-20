# Option A: Data description

## Generator call

```python
profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="moderate_activity",
    seed=42,
    number_of_windows=12,
)
```

The function returns one participant-profile dictionary and a list of observation
dictionaries. It does not return the expected classification.

## Profile fields

| Field | Description | Unit |
|---|---|---|
| `participant_id` | Simulated participant identifier | none |
| `baseline_heart_rate` | Personal resting reference | beats/minute |
| `baseline_skin_response` | Personal reference skin response | simulated units |
| `baseline_temperature` | Personal skin-temperature reference | degrees Celsius |

## Observation fields

| Field | Description | Expected range |
|---|---|---|
| `timestamp` | Ordered observation number | integer, 0 or greater |
| `heart_rate` | Measured heart rate | normally 35-205 bpm |
| `skin_response` | Simulated sensor value | normally 0 or greater |
| `temperature` | Simulated skin temperature | normally 25-42 C |
| `activity_level` | Normalized movement level | 0-1 |
| `signal_quality` | Measurement reliability indicator | 0-1 |

Poor-quality scenarios intentionally contain `None` values and impossible
values. Your program must decide how to reject or flag these observations.

## Reproducibility

The same function arguments and seed produce the same data. Different seeds
produce different profiles and measurements.

