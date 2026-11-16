import sys
from pathlib import Path

# Tests import the app modules as top-level modules, like uvicorn and streamlit do.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
