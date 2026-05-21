# Multi-Agent Software Engineering Pipeline

Built from scratch in Python. No LangChain. No CrewAI. No shortcuts.

## What it does

You give it a goal in plain English.
It automatically plans, writes, tests, and reviews code.

Input:
"write a function that adds two numbers"

What happens:
1. Planner breaks it into subtasks
2. Coder writes the Python file and runs it
3. Tester writes and runs tests
4. Reviewer critiques the code
5. Eval harness scores everything automatically
6. plus ive added the memory architecture:short term:working mem, long term:episodic mem, andd semantic memory 

## Why did i build it from scratch?

Most people use LangChain or CrewAI which hides
everything. I built the ReAct loop myself so I could
understand every decision the agent makes.
That understanding is what lets me debug it,
improve it, and explain it.

## Architecture
## Architecture

```text
type a goal
      ↓
orchestrator.py
      ↓
planner_agent.py
      ↓
orchestrator loops through tasks and calls:

  ├── coder_agent.py
  │     writes and runs code

  ├── tester_agent.py
  │     writes and runs tests

  └── reviewer_agent.py
        reads and critiques code


every agent uses:

  ├── base_agent.py
  │     shared ReAct loop / base class

  ├── llm_client.py
  │     Groq API calls

  └── tool_registry.py
        write_file, read_file, run_python


after each task:

  ├── memory/working_memory.py
  │     short-term context

  ├── memory/episodic_memory.py
  │     SQLite memory storage

  └── memory/semantic_memory.py
        ChromaDB vector memory



separately:
  eval_runner.py       ← runs 5 tasks and scores everything, what passed , what failed
  tasks.py             ← the list of test goals


  ## How to run

```bash
# setup
pip install groq python-dotenv chromadb sentence-transformers
echo 'GROQ_API_KEY=your_key_here' > .env

# run a single goal
python3 -c "
from orchestrator import Orchestrator
o = Orchestrator()
o.run('wtv task u want it to code ')
"

# run full evaluation using tasks.py ka task list 
python3 eval_runner.py
```
