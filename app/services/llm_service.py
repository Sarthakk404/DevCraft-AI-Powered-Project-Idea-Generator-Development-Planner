import json
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas.idea import (
    UserProfileRequest, 
    ProjectIdea, 
    FeatureBreakdown, 
    Feature,
    TechStack,
    Roadmap,
    Phase,
    LearningPath,
    Resource
)

settings = get_settings()


class LLMService:
    """Service for interacting with Google Gemini API using the new SDK."""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model
    
    def _generate_json(self, prompt: str) -> dict:
        """Generate JSON response from LLM with simple retry logic."""
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                result = json.loads(response.text)
                print(f"DEBUG: Gemini JSON Response: {json.dumps(result, indent=2)}")
                return result
            except Exception as e:
                error_str = str(e)
                # Check for rate limit or overload errors
                if attempt < max_retries - 1 and ("429" in error_str or "ResourceExhausted" in error_str or "retry" in error_str.lower()):
                    wait_time = (attempt + 1) * 15  # 15s, 30s, 45s
                    print(f"Rate limit hit. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                    
                print(f"LLM Generation Error: {e}")
                if attempt == max_retries - 1:
                    print(f"CRITICAL: Failed to parse Gemini response as JSON. RAW TEXT: {response.text}")
                    raise RuntimeError(f"Failed to generate valid JSON from Gemini after {max_retries} attempts: {e}")
    
    async def generate_project_ideas(self, profile: UserProfileRequest) -> list[ProjectIdea]:
        """Generate personalized project ideas based on user profile."""
        
        # Ensure goal is treated as string for the prompt
        goal_str = str(profile.goal)

        prompt = f"""You are an expert software development mentor. Generate {settings.max_ideas} unique and creative project ideas based on this user profile:

**User Profile:**
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience Level: {profile.experience_level.value}
- Goal: {goal_str}
- Time Available: {profile.time_available}
- Preferences: {profile.preferences or 'None specified'}

**Requirements:**
1. Ideas should match the user's skill level
2. Ideas should align with their interests
3. Projects should be completable within the time available
4. For "{goal_str}" goal, focus on projects that match this specific goal type.

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Project Title",
    "description": "2-3 sentence description of what the project does",
    "difficulty": "Beginner|Intermediate|Advanced",
    "estimated_time": "X days/weeks",
    "why_suitable": "Why this project is perfect for this user"
  }}
]
"""
        ideas_data = self._generate_json(prompt)
        return [ProjectIdea(**idea) for idea in ideas_data]
    
    async def generate_features(self, idea: ProjectIdea, profile: UserProfileRequest) -> FeatureBreakdown:
        """Generate feature breakdown for a project idea."""
        
        prompt = f"""You are a product manager. Break down this project into features:

**Project:** {idea.title}
**Description:** {idea.description}
**User Experience Level:** {profile.experience_level.value}
**Time Available:** {profile.time_available}

Create a feature breakdown with:
1. Core features (must-have for MVP)
2. Nice-to-have features (can add later)

Return ONLY JSON with this structure:
{{
  "core_features": [
    {{"name": "Feature Name", "description": "What it does", "priority": "core"}}
  ],
  "nice_to_have": [
    {{"name": "Feature Name", "description": "What it does", "priority": "nice-to-have"}}
  ]
}}
"""
        data = self._generate_json(prompt)
        
        return FeatureBreakdown(
            core_features=[Feature(**f) for f in data["core_features"]],
            nice_to_have=[Feature(**f) for f in data["nice_to_have"]]
        )
    
    async def recommend_tech_stack(self, idea: ProjectIdea, profile: UserProfileRequest) -> TechStack:
        """Recommend technology stack based on user skills and project needs."""
        
        prompt = f"""You are a senior software architect. Recommend a tech stack for:

**Project:** {idea.title}
**Description:** {idea.description}
**User's Current Skills:** {', '.join(profile.skills)}
**Experience Level:** {profile.experience_level.value}
**Goal:** {profile.goal}

Guidelines:
1. Prefer technologies the user already knows when possible
2. Suggest 1-2 new technologies to learn (not too many)
3. Keep it simple for beginners, more options for advanced
4. Consider the project requirements

Return ONLY JSON:
{{
  "frontend": ["Technology1", "Technology2"],
  "backend": ["Technology1"],
  "database": ["Database1"],
  "tools": ["Tool1", "Tool2"],
  "reasoning": "Brief explanation of why these choices"
}}
"""
        data = self._generate_json(prompt)
        return TechStack(**data)
    
    async def create_roadmap(
        self, 
        idea: ProjectIdea, 
        features: FeatureBreakdown, 
        tech_stack: TechStack,
        profile: UserProfileRequest
    ) -> Roadmap:
        """Create a development roadmap with phases and tasks."""
        
        core_feature_names = [f.name for f in features.core_features]
        
        prompt = f"""You are a project manager. Create a development roadmap for:

**Project:** {idea.title}
**Time Available:** {profile.time_available}
**Core Features to Build:** {', '.join(core_feature_names)}
**Tech Stack:** Frontend: {tech_stack.frontend}, Backend: {tech_stack.backend}, Database: {tech_stack.database}

Create a phased roadmap that:
1. Starts with setup and foundation
2. Builds features incrementally
3. Ends with testing and polish
4. Fits within the time available

Return ONLY JSON:
{{
  "total_duration": "X weeks",
  "phases": [
    {{
      "phase_number": 1,
      "title": "Phase Title",
      "duration": "X days",
      "tasks": ["Task 1", "Task 2"],
      "deliverables": ["What's completed"]
    }}
  ]
}}
"""
        data = self._generate_json(prompt)
        
        return Roadmap(
            total_duration=data["total_duration"],
            phases=[Phase(**p) for p in data["phases"]]
        )
    
    async def create_learning_path(
        self, 
        tech_stack: TechStack, 
        profile: UserProfileRequest
    ) -> LearningPath:
        """Create a learning path for technologies the user doesn't know."""
        
        known_skills = set(skill.lower() for skill in profile.skills)
        all_tech = tech_stack.frontend + tech_stack.backend + tech_stack.database + tech_stack.tools
        new_tech = [t for t in all_tech if t.lower() not in known_skills]
        
        if not new_tech:
            return LearningPath(new_technologies=[], resources=[])
        
        prompt = f"""You are a learning advisor. Create a learning path for:

**Technologies to Learn:** {', '.join(new_tech)}
**User's Current Skills:** {', '.join(profile.skills)}
**Experience Level:** {profile.experience_level.value}
**Time Available:** {profile.time_available}

For each technology, suggest 2-3 learning resources (mix of videos, articles, docs).
Prioritize free resources. Order from basics to advanced.

Return ONLY JSON:
{{
  "new_technologies": ["Tech1", "Tech2"],
  "resources": [
    {{
      "topic": "Technology Name",
      "resource_type": "video|article|course|documentation",
      "title": "Resource Title",
      "url": "https://...",
      "estimated_time": "X hours"
    }}
  ]
}}
"""
        data = self._generate_json(prompt)
        
        return LearningPath(
            new_technologies=data["new_technologies"],
            resources=[Resource(**r) for r in data["resources"]]
        )


    async def generate_complete_plan_one_shot(self, profile: UserProfileRequest) -> dict:
        """Generate the entire project plan in a single LLM call to save API requests."""
        
        goal_str = str(profile.goal)
        
        prompt = f"""You are an expert software architect. Create a COMPLETE, detailed project development plan for a user with this profile:

**User Profile:**
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience Level: {profile.experience_level.value}
- Goal: {goal_str}
- Time Available: {profile.time_available}
- Preferences: {profile.preferences or 'None specified'}

**Constraint:** The project must be fully completable within EXACTLY {profile.time_available} and suitable for a {profile.experience_level.value} developer.

**CRITICAL INSTRUCTION ON TIME:**
If the user says "2 months", the roadmap MUST span 2 months. Do NOT create a 2-week roadmap for a 2-month available time. Use the full time availability to create a more in-depth, polished project.

Generate a single JSON object containing:
1. One perfect project idea
2. Feature breakdown (Core vs Nice-to-have)
3. Tech Stack recommendations
4. A detailed Roadmap (Phased, adhering strictly to the time limit)
5. Learning Path for new technologies

Return ONLY JSON with this structure:
{{
  "idea": {{
    "title": "Project Title",
    "description": "Description",
    "difficulty": "Beginner|Intermediate|Advanced",
    "estimated_time": "{profile.time_available}",
    "why_suitable": "Why this fits"
  }},
  "features": {{
    "core_features": [{{"name": "Feature Name", "description": "Short description", "priority": "core"}}],
    "nice_to_have": [{{"name": "Feature Name", "description": "Short description", "priority": "nice-to-have"}}]
  }},
  "tech_stack": {{
    "frontend": ["Tech"], "backend": ["Tech"], "database": ["Tech"], "tools": ["Tech"], "reasoning": "Why"
  }},
  "roadmap": {{
    "total_duration": "{profile.time_available}",
    "phases": [
      {{ "phase_number": 1, "title": "Phase", "duration": "Duration", "tasks": ["Task"], "deliverables": ["Items"] }}
    ]
  }},
  "learning_path": {{
    "new_technologies": ["Tech"],
    "resources": [
      {{ "topic": "Tech", "resource_type": "video", "title": "Title", "url": "https://...", "estimated_time": "Hours" }}
    ]
  }}
}}
"""
        return self._generate_json(prompt)


# Singleton instance
llm_service = LLMService()
