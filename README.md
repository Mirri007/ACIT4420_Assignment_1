# Smart Fitness Session Analyzer

Selected option: Option A - Smart Fitness Session Analyzer

Student name: Mirjam Throndsen
Student number: [Add student number here]

GitHub repository: https://github.com/Mirri007/ACIT4420_Assignment_1

## Short description

This application reads fitness measurement data for one participant, validates each observation window, compares every value against the participant's personal baseline, and classifies the complete session as resting, moderate activity, high activity, recovery, or poor quality.

The generator supplies raw dictionaries and lists. The assignment requires us to turn those into domain objects, analyze the session, and explain the final classification clearly.

## Repository structure

```text
student_repository/
├── README.md
├── main.py
├── sample_data.py
├── tests.py
├── requirements.txt
├── option_a_fitness/
│   ├── data_generator.py
│   ├── fitness_analyzer.py
│   ├── fitness_runner.py
│   └── test_fitness_analyzer.py
└── option_b_podcast/   # removed from final assignment version
```

The final project should only include the chosen assignment option. This repository keeps the relevant fitness solution in the `option_a_fitness` directory and uses a root-level entry point for the instructor or evaluator.

## Class design

### ParticipantProfile
Responsible for storing the participant's reference measurements:

- baseline heart rate
- baseline skin response
- baseline temperature

These values represent the person's normal baseline and are used for comparison.

### FitnessObservation
Represents one observation window. It stores:

- timestamp
- heart rate
- skin response
- temperature
- activity level
- signal quality
- validation issues

This object keeps the state for one measurement and makes it easy to validate and summarize.

### FitnessSessionAnalyzer
Responsible for:

- reading the raw data
- validating each observation
- separating valid and invalid readings
- calculating summary statistics
- comparing measurements to the participant baseline
- classifying the full session
- producing a report that explains the result

This class composes the participant profile and all observations into one session evaluation.

## Where OOP principles are demonstrated

### Encapsulation
Each class keeps its own state and exposes only the relevant behaviour. The participant baseline and the observation values are stored inside their own objects rather than as loose dictionaries.

### Composition
The analyzer is built from a participant profile plus many observations. The session is therefore a structured combination of objects instead of a single unstructured dictionary.

### Inheritance
This assignment does not require a deep inheritance hierarchy. The solution uses classes and composition to model the domain clearly and cleanly.

### Overriding
No overriding is required for this assignment, because the data generator is a supplied implementation and the analysis logic is implemented in custom classes.

## Assumptions and classification rules

The program assumes:

- the baseline values represent the participant's normal resting behaviour
- valid observations fall within realistic ranges for heart rate, temperature and activity
- poor-quality data is rejected or flagged instead of being trusted in the final classification

### Classification rules

- resting: activity and heart rate remain near the participant baseline
- moderate activity: activity and heart rate are above baseline but not extreme
- high activity: the session shows sustained high exertion
- recovery: heart rate and activity decline toward the baseline near the end of the session
- poor quality: too many observations are invalid or signal quality is too low

## Installation and running instructions

### Clone the repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

### Run the application from the repository root

```bash
python3 main.py
```

This root script starts the fitness program from the assignment-specific runner.

If your system uses `python` instead of `python3`, use:

```bash
python main.py
```

### Run the tests

```bash
python3 -m unittest -v
```

## How to use the generator and analyzer

The project is designed to work in a simple, readable pattern:

```python
from option_a_fitness.data_generator import generate_fitness_data
from option_a_fitness.fitness_analyzer import FitnessSessionAnalyzer

profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="recovery",
    seed=42,
    number_of_windows=10,
)

analyzer = FitnessSessionAnalyzer(profile, observations)
report = analyzer.generate_report()
print(report)
```

This generates one realistic data set, passes it to the analyzer, and prints the classification and summary.

## Generate and analyze many datasets

You can also create a batch of examples, for example 100 generated sessions, and analyze each one in a loop:

