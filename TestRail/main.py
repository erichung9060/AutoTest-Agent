from Lib.restfulwebservice import  APIClient,APIError
import json


url = 'https://testrail-tools.trendmicro.com'
client = APIClient(url)
client.user = 'eric_hung@trendmicro.com'
client.password = 'ouwcAPBvhm9t99nlGJRo-y.LCwLNbZ4ZFjJtsKokj'

# re = client.get_sections(623,401816)
# print(json.dumps(re, indent=2))
# print(json.dumps(client.get_sections(623,401816), indent=2))

project_id = 623
suite_id = 401816
section_id = 16233670

test_cases = client.get_cases(project_id, suite_id, section_id)
# print(json.dumps(test_cases, indent=2))

for i, case in enumerate(test_cases['data']):
    print(f"=== Test Case {i+1}: {case['title']} ===")
    print(f"Custom Steps:\n{case['custom_steps']}")
    print(f"Custom Expected:\n{case['custom_expected']}")
    print("-" * 50)