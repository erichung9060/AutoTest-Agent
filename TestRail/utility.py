from TestRail.restfulwebservice import  APIClient,APIError
import json
import os

from dotenv import load_dotenv
load_dotenv()

client = APIClient(os.environ.get('TESTRAIL_URL'))
client.user = os.environ.get('TESTRAIL_EMAIL')
client.password = os.environ.get('TESTRAIL_API_KEY')

# print(json.dumps(client.get_sections(623,401816), indent=2))
# print(json.dumps(client.get_cases(623, 401816, 16233670), indent=2))
# print(json.dumps(client.get_tests(808849), indent=2))

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

def upload_test_case_result(run_id, case_id, results):
    print(f"Uploading test results for run ID: {run_id}, Case ID: {case_id}")

    response = client.add_result_for_case(run_id, case_id, results)
    if response['code'] == 0:
        print("✅ Test results uploaded successfully.")
    else:
        print("❌ Failed to upload test results:", response)
