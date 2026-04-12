# DevCraft — AI-Powered Project Idea Generator & Development Planner

> **Stop searching for project ideas.** DevCraft generates personalized project plans, tech stacks, and roadmaps tailored to your skills and goals — powered by **Google Gemini AI**.

![DevCraft](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

---

## ✨ How It Works

DevCraft uses a **two-step AI flow** for a better experience:

1. **📝 Tell us about yourself** — Select your skills, interests, experience level, goals, and available time
2. **💡 Get project ideas** — Gemini generates 3-5 personalized project ideas
3. **👆 Pick your favorite** — Select the idea that excites you most
4. **🗺️ Get the full plan** — Gemini creates a complete development plan with:
   - ✅ Feature breakdown (core MVP + nice-to-have)
   - 🛠️ Tech stack recommendations with reasoning
   - 📅 Development roadmap with phases, tasks & deliverables
   - 📚 Learning path with curated resources

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite, Framer Motion, Tailwind CSS v4, Lucide Icons |
| **Backend** | FastAPI, Python 3.11+, Pydantic v2 |
| **AI** | Google Gemini 2.0 Flash |
| **Database** | PostgreSQL (NeonDB) |
| **ORM** | SQLAlchemy 2.0 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Google AI Studio API key](https://aistudio.google.com/apikey)
- PostgreSQL database (or use [NeonDB](https://neon.tech) for free)

### 1. Clone the repository

```bash
git clone https://github.com/Sarthakk404/DevCraft-AI-Powered-Project-Idea-Generator-Development-Planner.git
cd DevCraft-AI-Powered-Project-Idea-Generator-Development-Planner
```

### 2. Set up the backend

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
MAX_IDEAS=5
```

### 4. Start the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

### 5. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/idea/generate` | Step 1: Generate 3-5 project ideas |
| `POST` | `/api/v1/idea/expand` | Step 2: Expand selected idea into full plan |
| `POST` | `/api/v1/idea/full-plan` | Legacy: One-shot full plan generation |
| `GET` | `/api/v1/idea/{id}` | Get a specific idea by ID |
| `POST` | `/api/v1/idea/{id}/details` | Get full plan for a saved idea |
| `GET` | `/health` | Health check |

---

## 📁 Project Structure

```
DevCraft/
├── app/                        # Backend (FastAPI)
│   ├── api/v1/endpoints/       # API route handlers
│   ├── models/                 # SQLAlchemy database models
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # Business logic & LLM integration
│   ├── config.py               # App configuration
│   ├── database.py             # Database connection
│   └── main.py                 # FastAPI app entry point
├── frontend/                   # Frontend (React + Vite)
│   └── src/
│       ├── components/         # React components
│       │   ├── Hero.jsx        # Landing hero section
│       │   ├── GeneratorForm.jsx # User profile form
│       │   ├── IdeaPicker.jsx  # Idea selection cards
│       │   ├── FullPlan.jsx    # Complete plan display
│       │   └── Layout.jsx      # App shell (nav + footer)
│       ├── services/api.js     # API client
│       ├── App.jsx             # Main app with 3-stage flow
│       └── index.css           # Design system & global styles
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🎨 Design

DevCraft features a premium dark UI with:
- Animated mesh gradient backgrounds
- Glassmorphism cards with backdrop blur
- Rotating gradient borders on selected elements
- Staggered entrance animations via Framer Motion
- Difficulty-coded badges (🌱 Beginner, ⚡ Intermediate, 🔥 Advanced)
- Animated timeline with pulsing dots
- Custom scrollbar styling

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Sarthakk404">Sarthak</a>
</p>
