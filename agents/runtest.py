from agents.Agent import ReActAgent

class RunTestAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized RunTestAgent with model: {self.model}")
        
    def run(self, title: str, description: str) -> dict:
        prompt = f"""
        You are a QA tester using the mobile MCP to control a phone.
        The app, ScamCheck, is opened already.
        You need to execute the following test case:

        Test Title: {title}
        Test Description: {description}

        Please perform this test step by step using the available MCP tools.
        At the end, provide the execution result.
        Prefer using XML to locate elements and perform actions on them.
        If you cannot find the required element in the XML dump, take a screenshot of the current screen to help with further investigation.
        """
        try:
            run_result = self.agent.invoke({"input": prompt})
            result = run_result['output']
            return result
            
        except Exception as e:
            print(f"Error executing test: {e}")
            return str(e)
