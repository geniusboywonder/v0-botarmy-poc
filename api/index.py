# This file is the entrypoint for Vercel's serverless function.
# It imports the FastAPI app instance from the main backend application.

# Add the backend directory to the Python path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.main import app