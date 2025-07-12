from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
import os
def create_agent_executor(tools, model = "claude-4-sonnet"):
    load_dotenv()
    print("Using model:", model)

    llm = ChatOpenAI(
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=model,
        temperature=0.0
    )

    prompt = hub.pull("hwchase17/react")

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