```python
from option_a_fitness.data_generator import generate_fitness_data
from option_a_fitness.fitness_analyzer import FitnessSessionAnalyzer

results = []

for i in range(100):
    profile, observations = generate_fitness_data(
        participant_id=f"P{i:03d}",
        scenario="random",
        seed=i,
        number_of_windows=12,
    )

    analyzer = FitnessSessionAnalyzer(profile, observations)
    results.append({
        "participant_id": profile["participant_id"],
        "classification": analyzer.session_summary["classification"],
        "valid_observations": analyzer.session_summary["valid_observations"],
        "rejected_observations": analyzer.session_summary["rejected_observations"],
    })

print(f"Analyzed {len(results)} sessions")
print(results[:5])
```

This pattern is useful if you want to test many generated sessions, inspect how often each class appears, or quickly check whether the classification logic remains stable.

## Example output

### Example 1: single dataset

```python
from option_a_fitness.data_generator import generate_fitness_data
from option_a_fitness.fitness_analyzer import FitnessSessionAnalyzer

profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="recovery",
    seed=42,
    number_of_windows=10,
)

analyzer = FitnessSessionAnalyzer(profile, observations)
print(analyzer.generate_report())
```

Example result:

```text
{'participant_id': 'P001',
 'classification': 'recovery',
 'valid_observations': 10,
 'rejected_observations': 0,
 'total_observations': 10,
 'average_heart_rate': 112.8,
 'classification_reason': 'heart rate and activity declined toward the participant baseline near the end of the session'}
```

### Example 2: 200 generated datasets

```python
from collections import Counter
from option_a_fitness.data_generator import generate_fitness_data
from option_a_fitness.fitness_analyzer import FitnessSessionAnalyzer

results = Counter()

for i in range(200):
    profile, observations = generate_fitness_data(
        participant_id=f"P{i:03d}",
        scenario="random",
        seed=i,
        number_of_windows=12,
    )
    analyzer = FitnessSessionAnalyzer(profile, observations)
    results[analyzer.session_summary["classification"]] += 1

print(results)
```

This prints something like:

```text
Counter({'moderate_activity': 78, 'resting': 35, 'recovery': 22, 'high_activity': 19, 'poor_quality': 46})
```

The exact numbers vary because the generator is random, but the pattern shows how you can evaluate many generated sessions quickly.

## Known limitations

- This is designed for the structured exercise data produced by the generator and is not a medical monitoring system.
- Recovery detection is based on the generated pattern and simplified rules, not a full physiological model.
- No third-party packages are required; the project uses only the Python standard library.

## GitHub repository and submission

This project is published in the repository below and is ready for submission:

- Repository URL: https://github.com/Mirri007/ACIT4420_Assignment_1
- Branch: main
- Final commit hash: use the latest commit hash from the repository history at the time of submission

Create a public repository or a private repository that is accessible to the instructor. Submit both the repository URL and the final commit hash representing the final assessed version.

## Required repository contents

The repository should contain the project files and may use a different structure if explained in the README. The final project structure for this submission is:

```text
ACIT4420_Assignment_1/
├── README.md
├── main.py
├── sample_data.py
├── tests.py
├── requirements.txt
├── option_a_fitness/
│   ├── DATA_DESCRIPTION.md
│   ├── data_generator.py
│   ├── fitness_analyzer.py
│   ├── fitness_runner.py
│   └── test_fitness_analyzer.py
└── .gitignore
```

If no third-party packages are used, `requirements.txt` may be empty or may state that the project uses only the Python standard library.

## How to run and verify the project

From the project root:

```bash
cd /Users/mirijamthrondsen/Documents/GitHub/ACIT4420_Assignment_1
python3 main.py
```

To run the automated tests:

```bash
cd /Users/mirijamthrondsen/Documents/GitHub/ACIT4420_Assignment_1
python3 tests.py
```

This project uses only the Python standard library, so no package installation is required beyond Python itself.

## Final note

The instructor-provided data generator should be treated as supplied code and should not be modified unless the assignment explicitly allows it. The required analysis logic should be implemented in the student's own classes and modules.

This repository implements Option A only, in line with the assignment requirement to keep only the selected solution and remove the other assignment option from the final submission.

