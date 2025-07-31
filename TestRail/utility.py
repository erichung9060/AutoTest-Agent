from dotenv import load_dotenv
load_dotenv()

try:
    from TestRail.restfulwebservice import  APIClient,APIError
except ImportError:
    from restfulwebservice import APIClient, APIError
import json
import os
from datetime import datetime

client = APIClient(os.environ.get('TESTRAIL_URL'))
client.user = os.environ.get('TESTRAIL_EMAIL')
client.password = os.environ.get('TESTRAIL_API_KEY')

def create_new_run(suite_id):
    suit_data = client.get_suite(suite_id)['data']
    project_id = suit_data['project_id']
    name = suit_data['name'] + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    run_data = {
        "name": name,
        "suite_id": suite_id,
        # "include_all": False,
        # "case_ids": [332622135, 332622136, 332622137]
    }
    run_id = client.add_run(project_id, run_data)['data']['id']
    return run_id

def get_test_cases_description(run_id):
    print(f"Fetching test cases for run ID: {run_id}")
    
    test_cases = client.get_tests(run_id)
    result = {}
    for case in test_cases['data']:
        try:
            title = case['title']
            steps = case['custom_steps'].replace('\n', ', ').replace('\r', '')
            expected = case['custom_expected'].replace('\n', ', ').replace('\r', '')

            description = f"Steps: {steps}, \nExpected: {expected}"
            result[title] = {"description": description, "case_id": case['case_id']}
            print(f"✅ Successfully fetched case {case['title']}")
        except Exception as e:
            print(f"❌ Error for case: {case['title']}: {e}")

    return result

def upload_test_case_result(run_id, case_id, workflow_result):
    print(f"Uploading test results for run ID: {run_id}, Case ID: {case_id}")

    results = {
    "status_id": 1 if workflow_result['passed'] else 5,
    "comment": f"""
{workflow_result['judge_result']}
--------------------------------
{workflow_result['run_result']}
"""}

    response = client.add_result_for_case(run_id, case_id, results)
    if response['code'] == 0:
        print("✅ Test results uploaded successfully.")

        result_id = response['data']['id']
        screenshot_path = os.path.join('screenshots', workflow_result['screenshot_path'])
        
        print(f"📸 Uploading screenshot: {screenshot_path}")
        attachment_response = client.add_attachment_to_result(result_id, screenshot_path)
        if attachment_response:
            print("✅ Screenshot uploaded successfully.")
        else:
            print("❌ Failed to upload screenshot.")
        
    else:
        print("❌ Failed to upload test results:", response)
