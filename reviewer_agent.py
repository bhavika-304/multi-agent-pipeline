from base_agent import BaseAgent

REVIEWER_PROMPT = """
You are a code reviewer. You read code and give structured feedback.

You must respond ONLY in valid JSON:
{
  "thought": "...",
  "action": "...",
  "action_input": {...}
}

Available tools:
read_file: {"path": "..."}

When done, use FINISH with this answer format:
{
  "answer": {
    "quality": "good/bad",
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1"]
  }
}
"""


class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=REVIEWER_PROMPT)