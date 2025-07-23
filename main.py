from dotenv import load_dotenv
load_dotenv()

from langgraph_core import LangGraphTestRunner
from TestRail.utility import get_test_cases_description

project_id = 623
suite_id = 401816
section_id = 16233670

test_runner = LangGraphTestRunner()

print("Generating workflow diagram...")
test_runner.generate_workflow_diagram("workflow_diagram.png")
print()

test_cases = get_test_cases_description(project_id, suite_id, section_id)
results = []

for title, description in test_cases.items():
    print(f"Test Case: {title}\nDescription:\n{description}\n")
    
    workflow_result = test_runner.run_test_workflow(title, description)
    
    result_entry = {
        "title": title,
        "passed": workflow_result["passed"],
    }
    results.append(result_entry)
    # reset node

print("=== All Test Case Results ===")
for entry in results:
    print(f"{'✅' if entry['passed'] else '❌'}: {entry['title']}")
