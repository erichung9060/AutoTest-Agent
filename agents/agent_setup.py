from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
def create_agent_executor(tools, model = "claude-4-sonnet"):
    load_dotenv()
    
    print("\nUsing model:", model)

    llm = ChatOpenAI(
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=model,
        temperature=0.0
    )

    # prompt = hub.pull("hwchase17/react")
    custom_template = '''Do the following task as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: You are a QA tester using mobile MCP to control a phone. 
The app to be tested is already opened. 
The test steps are as follows:
{input}
Finally, output a report. The test can only be considered Pass if it STRICTLY meets the Expected Result.
Thought:{agent_scratchpad}

If the expected result is not obtained, please retry up to 3 times before finishing.
If you know the final answer, remember to output it in this format:
Final Answer: <your final answer here>
'''
    
    prompt = PromptTemplate(
        template=custom_template,
        input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
    )
    
    react_agent = create_react_agent(llm, tools, prompt)

    agent = AgentExecutor(
        agent=react_agent, 
        tools=tools,
        max_iterations=100,
        max_execution_time=900,
        verbose=True,
        # handle_parsing_errors=True,  # retry
    )
    return agent