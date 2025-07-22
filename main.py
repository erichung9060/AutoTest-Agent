from langgraph_core import LangGraphTestRunner
from TestRail.utility import get_test_cases_description

from dotenv import load_dotenv
load_dotenv()

project_id = 623
suite_id = 401816
section_id = 16233670

test_runner = LangGraphTestRunner()

print("Generating workflow diagram...")
test_runner.generate_workflow_diagram("workflow_diagram.png")
print()

test_cases = get_test_cases_description(project_id, suite_id, section_id)
for title, description in test_cases.items():
    description = description.replace("green", "blue")
    print(f"Test Case: {title}\nDescription:\n{description}\n")
    
    workflow_result = test_runner.run_test_workflow(title, description)
    
    print(f"=== Workflow Result ===")
    print(f"Status: {workflow_result['status']}")
    print(f"Retry Count: {workflow_result['retry_count']}")
    print(f"Test Result: {workflow_result['test_result']}")
    print(f"Final Result: {workflow_result['final_result']}")
    print()

    break

print("All test cases processed.")