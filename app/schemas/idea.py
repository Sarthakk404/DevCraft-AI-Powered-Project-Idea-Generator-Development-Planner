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
        examples=[["Python", "JavaScript", "SQL"]],
        description="Technical skills the user has"
    )
    interests: list[str] = Field(
        ...,
        min_length=1,
        examples=[["AI/ML", "Web Development", "Mobile Apps"]],
        description="Areas of interest"
    )
    experience_level: ExperienceLevel = Field(
        ...,
        examples=["intermediate"],
        description="Overall experience level"
    )
    goal: str = Field(
        ...,
        examples=["portfolio"],
        description="Purpose of the project"
    )
    time_available: str = Field(
        ...,
        examples=["2 weeks"],
        description="Time available to complete the project"
    )
    preferences: Optional[str] = Field(
        None,
        examples=["I want to learn something new with AI"],
        description="Any specific preferences or requirements"
    )


class SelectedIdea(BaseModel):
    """The idea the user selected from the suggestions."""
    title: str
    description: str
    difficulty: str = "Intermediate"
    estimated_time: str = ""
    why_suitable: str = ""


class ExpandIdeaRequest(BaseModel):
    """Request to expand a selected idea into a full project plan."""
    profile: UserProfileRequest
    selected_idea: SelectedIdea


class IdeaSelectionRequest(BaseModel):
    """Request to select an idea for detailed breakdown."""
    idea_id: int = Field(..., description="ID of the selected idea")


# ============ Response Schemas ============

class ProjectIdea(BaseModel):
    """A single project idea."""
    id: Optional[int] = None
    title: str = Field(..., examples=["AI-Powered Resume Analyzer"])
    description: str = Field(..., examples=["Build a web app that uses NLP to analyze resumes..."])
    difficulty: str = Field(..., examples=["Intermediate"])
    estimated_time: str = Field(..., examples=["2-3 weeks"])
    why_suitable: str = Field(..., examples=["Matches your Python and AI interests..."])

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
    frontend: list[str] = Field(default_factory=list, examples=[["React", "TailwindCSS"]])
    backend: list[str] = Field(default_factory=list, examples=[["FastAPI", "Python"]])
    database: list[str] = Field(default_factory=list, examples=[["PostgreSQL"]])
    tools: list[str] = Field(default_factory=list, examples=[["Git", "GitHub Actions"]])
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


# ============ Combined Responses ============

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
