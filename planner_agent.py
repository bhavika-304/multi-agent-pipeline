from llm_client import call_llm
import json

PLANNER_PROMPT = """
You are a planning agent.
Your only job is to break a goal into tasks.

Respond ONLY in this JSON format:
{
  "goal": "the original goal",
  "tasks": [
    {"id": 1, "description": "first task", "agent": "coder", "depends_on": []},
    {"id": 2, "description": "second task", "agent": "tester", "depends_on": [1]},
    {"id": 3, "description": "verify everything works", "agent": "coder", "depends_on": [2]}
  ]
}

Rules:
- agent must be one of: coder, reviewer, tester
- depends_on lists which task ids must finish first
- always end with a verification task
- every task description must include the FULL goal details
- never write vague tasks like "design the function" — always say "write a multiply function that takes two numbers and returns their product, save to multiply.py"
- output ONLY the JSON, nothing else
- Keep plans minimal
- Use maximum 3 tasks unless absolutely necessary
"""

class PlannerAgent:

    def plan(self, goal):
        messages = [
            {"role": "user", "content": f"Goal: {goal}"}
        ]

        for attempt in range(3):
            response = call_llm(messages, PLANNER_PROMPT)

            try:
                plan = json.loads(response.strip())
                print(f"Plan created with {len(plan['tasks'])} tasks")
                return plan

            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": "Invalid JSON. Reply with ONLY the JSON object."})

        print("Planner failed after 3 attempts")
        return None