import os
import json
import subprocess
import importlib.util

from orchestrator import Orchestrator
from tasks import TASKS
from llm_client import call_llm


# CHECK FUNCTION CORRECTNESS

def check_correctness(check):

    module_name = check["import_from"]

    function_name = check["function"]

    test_cases = check["test_cases"]
    #tasks.py mei se function import karna, phir us function ko test cases ke against run karna, aur count karna ki kitne pass hue


    try:

        spec = importlib.util.spec_from_file_location(
            module_name,
            f"{module_name}.py"
        )
#for dynamic loading of the module the agent creates , dyanamic coz its happening at runtime
        module = importlib.util.module_from_spec(spec)
#create an empty module object to sore the file 
        spec.loader.exec_module(module)#run the module

        func = getattr(
            module,
            function_name
        )
#get function name 
    except Exception as e:

        return {
            "passed": 0,
            "total": len(test_cases),
            "error": str(e)
        }

    passed = 0

    for case in test_cases:

        try:#for each test case call the function with the args and compare with expected output, count how many passed

            result = func(
                *case["args"]
            )# * is for unpacking the list of arguments

            if result == case["expected"]:

                passed += 1

        except Exception:

            pass

    return {
        "passed": passed,
        "total": len(test_cases),
        "error": None
    }



# LLM CODE REVIEW

def llm_judge(goal, code):

    prompt = f"""
Goal:
{goal}

Code:
{code}

Return ONLY valid JSON:

{{
  "score": 8,
  "correct": true,
  "issues": [],
  "summary": "short review"
}}
"""

    try:

        response = call_llm(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            system_prompt="You are a code reviewer.return valid json only , no markdowns"
        )

        return json.loads(
            response
        )

    except Exception as e:

        return {
            "score": 0,
            "correct": False,
            "issues": ["judge failed"],
            "summary": str(e)
        }


# =========================
# MAIN EVAL LOOP
# =========================
def run_evals():

    orchestrator = Orchestrator()

    passed = 0

    failed = 0

    results = []

    for task in TASKS:

        task_id = task["id"]

        goal = task["goal"]

        expected_file = task["expected_file"]

        print(f"\nRunning task {task_id}")

        try:

            # run agents
            orchestrator.run(goal)

            # LEVEL 1
            # did file get created?

            file_exists = os.path.exists(
                expected_file
            )

            # LEVEL 2
            # does file run?

            run_ok = False

            if file_exists:

                result = subprocess.run(
                    ["python3", expected_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                run_ok = (
                    result.returncode == 0
                )

            # LEVEL 3
            # is logic correct?

            correctness = {
                "passed": 0,
                "total": 0
            }

            if file_exists and "check" in task:

                correctness = (
                    check_correctness(
                        task["check"]
                    )
                )

            # LEVEL 4
            # ask another LLM

            judge = {
                "score": 0,
                "summary": "not checked"
            }

            if file_exists:

                with open(
                    expected_file,
                    "r"
                ) as f:

                    code = f.read()

                judge = llm_judge(
                    goal,
                    code
                )

            # FINAL DECISION

            correctness_ok = (
                correctness["total"] > 0
                and

                correctness["passed"]
                ==
                correctness["total"]
            )

            if not file_exists:

                status = "FAILED"

                reason = (
                    "file not created"
                )

            elif not run_ok:

                status = "FAILED"

                reason = (
                    "file crashes"
                )

            elif not correctness_ok:

                status = "FAILED"

                reason = (
                    "wrong answers"
                )

            else:

                status = "PASSED"

                reason = None

            # metrics

            if status == "PASSED":

                passed += 1

            else:

                failed += 1

            print(
                f"Status: {status}"
            )

            # save result

            results.append({

                "task_id": task_id,

                "status": status,

                "reason": reason,

                "correctness": correctness,

                "judge": judge
            })

        except Exception as e:

            failed += 1

            print(f"CRASHED: {e}")

    # SAVE REPORT

    with open(
        "eval_report.json",
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )

    # SUMMARY

    print("\n==========")

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Score: "
        f"{round(passed/len(TASKS)*100)}%"
    )

    print("==========")


if __name__ == "__main__":

    run_evals()

# import os

# from orchestrator import Orchestrator
# from tasks import TASKS


# def run_evals():

#     orchestrator = Orchestrator()

#     passed = 0

#     for task in TASKS:

#         goal = task["goal"]

#         expected_file = (
#             task["expected_file"]
#         )

#         print(f"\nRunning: {goal}")

#         try:

#             orchestrator.run(goal)

#             if os.path.exists(
#                 expected_file
#             ):

#                 print("PASSED")

#                 passed += 1

#             else:

#                 print("FAILED")

#         except Exception as e:

#             print(f"CRASHED: {e}")

#     print("\n================")

#     print(
#         f"Passed: {passed}/{len(TASKS)}"
#     )

#     print("================")


# if __name__ == "__main__":

#     run_evals()