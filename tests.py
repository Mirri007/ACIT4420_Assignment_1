from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent
FITNESS_DIR = ROOT / "option_a_fitness"
if str(FITNESS_DIR) not in sys.path:
    sys.path.insert(0, str(FITNESS_DIR))

suite = unittest.defaultTestLoader.discover(str(FITNESS_DIR), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)

if not result.wasSuccessful():
    raise SystemExit(1)
