import sys
from pathlib import Path

# Ensure the src directory is on the path for tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
