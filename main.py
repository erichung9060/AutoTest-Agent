from agents.runtest import RunTestAgent
from agents.judge import JudgeAgent

from TestRail.utility import get_test_cases_description

from dotenv import load_dotenv
load_dotenv()

project_id = 623
suite_id = 401816
section_id = 16233670

run_test_agent = RunTestAgent()
judge_agent = JudgeAgent()

test_cases = get_test_cases_description(project_id, suite_id, section_id)
for title, description in test_cases.items():
    description = description.replace("green", "blue")
    print(f"Test Case: {title}\nDescription:\n{description}\n")
    
    run_result = run_test_agent.run(title, description)
    print(f"=== Result ===\n{run_result}\n")
    
    judge_result = judge_agent.judge_test_result(title, description, run_result)
    print(f"=== Judge Result ===\n{judge_result}\n")

    break

print("All test cases processed.")