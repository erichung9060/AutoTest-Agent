from TestRail.restfulwebservice import  APIClient,APIError
import json
import os

client = APIClient(os.environ.get('TESTRAIL_URL'))
client.user = os.environ.get('TESTRAIL_EMAIL')
client.password = os.environ.get('TESTRAIL_API_KEY')

# print(json.dumps(client.get_sections(623,401816), indent=2))
# print(json.dumps(client.get_cases(623, 401816, 16233670), indent=2))

def get_test_cases_description(project_id, suite_id, section_id):
    test_cases = client.get_cases(project_id, suite_id, section_id)
    result = {}
    for case in test_cases['data']:
        title = case.get('title', 'Untitled')
        steps = case.get('custom_steps', '').replace('\n', ', ')
        expected = case.get('custom_expected', '').replace('\n', ', ')

        description = f"Steps: {steps}, \nExpected: {expected}"
        result[title] = description
    return result
