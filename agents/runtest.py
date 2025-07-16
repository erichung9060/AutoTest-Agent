from agents.Agent import ReActAgent

class RunTestAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized RunTestAgent with model: {self.model}")
        
    def run(self, title: str, description: str) -> dict:
        prompt = f"""
You are a QA tester using mobile MCP to control a phone. 
The app to be tested is already opened. 

Test Title: {title}
Test Description: {description}

Please execute this test step by step using available MCP tools.
Finally, output a execution result.
If the expected result is not obtained, please retry up to 3 times before finishing.
        """
        try:
            run_result = self.agent.invoke({"input": prompt})
            result = run_result['output']
            return result
            
        except Exception as e:
            print(f"Error executing test: {e}")
            return str(e)
