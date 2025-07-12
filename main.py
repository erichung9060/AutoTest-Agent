from mcp_client import MCPClient
from agent_setup import create_agent_executor


mcp_client = MCPClient()
generated_tools = mcp_client.generate_tools()
agent = create_agent_executor(generated_tools)
# agent = create_agent_executor(generated_tools, model="gpt-4o")

user_input = """
You are a QA tester using mobile MCP to control a phone. The app to be tested is already opened. The test steps are as follows:
Step: 1. Tap Risk Check 2. Input https://www.google.com 3. Tap Check now, and wait 10 seconds.
Expected Result: 1. Display result: Safe with blue color 2. Action: Report.
Try to use element id as much as possible, instead of manual coordinates.
Finally, output a report. The test can only be considered Pass if it STRICTLY meets the Expected Result.
If the expected result is not obtained, please retry up to 5 times before finishing.
"""


try:
    result = agent.invoke({"input": user_input})

    print("\n=== MCP 執行結果 ===")
    print(result["output"])

    mcp_client.close()
except Exception as e:
    print(f"Error during agent execution: {e}")
    mcp_client.close()
