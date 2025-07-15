from mcp_client import MCPClient
from agents.agent_setup import create_agent_executor
from TestRail.utility import get_test_cases_description
import re

project_id = 623
suite_id = 401816
section_id = 16233670

mcp_client = MCPClient()
generated_tools = mcp_client.generate_tools()

test_cases = get_test_cases_description(project_id, suite_id, section_id)
for title, description in test_cases.items():
    print(f"Test Case: {title}\nDescription:\n{description}\n")
    
    agent = create_agent_executor(generated_tools)
    # agent = create_agent_executor(generated_tools, model="gpt-4o")

    result = agent.invoke({"input": description})
    print(f"=== Result ===\n{result['output']}\n")

    with open(f"report/{title}.md", "w", encoding="utf-8") as f:
        f.write(f"""
Test Case: {title}\ 
Description:\ 
{description}

========= Result =========

{result['output']}\n""")

    mcp_client.close()

    break
        
    