"""One-command launcher:  python run.py

Trains the models if artefacts are missing, then starts the Streamlit app.
"""
import subprocess
import sys

from src.config import DB_PATH, MODELS_DIR
from src.pipeline import run_pipeline


def main() -> int:
    if not (MODELS_DIR / "metadata.json").exists() or not DB_PATH.exists():
        print("Model artefacts not found - running the pipeline first...")
        run_pipeline()
    return subprocess.call([sys.executable, "-m", "streamlit", "run", "app/dashboard.py"])


if __name__ == "__main__":
    sys.exit(main())
