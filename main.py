from dotenv import load_dotenv
load_dotenv()

from langgraph_core import LangGraphTestRunner
from TestRail.utility import get_test_cases_description, upload_test_results

run_id = 808849

test_runner = LangGraphTestRunner()
# print("Generating workflow diagram...")
# test_runner.generate_workflow_diagram("workflow_diagram.png")

test_cases = get_test_cases_description(run_id)
results = []

for title, case in test_cases.items():
    print(f"Test Case: {title}\nDescription:\n{case['description']}\n")

    workflow_result = test_runner.run_test_workflow(title, case['description'])

    result_entry = {
        "title": title,
        "case_id": case['case_id'],
        "status_id": 1 if workflow_result['passed'] else 5,
    }
    results.append(result_entry)
    # reset node
    # break

print("=== All Test Case Results ===")
for result in results:
    print(f"{'✅' if result['status_id'] == 1 else '❌'}: {result['title']}")

upload_test_results(run_id, results)