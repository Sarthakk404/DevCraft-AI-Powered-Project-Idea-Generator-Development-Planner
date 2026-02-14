import logging
import json
import asyncio
from openai import AsyncOpenAI
from app.config import get_settings
from app.schemas.idea import (
    UserProfileRequest,
    ProjectIdea,
)

settings = get_settings()
logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with Groq API (OpenAI-compatible)."""

    def __init__(self):
        self._client = None
        self.model = settings.groq_model

    @property
    def client(self):
        """Lazy-init the Groq client."""
        if self._client is None:
            if not settings.groq_api_key:
                raise RuntimeError(
                    "GROQ_API_KEY is not set. Add it to your .env file."
                )
            self._client = AsyncOpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            )
        return self._client

    async def _generate_json(self, prompt: str) -> dict:
        """Generate JSON response from Groq with retry logic."""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert project architect. Always return valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
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

    async def generate_project_ideas(self, profile: UserProfileRequest) -> list[ProjectIdea]:
        """Generate personalized project ideas based on user profile."""
        goal_str = str(profile.goal)

        prompt = f"""Expert mentor. Generate {settings.max_ideas} project ideas:
User: {', '.join(profile.skills)} | {', '.join(profile.interests)} | {profile.experience_level.value} | {goal_str} | {profile.time_available}
Prefs: {profile.preferences or 'None'}

Reqs: Match level/interests, completable in {profile.time_available}.
JSON array ONLY:
{{
  "ideas": [
    {{
      "title": "Title",
      "description": "2-3 sentences",
      "difficulty": "Beginner|Intermediate|Advanced",
      "estimated_time": "Duration",
      "why_suitable": "Reasoning"
    }}
  ]
}}"""
        data = await self._generate_json(prompt)
        return [ProjectIdea(**idea) for idea in data.get("ideas", [])]

    async def generate_complete_plan_one_shot(self, profile: UserProfileRequest) -> dict:
        """Generate the entire project plan in a single LLM call."""
        goal_str = str(profile.goal)

        prompt = f"""Expert architect. Create COMPLETE plan. 
User: {', '.join(profile.skills)} | {', '.join(profile.interests)} | {profile.experience_level.value} | Goal: {goal_str} | Time: {profile.time_available}
Prefs: {profile.preferences or 'None'}

Constraint: Fully completable in {profile.time_available}. 
Return ONLY JSON:
{{
  "idea": {{ "title": "Title", "description": "Desc", "difficulty": "Level", "estimated_time": "{profile.time_available}", "why_suitable": "Why" }},
  "features": {{
    "core_features": [{{ "name": "Name", "description": "Desc", "priority": "core" }}],
    "nice_to_have": [{{ "name": "Name", "description": "Desc", "priority": "nice-to-have" }}]
  }},
  "tech_stack": {{ "frontend": ["Tech"], "backend": ["Tech"], "database": ["Tech"], "tools": ["Tech"], "reasoning": "Why" }},
  "roadmap": {{ "total_duration": "{profile.time_available}", "phases": [{{ "phase_number": 1, "title": "Phase", "duration": "Duration", "tasks": ["Task"], "deliverables": ["Items"] }}] }},
  "learning_path": {{ "new_technologies": ["Tech"], "resources": [{{ "topic": "Tech", "resource_type": "video", "title": "Title", "url": "URL", "estimated_time": "Hours" }}] }}
}}"""
        return await self._generate_json(prompt)

# Singleton instance
llm_service = LLMService()
