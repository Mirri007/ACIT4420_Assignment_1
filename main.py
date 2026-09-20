from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
FITNESS_DIR = ROOT / "option_a_fitness"
if str(FITNESS_DIR) not in sys.path:
    sys.path.insert(0, str(FITNESS_DIR))

from fitness_runner import main


if __name__ == "__main__":
    main()
