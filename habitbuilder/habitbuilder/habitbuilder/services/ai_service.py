import json
import anthropic
from dataclasses import dataclass


@dataclass
class HabitPlan:
    identity_statement: str
    habits: list[dict]


SYSTEM_PROMPT = """You are a habit coach applying the Atomic Habits framework by James Clear.
Given a user's goal, return ONLY a valid JSON object with this exact structure:
{
  "identity_statement": "I am someone who...",
  "habits": [
    {
      "title": "Short habit label (max 8 words)",
      "two_min_version": "2-minute fallback version of this habit",
      "cue": "After I [existing habit], I will [new habit]"
    }
  ]
}

Rules:
- Return exactly 3 habits derived from the goal
- Apply the 2-minute rule: each habit must have a version completable in 2 minutes
- Use implementation intentions for cues: "After I [anchor habit], I will [new habit]"
- The identity statement must start with "I am someone who"
- Return ONLY the JSON object — no preamble, no explanation, no markdown fences"""


class AIService:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)

    def breakdown_goal(self, goal: str) -> HabitPlan:
        """
        Call Claude API once to break a user goal into a structured habit plan.
        This is the only AI call in the entire application.
        """
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f"My goal: {goal}"}
            ]
        )

        raw = response.content[0].text.strip()
        data = json.loads(raw)

        return HabitPlan(
            identity_statement=data["identity_statement"],
            habits=data["habits"]
        )
