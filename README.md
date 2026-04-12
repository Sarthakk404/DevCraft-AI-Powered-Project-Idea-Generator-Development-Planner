<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=200&section=header&text=DevCraft&fontSize=80&fontAlignY=35&desc=AI-Powered%20Project%20Idea%20Generator%20&descAlignY=60&descAlign=50" />

  **Stop searching. Start building.**  
  *DevCraft generates hyper-personalized project plans, comprehensive tech stacks, and step-by-step roadmaps tailored strictly to your unique skill set and carrier ambitions — now supercharged by lightning-fast **Groq Llama 3.3 70B**.*

  ### 🪐 The Ultimate Idea Generator for Modern Developers

  <p align="center">
    <img src="https://img.shields.io/badge/Powered%20by-Groq%20Llama-black?style=for-the-badge&logo=ai&logoColor=f59e0b" alt="Groq Llama" />
    <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Frontend-React%20%7C%20Vite-black?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  </p>

</div>

---

## ✨ Experience The Magic: How It Works

DevCraft utilizes an elegant, **context-aware two-step AI flow** to generate bespoke engineering plans:

1. **📝 Tell Us About Yourself**  
   Input your tech arsenal, domains of interest, raw experience level, goals, and strict time constraints.
2. **💡 Enter The Matrix**  
   Our Groq-backed neural engine processes your profile to generate 3-5 high-converting, tailored project ideas instantly.
3. **👆 Select Your Destiny**  
   Pick the single project that ignites your passion via an immersive card portfolio.
4. **🗺️ Unveil the Master Plan**  
   Watch as the AI fabricates a comprehensive, enterprise-tier development plan in seconds:
   - ✅ **MVP Feature Breakdown** *(Core capabilities vs Nice-to-Haves)*
   - 🛠️ **Curated Tech Stack** *(Explicit front-to-back tooling with embedded reasoning)*
   - 📅 **Strategic Roadmap** *(Phase-by-phase deliverables)*
   - 📚 **Learning Path** *(Targeted, non-hallucinated resources)*

---

## 🏗️ Architecture Stack

Engineered using modern, lightning-fast tools dedicated to maximum visual elegance and backend velocity.

| Layer | Premium Technology Context |
|-------|-----------|
| **Frontend UI** | **React 19** powered by **Vite**, deep interactions via **Framer Motion**, styled with **Tailwind CSS v4**, and **Lucide Icons** |
| **Backend Core** | **FastAPI** utilizing **Python 3.11+**, strongly typed with **Pydantic v2** |
| **Intelligence** | **Groq Llama 3.3 70B Versatile** *(JSON Mode via `groq` async SDK)* |
| **Database** | Fully-Managed **PostgreSQL (NeonDB)** |
| **Data Layer** | **SQLAlchemy 2.0 / pg8000** |

---

## 🚀 Lift-Off

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- A High-Speed [Groq API key](https://console.groq.com/keys)
- PostgreSQL database URL (or use [NeonDB](https://neon.tech) for a free instance)

### 1. Initialize the Repository

```bash
git clone https://github.com/Sarthakk404/DevCraft-AI-Powered-Project-Idea-Generator-Development-Planner.git
cd DevCraft-AI-Powered-Project-Idea-Generator-Development-Planner
```

### 2. Ignite the Backend Core

```bash
# Form virtual environment network
python -m venv venv

# Activate connection
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install essential dependencies
pip install -r requirements.txt
```

### 3. Synchronize Environment Variables

Clone the environment template and embed your personal keys:

```bash
cp .env.example .env
```

*Inside `.env`:*
```env
# Groq API keys required for hyper-fast generations
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Database Tunnel
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
MAX_IDEAS=5
```

### 4. Boot UP

```bash
uvicorn app.main:app --reload
```
> The API server initiates at `http://localhost:8000`. Full OpenAPI docs mapped at `http://localhost:8000/docs`.

### 5. Launch the Client Interface

```bash
cd frontend
npm install
npm run dev
```
> Discover your visually-luxurious UI live at `http://localhost:5173`.

---

## 📡 Core API Topography

| Method | Endpoint | Architectural Purpose |
|--------|----------|-------------|
| `POST` | `/api/v1/idea/generate` | Stage I: Generate 3-5 unique ideas mapped to user context |
| `POST` | `/api/v1/idea/expand` | Stage II: Explode selected idea into an explicit engineering playbook |
| `POST` | `/api/v1/idea/full-plan` | Legacy integration: Immediate A-Z end-to-end plan generation |
| `GET`  | `/api/v1/idea/{id}` | Retrieve cached specific idea definition |
| `POST` | `/api/v1/idea/{id}/details` | Rehydrate fully-saved comprehensive plan |
| `GET`  | `/health` | Systems check |

---

## 🎨 A Visually Luxurious Playground

DevCraft introduces an enterprise-grade dark-mode UI intentionally designed to stun:
- **Dynamic Deep Space Backgrounds:** Multi-layered radial meshing casting an ambient indigo glow.
- **Pure Glassmorphism Cards:** Intricate `.backdrop-blur-xl` layering providing heavy, premium depth overlays.
- **Liquid Physics:** Component bounds breathe through subtle `scale` modulations and deep inner drop-shadow transitions.
- **Cinematic Pacing:** Staggered entrance animations governed actively by Framer Motion. 

---

## 📄 License & Intellectual Property

This masterpiece is fully open source under the robust [MIT License](LICENSE).

---

<div align="center">
  <p>Engineered to Perfection with ❤️ by <a href="https://github.com/Sarthakk404">Sarthak</a></p>
</div>
