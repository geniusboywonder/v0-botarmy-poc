# BotArmy Backend Setup Instructions

## Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

## Setup Steps

### 1. Navigate to Backend Directory
\`\`\`bash
cd backend
\`\`\`

### 2. Create Virtual Environment (Recommended)
\`\`\`bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set Environment Variables (Optional)
Create a `.env` file in the backend directory:
\`\`\`env
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
\`\`\`

### 5. Start the Backend Server
\`\`\`bash
python main.py
\`\`\`

Or using uvicorn directly:
\`\`\`bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### 6. Verify Backend is Running
- Open http://localhost:8000 in your browser
- You should see: `{"message": "BotArmy Backend is running", ...}`
- Health check: http://localhost:8000/health

## Docker Setup (Alternative)

### 1. Build and Run with Docker Compose
\`\`\`bash
cd backend
docker-compose up --build
\`\`\`

## Frontend Connection
Once the backend is running, the frontend will automatically connect to:
- WebSocket: `ws://localhost:8000/ws/agui`
- REST API: `http://localhost:8000`

## Troubleshooting
- **Port 8000 in use**: Change the port in `main.py` or kill the process using port 8000
- **Module not found**: Ensure you're in the backend directory and virtual environment is activated
- **WebSocket connection failed**: Verify the backend server is running on port 8000

## Development Mode
The frontend automatically detects development mode and uses WebSocket simulation when the backend isn't running, so you can develop the UI without starting the backend.
