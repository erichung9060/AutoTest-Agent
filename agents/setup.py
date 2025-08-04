from agents.Agent import ReActAgent

class SetupAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized SetupAgent with model: {self.model}")
        
    def run(self) -> dict:
        prompt = f"""
        You are a setup assistant using the mobile MCP to control a phone.
        You need to set up all necessary permissions for the opening app before running any tests.

        Your task is to:
        1. Check the current screen and identify any permission requests or setup prompts
        2. Follow all on-screen instructions to grant necessary permissions
        3. Navigate through any initial setup flows or tutorials
        4. Ensure the app is ready for testing by reaching the main interface
        5. Handle any system dialogs, permission requests, or notifications that appear

        Important guidelines:
        - Always read the screen content carefully before taking action
        - Grant all permissions when prompted (camera, location, notifications, etc.)
        - Skip or dismiss any optional tutorials or promotional content
        - If you encounter errors, try alternative approaches
        - Take screenshots to document the setup process
        - Use XML-based element location when possible, only use coordinates as fallback

        **If a required toggle (e.g., "Use ScamCheck") is visible but the switch itself is not detected in the element list, try to tap the likely switch area based on nearby elements such as the label text. You may estimate the button's position using the bounding box of the label and standard Android layouts.**

        **For example, if "Use ScamCheck" appears as a `TextView`, and there is no `Switch` nearby, estimate the switch location to be on the same horizontal line and right-aligned (e.g., +700px on x-axis from the left of the text).**

        The setup is complete when:
        - All permissions have been granted
        - The app is showing its main interface/home screen
        - No more setup dialogs or permission requests are pending

        Please proceed step by step and provide a summary of what was set up.
        """
        try:
            setup_result = self.agent.invoke({"input": prompt})
            result = setup_result['output']
            return result
            
        except Exception as e:
            print(f"Error during setup: {e}")
            return str(e)