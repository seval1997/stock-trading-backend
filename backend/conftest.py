import sys
from pathlib import Path

# Ensure the backend package directory is importable during pytest runs.
BACKEND_ROOT = Path(__file__).resolve().parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
