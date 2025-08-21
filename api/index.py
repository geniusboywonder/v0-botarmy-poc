# Vercel Serverless Function Entrypoint
import sys
from pathlib import Path

# Add project root to the Python path to allow imports from `backend`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import the configured FastAPI app instance
from backend.main import app