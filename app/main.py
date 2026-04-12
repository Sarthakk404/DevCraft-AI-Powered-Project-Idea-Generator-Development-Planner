from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.database import engine, Base
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    print("👋 Shutting down DevCraft")


app = FastAPI(
    title="DevCraft API",
    description="""
## 🚀 AI-Powered Project Idea Generator & Development Planner

DevCraft uses **Groq Llama** AI to generate personalized project ideas based on your:
- **Skills** — What technologies you know
- **Interests** — What domains excite you
- **Experience Level** — Beginner, intermediate, or advanced
- **Goals** — Learning, portfolio, startup, or hackathon
- **Time Available** — How long you have to build

### How It Works
1. 🎯 **Step 1:** Submit your profile → Get 3-5 personalized project ideas
2. ✅ **Step 2:** Pick the idea you love → Get a complete development plan

### What You Get
- 📋 Feature breakdown and prioritization
- 🛠️ Tech stack recommendations with reasoning
- 🗺️ Development roadmap with phases and deliverables
- 📚 Learning path for new technologies with resources
    """,
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dev-craft-ai-powered-project-idea-g.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to DevCraft API 🚀",
        "docs": "/docs",
        "version": settings.app_version,
        "powered_by": "Groq Llama",
        "endpoints": {
            "generate_ideas": "POST /api/v1/idea/generate",
            "expand_idea": "POST /api/v1/idea/expand",
            "full_plan": "POST /api/v1/idea/full-plan",
            "idea_details": "POST /api/v1/idea/{idea_id}/details",
        },
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "DevCraft", "version": settings.app_version}
