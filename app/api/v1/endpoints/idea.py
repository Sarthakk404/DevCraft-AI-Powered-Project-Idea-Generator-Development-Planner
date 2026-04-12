import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.idea import (
    UserProfileRequest,
    ExpandIdeaRequest,
    GenerateIdeasResponse,
    FullProjectPlanResponse,
    ProjectIdea,
)
from app.services.idea_service import idea_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=GenerateIdeasResponse)
async def generate_ideas(
    profile: UserProfileRequest,
    db: Session = Depends(get_db),
):
    """
    Step 1: Generate personalized project ideas based on user profile.

    Returns a list of 3-5 project ideas tailored to the user's
    skills, interests, experience level, goals, and time availability.
    """
    try:
        _, ideas = await idea_service.generate_and_save_ideas(db, profile)
        return GenerateIdeasResponse(ideas=ideas)
    except Exception as e:
        logger.exception("Error generating ideas")
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {e}")


@router.post("/expand", response_model=FullProjectPlanResponse)
async def expand_idea(
    request: ExpandIdeaRequest,
    db: Session = Depends(get_db),
):
    """
    Step 2: Expand a selected idea into a complete project plan.

    Takes the user profile and their selected idea, then generates
    a full development plan with features, tech stack, roadmap,
    and learning path tailored to that specific project.
    """
    try:
        plan = await idea_service.expand_idea_to_plan(db, request)
        return plan
    except Exception as e:
        logger.exception("Error expanding idea to plan")
        raise HTTPException(
            status_code=500, detail=f"Error generating plan: {e}"
        )


@router.post("/full-plan", response_model=FullProjectPlanResponse)
async def generate_full_plan(
    profile: UserProfileRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a complete project plan in one call (legacy).

    This endpoint generates a project idea, feature breakdown,
    tech stack recommendation, development roadmap, and learning path
    all in a single response.
    """
    try:
        plan = await idea_service.generate_complete_plan(db, profile)
        return plan
    except Exception as e:
        logger.exception("Error generating full plan")
        raise HTTPException(status_code=500, detail=f"Error generating plan: {e}")


@router.get("/{idea_id}", response_model=ProjectIdea)
async def get_idea(
    idea_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific idea by ID."""
    idea = await idea_service.get_idea_by_id(db, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return ProjectIdea(
        id=idea.id,
        title=idea.title,
        description=idea.description,
        difficulty=idea.difficulty,
        estimated_time=idea.estimated_time,
        why_suitable=idea.why_suitable or "",
    )


@router.post("/{idea_id}/details", response_model=FullProjectPlanResponse)
async def get_idea_details(
    idea_id: int,
    db: Session = Depends(get_db),
):
    """Get the full development plan for a specific idea."""
    plan = await idea_service.get_full_plan_by_id(db, idea_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
