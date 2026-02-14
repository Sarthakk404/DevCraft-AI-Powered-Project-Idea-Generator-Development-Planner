# DevCraft – AI-Powered Project Idea Generator & Development Planner

DevCraft is a FastAPI + React application that uses Google Gemini AI to generate personalized project ideas, feature breakdowns, tech stack recommendations, development roadmaps, learning paths, and timelines based on your skills, interests, goals, and time availability.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, TailwindCSS
- **AI**: Google Gemini 2.0 Flash

## Quick Start (Manual Setup)

This project is designed to run locally without Docker for simplicity.

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Google Gemini API key](https://aistudio.google.com/apikey) (Free)

### 1. Backend Setup

1.  Open a terminal in the root `DevCraft` folder.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure `.env`:
    - Create a `.env` file (copy `.env.example` if it exists, or just create new).
    - Add your Gemini API Key:
      ```properties
      GEMINI_API_KEY=your_key_here
      GEMINI_MODEL=gemini-2.0-flash
      ```
5.  Start the server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup

1.  Open a **new** terminal.
2.  Navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Start the dev server:
    ```bash
    npm run dev
    ```
5.  Open `http://localhost:5173` in your browser.

## usage

1.  Fill out your profile (Skills, Interests, Goal, Time).
2.  Click **"Generate Project Plan"**.
3.  Wait for the AI to generate your plan (this may take 30-60 seconds).
    - _Note: If you hit rate limits, the app will automatically wait and retry. Just be patient!_

## Troubleshooting

- **429 Resource Exhausted**: You hit the free tier rate limit. The app handles this by waiting, but if it persists, try waiting 1-2 minutes manually or get a new API key.
- **Database Error**: Ensure you aren't running an old PostgreSQL config. The defaults use SQLite (`devcraft.db`) which is created automatically.
