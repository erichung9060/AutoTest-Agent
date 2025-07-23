from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
import os

class Agent:
    def __init__(self, model="claude-4-sonnet"):
        self.model = model
        self.llm = self._create_llm(model)

    def _create_llm(self, model):
        return ChatOpenAI(
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name=model,
            temperature=0.0
        )
    


class ReActAgent(Agent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        self.mcp_manager = None
        self.agent = self.create_react_agent()
    
    def __del__(self):
        if self.mcp_manager:
            self.mcp_manager.close_all()

    def create_react_agent(self):
        custom_template = '''
        Do the following task as best you can. You have access to the following tools:
        {tools}
        
        Use ReAct methodology - think through each step, take actions, observe results.

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

        Question: {input}
        Thought:{agent_scratchpad}

        If you know the final answer, remember to output it in this format:
        Final Answer: <your final answer here>
        '''
        prompt = PromptTemplate(
            template=custom_template,
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
        )
        
        from MCP.MCP_Manager import MCPManager
        self.mcp_manager = MCPManager()
        self.tools = self.mcp_manager.get_all_tools()
        
        react_agent = create_react_agent(self.llm, self.tools, prompt)
        
        agent = AgentExecutor(
            agent=react_agent, 
            tools=self.tools,
            max_iterations=100,
            max_execution_time=900,
            verbose=True,
        )
        return agent
