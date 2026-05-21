from base_agent import BaseAgent


agent = BaseAgent()

result = agent.run(
    "Create a Python file hello.py that prints hello world and run it"
)

result.log()