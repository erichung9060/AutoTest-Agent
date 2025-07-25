from dotenv import load_dotenv
load_dotenv()

import os
from langgraph_core import LangGraphTestRunner
from TestRail.utility import get_test_cases_description, upload_test_case_result, create_new_run

test_runner = LangGraphTestRunner()
test_runner.generate_workflow_diagram("workflow_diagram.png")

suite_id = os.environ.get('SUITE_ID')
run_id = create_new_run(suite_id)
test_cases = get_test_cases_description(run_id)

results = []
for title, case in test_cases.items():
    print(f"=== Running Test Case: {title} ===")
    print(f"Description:\n{case['description']}\n")

    workflow_result = test_runner.run_test_workflow(title, case['description'])

    result_entry = {
        "title": title,
        "status_id": 1 if workflow_result['passed'] else 5,
        "comment": workflow_result['judge_result'],
    }
    results.append(result_entry)
    # TODO: reset node

    upload_test_case_result(run_id, case['case_id'], result_entry)
    # break

print("=== All Test Case Results ===")
for result in results:
    print(f"{'✅' if result['status_id'] == 1 else '❌'}: {result['title']}")

