from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.idea import (
    UserProfileRequest,
    GenerateIdeasResponse,
    FullProjectPlanResponse,
    ProjectIdea
)
from app.services.idea_service import idea_service

router = APIRouter()


@router.get("/test")
def test_idea_api():
    """Test endpoint to verify API is working."""
    return {"status": "Idea API working fine 🚀"}


@router.post("/generate", response_model=GenerateIdeasResponse)
async def generate_ideas(
    profile: UserProfileRequest,
    db: Session = Depends(get_db)
):
    """
    Generate personalized project ideas based on user profile.
    
    Returns a list of 3-5 project ideas tailored to user's:
    - Skills
    - Interests
    - Experience level
    - Goals
    - Time availability
    """
    try:
        _, ideas = await idea_service.generate_and_save_ideas(db, profile)
        return GenerateIdeasResponse(ideas=ideas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")


@router.post("/full-plan", response_model=FullProjectPlanResponse)
async def generate_full_plan(
    profile: UserProfileRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a complete project plan in one call.
    
    This endpoint:
    1. Generates project ideas
    2. Selects the best one
    3. Creates feature breakdown
    4. Recommends tech stack
    5. Creates development roadmap
    6. Generates learning path
    
    Perfect for getting everything you need to start building!
    """
    try:
        plan = await idea_service.generate_complete_plan_new(db, profile)
        return plan
    except Exception as e:
        import traceback
        print(f"ERROR in generate_full_plan: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")


@router.post("/{idea_id}/details", response_model=FullProjectPlanResponse)
async def get_idea_details(
    idea_id: int,
    profile: UserProfileRequest,
    db: Session = Depends(get_db)
):
    """
    Get detailed breakdown for a specific idea.
    
    Use this after generating ideas to get the full plan
    for an idea you're interested in.
    """
    try:
        plan = await idea_service.generate_full_plan(db, idea_id, profile)
        return plan
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating details: {str(e)}")


@router.get("/{idea_id}", response_model=ProjectIdea)
async def get_idea(
    idea_id: int,
    db: Session = Depends(get_db)
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
        why_suitable=""
    )
