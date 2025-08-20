# botarmy-poc

*Automatically synced with your [v0.app](https://v0.app) deployments*

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/geniusboywonder/v0-botarmy-poc)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.app-black?style=for-the-badge)](https://v0.app/chat/projects/ZwGgRjunf45)

## Overview

This repository will stay in sync with your deployed chats on [v0.app](https://v0.app).
Any changes you make to your deployed app will be automatically pushed to this repository from [v0.app](https://v0.app).

## Deployment

Your project is live at:

**[https://vercel.com/geniusboywonder/v0-botarmy-poc](https://vercel.com/geniusboywonder/v0-botarmy-poc)**

## Build your app

Continue building your app on:

**[https://v0.app/chat/projects/ZwGgRjunf45](https://v0.app/chat/projects/ZwGgRjunf45)**

## How It Works

1. Create and modify your project using [v0.app](https://v0.app)
2. Deploy your chats from the v0 interface
3. Changes are automatically pushed to this repository
4. Vercel deploys the latest version from this repository

---

## Running Locally for Demo

To run this project locally for a demonstration, follow these steps.

### Prerequisites

*   Python 3.8+
*   Node.js 18+ and pnpm (or npm/yarn)
*   An `OPENAI_API_KEY` environment variable set with a valid OpenAI API key.

### 1. Backend Setup

From the root of the project directory:

```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python main.py
```

The backend server will start on `http://localhost:8000`.

### 2. Frontend Setup

In a new terminal, from the root of the project directory:

```bash
# Install Node.js dependencies
pnpm install

# Run the frontend development server
pnpm run dev
```

The frontend application will be available at `http://localhost:3000`.

### 3. Running the Demo

1.  Open `http://localhost:3000` in your browser.
2.  The connection status in the top right should indicate "Connected".
3.  Use the "Test Backend" and "Test OpenAI" buttons to ensure services are running.
4.  Use the "Start Test Project" button or enter your own project brief to start the agent workflow.
5.  Observe the real-time status updates in the log and the agent status cards.
