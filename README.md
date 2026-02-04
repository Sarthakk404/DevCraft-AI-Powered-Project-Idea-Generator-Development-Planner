# DevCraft 🚀

DevCraft is an AI-powered project idea generator and development planner designed to help developers bridge the gap between learning and building. It generates personalized project ideas, detailed feature breakdowns, tech stack recommendations, and step-by-step roadmaps based on your skills and interests.

## ✨ Features

- **Personalized Idea Generation**: Tailored to your skill level and goals.
- **Smart Tech Stack**: Recommendations based on what you know + what you should learn.
- **Detailed Roadmaps**: Phased development plans to keep you on track.
- **Feature Breakdowns**: Core MVP features vs. "Nice-to-have" extras.
- **Learning Resources**: Curated links for new technologies.

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Framer Motion, Lucide Icons
- **Backend**: FastAPI, Python 3.11
- **AI**: Google Gemini Pro (via `google-genai` SDK)
- **Database**: PostgreSQL
- **Orchestration**: Docker & Docker Compose

## 🚀 Quick Start (with Docker)

The easiest way to get DevCraft running is using Docker Compose.

### Prerequisites

- Docker and Docker Compose installed
- Google Gemini API Key

### Installation

1. Clone the repository
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Add your `GEMINI_API_KEY` to the `.env` file.
4. Run the application:
   ```bash
   docker compose up --build
   ```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)

---

## 🛠️ Manual Development Setup

If you prefer to run the services manually:

### Backend

1. Create virtual environment: `python -m venv venv`
2. Activate venv: `source venv/bin/activate` (Windows: `venv\Scripts\Activate`)
3. Install deps: `pip install -r requirements.txt`
4. Run: `fastapi dev app/main.py`

### Frontend

1. Navigate to `frontend/`
2. Install deps: `npm install`
3. Run: `npm run dev`

## 👤 Author

**Sarthak** - [github.com/Sarthakk404](https://github.com/Sarthakk404)

## 📄 License

MIT
