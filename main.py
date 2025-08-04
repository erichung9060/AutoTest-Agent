from dotenv import load_dotenv
load_dotenv()

import os
from langgraph_core import LangGraphTestRunner
from TestRail.utility import get_test_cases_description, upload_test_case_result, create_new_run

from agents.setup import SetupAgent
setup_agent = SetupAgent()
result = setup_agent.run()

test_runner = LangGraphTestRunner()
# test_runner.generate_workflow_diagram("workflow_diagram.png")

suite_id = os.environ.get('SUITE_ID')
run_id = create_new_run(suite_id)
test_cases = get_test_cases_description(run_id)

results = []
for title, case in test_cases.items():
    print(f"=== Running Test Case: {title} ===")
    print(f"Description:\n{case['description']}\n")

    workflow_result = test_runner.run_test_workflow(title, case['description'])
    result = {"title": title, "passed": workflow_result['passed']}
    results.append(result)
    
    upload_test_case_result(run_id, case['case_id'], workflow_result)
    # TODO: reset node
    # break

print("=== All Test Case Results ===")
for result in results:
    print(f"{'✅' if result['passed'] else '❌'}: {result['title']}")

