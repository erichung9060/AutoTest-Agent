from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess
import os
import re
from agents.Agent import ReActAgent
import urllib.parse

class JudgeAgent(ReActAgent):
    def __init__(self, model="claude-4-sonnet"):
        super().__init__(model)
        print(f"Initialized JudgeAgent with model: {self.model}")

        
    def take_screenshot(self, screenshot_name: str) -> str:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.join("screenshots", screenshot_name)

        result = subprocess.run([
            "adb", "exec-out", "screencap", "-p"
        ], capture_output=True, check=True)
        
        with open(screenshot_path, "wb") as f:
            f.write(result.stdout)
        
        return screenshot_name
    


    def judge_test_result(self, title, description, run_result):
        timestamp = datetime.now(ZoneInfo('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")
        screenshot_name = screenshot_name = f"{title}_{timestamp}.png"
        screenshot_path = self.take_screenshot(screenshot_name)

        judge_prompt = f"""
    You are an expert software test judge. Your task is to strictly evaluate whether the test case has passed or failed based on the provided information.

    Test Case Title: {title}
    Test Description: {description}
    Execution Result: {run_result}

    Instructions:
    1. Carefully review the test description and execution result.
    2. Analyze the attached screenshot (take it first) to verify the actual outcome.
    3. The test is considered PASSED only if ALL requirements in the description are FULLY and STRICTLY satisfied. Any deviation or missing detail means the test should be marked as FAIL.
    4. Provide clear, detailed reasoning for your judgement, referencing specific points from the description and evidence from the execution result or screenshot.
    5. If further verification is needed, you may use available MCP tools.

    Respond in the following format:

    ---
    Final Answer: 
    Judgement: [PASS/FAIL]

    Reasoning:
    - [Your detailed reasoning here]
    ---
    """
        
        result = self.agent.invoke({"input": judge_prompt})
        judge_result = result['output']

        match = re.search(r'Judgement:\s*\[?(PASS|FAIL)\]?', judge_result, re.IGNORECASE)
        judgement_value = match.group(1).upper() if match else "UNKNOWN"
        prefix = "⭕️" if judgement_value == "PASS" else "❌"
        report_file_name = f"{prefix} {title}_{timestamp}.md"

        os.makedirs("report", exist_ok=True)
        with open(f"report/{report_file_name}", "w", encoding="utf-8") as f:
            f.write(f"""# Test Report

## Test Case Information
**Title:** {title}  
**Description:**  
{description}

## Execution Result
{run_result}

### Judgement Details
{judge_result}

## Judgement Result
**Screenshot:**  
![Screenshot](../screenshots/{urllib.parse.quote(screenshot_path)})

---
*Report generated at: {timestamp}*
""")
            
        return judge_result
    