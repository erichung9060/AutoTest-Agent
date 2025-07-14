from mcp_client import MCPClient
from agent_setup import create_agent_executor
from TestRail.utility import get_test_cases_description
import re

project_id = 623
suite_id = 401816
section_id = 16233670

test_cases = get_test_cases_description(project_id, suite_id, section_id)


for title, description in test_cases.items():
    print(f"Test Case: {title}\nDescription:\n{description}\n")

    user_input = f"""
You are a QA tester using mobile MCP to control a phone. The app to be tested is already opened. The test steps are as follows:
{description}
Try to use element id as much as possible, instead of manual coordinates.
Finally, output a report. The test can only be considered Pass if it STRICTLY meets the Expected Result.
If the expected result is not obtained, please retry up to 5 times before finishing.
"""
    
    mcp_client = MCPClient()
    generated_tools = mcp_client.generate_tools()
    agent = create_agent_executor(generated_tools)
    # agent = create_agent_executor(generated_tools, model="gpt-4o")

    result = agent.invoke({"input": user_input})
    print(f"=== Result ===\n{result['output']}\n")

    with open(f"report/{title}.txt", "w", encoding="utf-8") as f:
        f.write(f"Test Case: {title}\nDescription:\n{description}\n\n=== Result ===\n{result['output']}\n")

    mcp_client.close()

    break
        
    