from planner_agent import PlannerAgent
from reviewer_agent import ReviewerAgent
from coder_agent import CoderAgent
from tool_registry import TOOL_REGISTRY
from memory.working_memory import WorkingMemory
from memory.episodic_memory import EpisodicMemory
from memory.semantic_memory import SemanticMemory
from tester_agent import TesterAgent


class Orchestrator:

    def __init__(self):
        self.planner=PlannerAgent()
        self.agents={
            "coder": CoderAgent(),
            "reviewer": ReviewerAgent(),
            "tester": TesterAgent()
        }
        self.working_memory = WorkingMemory()
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()


    def run(self,goal):
        self.goal=goal
        plan=self.planner.plan(goal)
        if not plan:
            print("Planning failed. Exiting.")
            return
        self.tasks=plan["tasks"]
        results={}
        for task in self.tasks:


            task_id=task["id"]
            agent_name=task["agent"]
            description=task["description"]

            context=""
            for dep in task["depends_on"]:
                if dep in results:
                    context+=f"Task {dep} result:\n{results[dep]}\n\n"

            # full_task=description
            # if context:
            #     full_task=context + "\nTask description:\n" + task["description"]

            past_episodic = self.episodic_memory.as_context(description)
            past_semantic = self.semantic_memory.as_context(description)

            full_task = f"Overall goal: {goal}\n\nYour specific task: {description}"

            if context:
                full_task += f"\n\nContext from previous tasks:\n{context}"

            if past_episodic:
                full_task += f"\n\nLESSON FROM PAST RUNS (keyword match):\n{past_episodic}\nIf a past run failed, do NOT repeat that same approach."

            if past_semantic:
                full_task += f"\n\nLESSON FROM SIMILAR TASKS (meaning match):\n{past_semantic}\nUse successful patterns, avoid failed ones."


            agent=self.agents[agent_name]
            print(f"Running task {task_id} with agent {agent_name}")

            trajectory=agent.run(full_task)

            results[task_id] = trajectory.final_answer

            print(f"    Result: {trajectory.final_answer}")
            print(f"    Success: {trajectory.success}")
            self.episodic_memory.save(
                    task=description,
                    agent=agent_name,
                    success=trajectory.success,
                    result=trajectory.final_answer
                )
            self.working_memory.set(
                f"task_{task_id}_result",
                trajectory.final_answer
            )
            self.semantic_memory.save(
                task=description,
                result=trajectory.final_answer,
                success=trajectory.success
            )

        print(f"\n{'='*50}")
        print("ALL TASKS COMPLETE")
        print(f"{'='*50}")
        return results