from agents.Agent import ReActAgent

class RunTestAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized RunTestAgent with model: {self.model}")
        
    def run(self, title: str, description: str) -> dict:
        prompt = f"""
        You are a QA tester using the mobile MCP to control a phone.
        First, open the ScamCheck app.
        Then, execute the following test case:

        Test Title: {title}
        Test Description: {description}

        Please perform this test step by step using the available MCP tools.
        At the end, provide the execution result.
        If the expected result is not achieved, retry up to 3 times before finishing.
        Prefer using XML to locate elements and perform actions on them.
        Only use coordinate-based clicks if absolutely necessary.
        """
        try:
            run_result = self.agent.invoke({"input": prompt})
            result = run_result['output']
            return result
            
        except Exception as e:
            print(f"Error executing test: {e}")
            return str(e)
