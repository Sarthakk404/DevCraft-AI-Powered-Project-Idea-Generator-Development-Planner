import logging
import json
import asyncio
from groq import AsyncGroq
from app.config import get_settings
from app.schemas.idea import UserProfileRequest, ProjectIdea

settings = get_settings()
logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Groq Llama API."""

    def __init__(self):
        self._client = None

    @property
    def client(self):
        """Lazy-init the Groq client."""
        if self._client is None:
            if not settings.groq_api_key:
                raise RuntimeError(
                    "GROQ_API_KEY is not set. Add it to your .env file."
                )
            self._client = AsyncGroq(api_key=settings.groq_api_key)
        return self._client

    async def _generate_json(self, prompt: str) -> dict:
        """Generate JSON response from Groq with retry logic."""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=settings.groq_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.9,
                )
                content = response.choices[0].message.content
                result = json.loads(content)
                logger.info("Groq returned valid JSON response")
                return result

            except Exception as e:
                logger.error(f"LLM generation error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                    continue

                raise RuntimeError(
                    f"Failed to generate valid JSON from Groq after {max_retries} attempts: {e}"
                )

    async def generate_project_ideas(
        self, profile: UserProfileRequest
    ) -> list[ProjectIdea]:
        """Generate personalized project ideas based on user profile."""
        goal_str = str(profile.goal)

        prompt = f"""You are an expert software mentor and project architect.

Generate exactly {settings.max_ideas} unique and creative project ideas for this developer:

**Developer Profile:**
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience Level: {profile.experience_level.value}
- Goal: {goal_str}
- Time Available: {profile.time_available}
- Preferences: {profile.preferences or 'None specified'}

**Requirements:**
- Each idea must match the developer's experience level
- Ideas should align with their interests and leverage their skills
- Projects must be completable within {profile.time_available}
- Include a mix of practical and creative ideas
- Each idea should be distinct from the others

Return a JSON object with this exact structure:
{{
  "ideas": [
    {{
      "title": "Short, catchy project title",
      "description": "2-3 sentence description of what the project does and its value",
      "difficulty": "Beginner|Intermediate|Advanced",
      "estimated_time": "Realistic time estimate",
      "why_suitable": "1-2 sentences on why this matches the developer's profile"
    }}
  ]
}}"""
        data = await self._generate_json(prompt)
        return [ProjectIdea(**idea) for idea in data.get("ideas", [])]

    async def generate_complete_plan_one_shot(
        self, profile: UserProfileRequest
    ) -> dict:
        """Generate the entire project plan in a single LLM call."""
        goal_str = str(profile.goal)

        prompt = f"""You are an expert software architect. Create a COMPLETE project plan.

**Developer Profile:**
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience Level: {profile.experience_level.value}
- Goal: {goal_str}
- Time Available: {profile.time_available}
- Preferences: {profile.preferences or 'None specified'}

**Constraint:** The project must be fully completable in {profile.time_available}.
Ensure "frontend" technologies strictly refer to client-side frameworks/libraries (e.g., React, Vue, HTML/CSS) and not backend frameworks (e.g., Flask, Django).
CRITICAL: Do NOT hallucinate specific URLs for learning resources. For videos/courses, provide a valid YouTube search URL (e.g., 'https://www.youtube.com/results?search_query=React+Tutorial'). For generic documentation, use ONLY canonical root domains (e.g., 'https://react.dev').

Return ONLY a JSON object with this exact structure:
{{
  "idea": {{
    "title": "Project Title",
    "description": "Detailed description",
    "difficulty": "Beginner|Intermediate|Advanced",
    "estimated_time": "{profile.time_available}",
    "why_suitable": "Why this fits the developer"
  }},
  "features": {{
    "core_features": [{{ "name": "Feature Name", "description": "What it does", "priority": "core" }}],
    "nice_to_have": [{{ "name": "Feature Name", "description": "What it does", "priority": "nice-to-have" }}]
  }},
  "tech_stack": {{
    "frontend": ["Technology"],
    "backend": ["Technology"],
    "database": ["Technology"],
    "tools": ["Technology"],
    "reasoning": "Why this stack was chosen"
  }},
  "roadmap": {{
    "total_duration": "{profile.time_available}",
    "phases": [{{
      "phase_number": 1,
      "title": "Phase Title",
      "duration": "Time for this phase",
      "tasks": ["Specific task 1", "Specific task 2"],
      "deliverables": ["What's delivered"]
    }}]
  }},
  "learning_path": {{
    "new_technologies": ["Tech to learn"],
    "resources": [{{
      "topic": "Technology",
      "resource_type": "video|article|course|documentation",
      "title": "Resource Title",
      "url": "https://...",
      "estimated_time": "Time to complete"
    }}]
  }}
}}"""
        return await self._generate_json(prompt)

    async def expand_idea_to_full_plan(
        self, profile: UserProfileRequest, selected_idea: dict
    ) -> dict:
        """Generate a full project plan for a specific selected idea."""
        goal_str = str(profile.goal)

        prompt = f"""You are an expert software architect. The developer has chosen a project idea.
Create a COMPLETE development plan for this specific project.

**Developer Profile:**
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience Level: {profile.experience_level.value}
- Goal: {goal_str}
- Time Available: {profile.time_available}
- Preferences: {profile.preferences or 'None specified'}

**Selected Project:**
- Title: {selected_idea['title']}
- Description: {selected_idea['description']}
- Difficulty: {selected_idea.get('difficulty', 'Intermediate')}
- Estimated Time: {selected_idea.get('estimated_time', profile.time_available)}

**Constraint:** The plan must be achievable within {profile.time_available}.
Ensure "frontend" technologies strictly refer to client-side frameworks/libraries (e.g., React, Vue, HTML/CSS) and not backend frameworks (e.g., Flask, Django).
CRITICAL: Do NOT hallucinate specific URLs for learning resources. For videos/courses, provide a valid YouTube search URL (e.g., 'https://www.youtube.com/results?search_query=React+Tutorial'). For generic documentation, use ONLY canonical root domains (e.g., 'https://react.dev').

Return ONLY a JSON object with this exact structure:
{{
  "idea": {{
    "title": "{selected_idea['title']}",
    "description": "{selected_idea['description']}",
    "difficulty": "{selected_idea.get('difficulty', 'Intermediate')}",
    "estimated_time": "{selected_idea.get('estimated_time', profile.time_available)}",
    "why_suitable": "Why this project fits the developer"
  }},
  "features": {{
    "core_features": [{{ "name": "Feature Name", "description": "Detailed description of the feature", "priority": "core" }}],
    "nice_to_have": [{{ "name": "Feature Name", "description": "Detailed description", "priority": "nice-to-have" }}]
  }},
  "tech_stack": {{
    "frontend": ["Technology"],
    "backend": ["Technology"],
    "database": ["Technology"],
    "tools": ["Tool"],
    "reasoning": "Detailed explanation of why this stack was chosen for this specific project"
  }},
  "roadmap": {{
    "total_duration": "{profile.time_available}",
    "phases": [{{
      "phase_number": 1,
      "title": "Phase Title",
      "duration": "Duration",
      "tasks": ["Specific task"],
      "deliverables": ["Deliverable"]
    }}]
  }},
  "learning_path": {{
    "new_technologies": ["Technologies the developer needs to learn"],
    "resources": [{{
      "topic": "Technology",
      "resource_type": "video|article|course|documentation",
      "title": "Resource Title",
      "url": "https://...",
      "estimated_time": "Time estimate"
    }}]
  }}
}}"""
        return await self._generate_json(prompt)


# Singleton instance
llm_service = LLMService()
