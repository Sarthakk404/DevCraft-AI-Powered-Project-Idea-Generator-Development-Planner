from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ============ Enums ============

class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ProjectGoal(str, Enum):
    learn = "learn"
    portfolio = "portfolio"
    startup = "startup"
    hackathon = "hackathon"
    fun = "fun"


# ============ Request Schemas ============

class UserProfileRequest(BaseModel):
    """User input for generating project ideas."""
    skills: list[str] = Field(
        ..., 
        min_length=1,
        example=["Python", "JavaScript", "SQL"],
        description="Technical skills the user has"
    )
    interests: list[str] = Field(
        ..., 
        min_length=1,
        example=["AI/ML", "Web Development", "Mobile Apps"],
        description="Areas of interest"
    )
    experience_level: ExperienceLevel = Field(
        ..., 
        example="intermediate",
        description="Overall experience level"
    )
    goal: str = Field(
        ..., 
        example="portfolio",
        description="Purpose of the project"
    )
    time_available: str = Field(
        ..., 
        example="2 weeks",
        description="Time available to complete the project"
    )
    preferences: Optional[str] = Field(
        None, 
        example="I want to learn something new with AI",
        description="Any specific preferences or requirements"
    )


class IdeaSelectionRequest(BaseModel):
    """Request to select an idea for detailed breakdown."""
    idea_id: int = Field(..., description="ID of the selected idea")


# ============ Response Schemas ============

class ProjectIdea(BaseModel):
    """A single project idea."""
    id: Optional[int] = None
    title: str = Field(..., example="AI-Powered Resume Analyzer")
    description: str = Field(..., example="Build a web app that uses NLP to analyze resumes...")
    difficulty: str = Field(..., example="Intermediate")
    estimated_time: str = Field(..., example="2-3 weeks")
    why_suitable: str = Field(..., example="Matches your Python and AI interests...")

    class Config:
        from_attributes = True


class Feature(BaseModel):
    """A single feature."""
    name: str
    description: str
    priority: str = Field(default="core", description="core, important, or nice-to-have")


class FeatureBreakdown(BaseModel):
    """Feature breakdown for a project."""
    core_features: list[Feature]
    nice_to_have: list[Feature]


class TechStack(BaseModel):
    """Technology stack recommendation."""
    frontend: list[str] = Field(default_factory=list, example=["React", "TailwindCSS"])
    backend: list[str] = Field(default_factory=list, example=["FastAPI", "Python"])
    database: list[str] = Field(default_factory=list, example=["PostgreSQL"])
    tools: list[str] = Field(default_factory=list, example=["Docker", "Git"])
    reasoning: Optional[str] = None


class Phase(BaseModel):
    """A development phase in the roadmap."""
    phase_number: int
    title: str
    duration: str
    tasks: list[str]
    deliverables: list[str]


class Roadmap(BaseModel):
    """Development roadmap."""
    total_duration: str
    phases: list[Phase]


class Resource(BaseModel):
    """A learning resource."""
    topic: str
    resource_type: str  # "video", "article", "course", "documentation"
    title: str
    url: Optional[str] = None
    estimated_time: str


class LearningPath(BaseModel):
    """Learning path for new technologies."""
    new_technologies: list[str]
    resources: list[Resource]


# ============ Combined Response ============

class GenerateIdeasResponse(BaseModel):
    """Response with generated project ideas."""
    ideas: list[ProjectIdea]
    message: str = "Here are your personalized project ideas!"


class FullProjectPlanResponse(BaseModel):
    """Complete project plan with all details."""
    idea: ProjectIdea
    features: FeatureBreakdown
    tech_stack: TechStack
    roadmap: Roadmap
    learning_path: LearningPath
    message: str = "Your complete project plan is ready!"
