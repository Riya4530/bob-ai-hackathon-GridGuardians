import sys
from pathlib import Path

# Ensure "app" package is importable when pytest is run from src/backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
