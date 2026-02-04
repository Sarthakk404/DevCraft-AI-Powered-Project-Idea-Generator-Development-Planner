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
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown: cleanup if needed
    print("👋 Shutting down DevCraft")


app = FastAPI(
    title="DevCraft API",
    description="""
## 🚀 AI-Powered Project Idea Generator & Development Planner

DevCraft uses AI (Google Gemini) to generate personalized project ideas based on your:
- **Skills** - What technologies you know
- **Interests** - What domains excite you
- **Experience Level** - Beginner, intermediate, or advanced
- **Goals** - Learning, portfolio, startup, or hackathon
- **Time Available** - How long you have to build

### Features
- 🎯 Personalized project idea generation
- 📋 Feature breakdown and prioritization
- 🛠️ Tech stack recommendations
- 🗺️ Development roadmap with phases
- 📚 Learning path for new technologies
    """,
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
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
        "endpoints": {
            "generate_ideas": "POST /api/v1/idea/generate",
            "full_plan": "POST /api/v1/idea/full-plan",
            "idea_details": "POST /api/v1/idea/{idea_id}/details"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "DevCraft"}
