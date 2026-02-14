from sqlalchemy.orm import Session
from app.models.idea import UserProfile, GeneratedIdea
from app.schemas.idea import (
    UserProfileRequest,
    ProjectIdea,
    FullProjectPlanResponse,
    FeatureBreakdown,
    Feature,
    TechStack,
    Roadmap,
    Phase,
    LearningPath,
    Resource,
)
from app.services.llm_service import llm_service


class IdeaService:
    """Service for managing project idea generation and storage."""

    async def create_user_profile(self, db: Session, profile: UserProfileRequest) -> UserProfile:
        """Save user profile to database."""
        db_profile = UserProfile(
            skills=profile.skills,
            interests=profile.interests,
            experience_level=profile.experience_level.value,
            goal=profile.goal,
            time_available=profile.time_available,
            preferences=profile.preferences,
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    async def generate_and_save_ideas(
        self, db: Session, profile: UserProfileRequest
    ) -> tuple[UserProfile, list[ProjectIdea]]:
        """Generate project ideas and save them to database."""
        
        # Save user profile
        db_profile = await self.create_user_profile(db, profile)
        
        # Generate ideas using LLM
        ideas = await llm_service.generate_project_ideas(profile)

        # Save ideas to database
        saved_ideas = []
        for idea in ideas:
            db_idea = GeneratedIdea(
                user_profile_id=db_profile.id,
                title=idea.title,
                description=idea.description,
                difficulty=idea.difficulty,
                estimated_time=idea.estimated_time,
                why_suitable=idea.why_suitable,
            )
            db.add(db_idea)
            db.commit()
            db.refresh(db_idea)
            
            # Add ID to the idea
            idea.id = db_idea.id
            saved_ideas.append(idea)

        return db_profile, saved_ideas

    async def get_idea_by_id(self, db: Session, idea_id: int) -> GeneratedIdea | None:
        """Get a generated idea by ID."""
        return db.query(GeneratedIdea).filter(GeneratedIdea.id == idea_id).first()

    async def generate_complete_plan(
        self, db: Session, profile: UserProfileRequest
    ) -> FullProjectPlanResponse:
        """Generate a complete plan in one shot using optimised LLM call."""
        
        # 1. Call LLM for everything
        data = await llm_service.generate_complete_plan_one_shot(profile)
        
        if not isinstance(data, dict):
            raise ValueError(f"LLM did not return a dictionary. Got: {type(data)}")

        for key in ("idea", "features", "tech_stack", "roadmap", "learning_path"):
            if key not in data:
                raise ValueError(f"Missing required key '{key}' in LLM response")

        # 2. Save Profile
        db_profile = await self.create_user_profile(db, profile)

        # 3. Save Idea
        idea_data = data["idea"]
        db_idea = GeneratedIdea(
            user_profile_id=db_profile.id,
            title=idea_data["title"],
            description=idea_data["description"],
            difficulty=idea_data["difficulty"],
            estimated_time=idea_data["estimated_time"],
            why_suitable=idea_data.get("why_suitable", ""),
            is_selected=True, # Auto-select
        )
        
        # 4. Save components (as JSON blobs via SQLAlchemy models which handle serialization if configured, or we assume models utilize JSON type)
        # Note: The original clean code assumed models had these fields.
        db_idea.features = data["features"]
        db_idea.tech_stack = data["tech_stack"]
        db_idea.roadmap = data["roadmap"]
        db_idea.learning_path = data["learning_path"]

        db.add(db_idea)
        db.commit()
        db.refresh(db_idea)

        # 5. Construct Response
        return FullProjectPlanResponse(
            idea=ProjectIdea(
                id=db_idea.id,
                title=db_idea.title,
                description=db_idea.description,
                difficulty=db_idea.difficulty,
                estimated_time=db_idea.estimated_time,
                why_suitable=idea_data.get("why_suitable", "Matches your profile perfectly."),
            ),
            features=FeatureBreakdown(
                core_features=[Feature(**f) for f in data.get("features", {}).get("core_features", [])],
                nice_to_have=[Feature(**f) for f in data.get("features", {}).get("nice_to_have", [])],
            ),
            tech_stack=TechStack(**data.get("tech_stack", {
                "frontend": [], "backend": [], "database": [], "tools": [],
                "reasoning": "Standard tech stack for this project type.",
            })),
            roadmap=Roadmap(
                total_duration=data.get("roadmap", {}).get("total_duration", profile.time_available),
                phases=[Phase(**p) for p in data.get("roadmap", {}).get("phases", [])],
            ),
            learning_path=LearningPath(
                new_technologies=data.get("learning_path", {}).get("new_technologies", []),
                resources=[Resource(**r) for r in data.get("learning_path", {}).get("resources", [])],
            ),
        )

    async def get_full_plan_by_id(self, db: Session, idea_id: int) -> FullProjectPlanResponse | None:
        """Retrieve a full plan from the database by idea ID."""
        db_idea = await self.get_idea_by_id(db, idea_id)
        if not db_idea:
            return None
            
        return FullProjectPlanResponse(
            idea=ProjectIdea(
                id=db_idea.id,
                title=db_idea.title,
                description=db_idea.description,
                difficulty=db_idea.difficulty,
                estimated_time=db_idea.estimated_time,
                why_suitable=db_idea.why_suitable or "Matches your profile perfectly.",
            ),
            features=FeatureBreakdown(
                core_features=[Feature(**f) for f in (db_idea.features or {}).get("core_features", [])],
                nice_to_have=[Feature(**f) for f in (db_idea.features or {}).get("nice_to_have", [])],
            ),
            tech_stack=TechStack(**(db_idea.tech_stack or {
                "frontend": [], "backend": [], "database": [], "tools": [],
                "reasoning": "Standard tech stack based on project type.",
            })),
            roadmap=Roadmap(
                total_duration=(db_idea.roadmap or {}).get("total_duration", db_idea.estimated_time),
                phases=[Phase(**p) for p in (db_idea.roadmap or {}).get("phases", [])],
            ),
            learning_path=LearningPath(
                new_technologies=(db_idea.learning_path or {}).get("new_technologies", []),
                resources=[Resource(**r) for r in (db_idea.learning_path or {}).get("resources", [])],
            ),
        )

idea_service = IdeaService()
