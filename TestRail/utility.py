from TestRail.restfulwebservice import  APIClient,APIError
import json


url = 'https://testrail-tools.trendmicro.com'
client = APIClient(url)
client.user = 'eric_hung@trendmicro.com'
client.password = 'ouwcAPBvhm9t99nlGJRo-y.LCwLNbZ4ZFjJtsKokj'

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
