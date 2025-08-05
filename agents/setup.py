import subprocess
from agents.Agent import ReActAgent
import os

class SetupAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized SetupAgent with model: {self.model}")
        
    def run(self) -> dict:
        prompt = f"""
        You are a setup assistant using mobile MCP to control a phone. Set up all necessary permissions for the app.

        Tasks:
        1. Identify permission requests or setup prompts
        2. Grant all permissions (camera, location, notifications, etc.)
        3. Navigate through setup flows/tutorials 
        4. Reach the main interface

        Guidelines:
        - PRIORITIZE XML element location (dump_screen_xml) over screenshots
        - Use screenshots only when XML fails or for final verification
        - Grant all permissions, don't skip steps
        - Output clean JSON only for actions

        COMPLETION: Must take final screenshot/UI dump to verify main interface is reached before declaring setup complete.
        OUTPUT: Provide detailed steps to speed up the next LLM approach."
        """
        try:
            setup_result = self.agent.invoke({"input": prompt})
            result = setup_result['output']
            
            self.take_screenshot("setup_checkpoint.png")
            
            return result
            
        except Exception as e:
            print(f"Error during setup: {e}")
            return str(e)
    
    def take_screenshot(self, screenshot_name: str) -> str:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.join("screenshots", screenshot_name)

        result = subprocess.run([
            "adb", "exec-out", "screencap", "-p"
        ], capture_output=True, check=True)
        
        with open(screenshot_path, "wb") as f:
            f.write(result.stdout)
        
        return screenshot_name