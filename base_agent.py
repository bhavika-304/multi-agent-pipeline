from trajectory import Trajectory
from tool_registry import TOOL_REGISTRY
from llm_client import call_llm

import json


SYSTEM_PROMPT = """
You are an AI agent.

Respond ONLY in valid JSON.

Format:

{
  "thought": "...",
  "action": "...",
  "action_input": {...}
}

Tools:

write_file:
{
  "path": "...",
  "content": "..."
}

read_file:
{
  "path": "..."
}

run_python:
{
  "filepath": "..."
}

When done:

{
  "thought": "...",
  "action": "FINISH",
  "action_input": {
      "answer": "..."
  }
}
"""


class BaseAgent:

    def __init__(
        self,
        system_prompt=None,
        max_steps=8
    ):

        self.system_prompt = (
            system_prompt or SYSTEM_PROMPT
        )

        self.max_steps = max_steps

    def run(self, task):

        trajectory = Trajectory(task)

        messages = [
            {
                "role": "user",
                "content": f"Task: {task}"
            }
        ]

        for step in range(
            self.max_steps
        ):

            raw_response = call_llm(
                messages,
                self.system_prompt
            )

            print(raw_response)

            try:

                parsed = json.loads(
                    raw_response
                )

            except Exception as e:

                print(
                    f"JSON error: {e}"
                )

                break

            thought = parsed["thought"]

            action = parsed["action"]

            action_input = parsed[
                "action_input"
            ]

            if action == "FINISH":

                trajectory.final_answer = (
                    action_input["answer"]
                )

                trajectory.success = True

                break

            if action not in TOOL_REGISTRY:

                observation = (
                    f"{action} not found"
                )

            else:

                observation = TOOL_REGISTRY[
                    action
                ](**action_input)

            trajectory.add_step(
                thought,
                action,
                action_input,
                observation
            )

            messages.append({
                "role": "assistant",
                "content": raw_response
            })

            messages.append({
                "role": "user",
                "content":
                    f"Tool result: {observation}"
            })

        return trajectory