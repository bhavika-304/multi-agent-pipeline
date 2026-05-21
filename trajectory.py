class TrajectoryStep:
    def __init__(self,thought,action,action_input,observation):
        self.thought = thought
        self.action=action
        self.action_input=action_input
        self.observation=observation

class Trajectory:
    def __init__(self,task):
        self.task=task
        self.steps=[]
        self.final_answer=""
        self.success=False
    def add_step(self,thought,action,action_input,observation):
        step=TrajectoryStep(thought,action,action_input,observation)
        self.steps.append(step)



    def log(self):
        print(f"task={self.task}")
        for i , s in enumerate(self.steps,start=1):
            print (f"step {i}:")
            print(f"thought: {s.thought}")
            print(f"action: {s.action}")
            print(f"action_input: {s.action_input}")
            print(f"observation: {s.observation}")
        print(f"final_answer: {self.final_answer}") 
        print(f"success: {self.success}") 