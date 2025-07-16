import subprocess
import threading
import json
from langchain.tools import Tool
from agents.image import ImageSummarizeAgent
import re

class MobileMCP:
    def __init__(self):
        self.process = subprocess.Popen(
            ["npx", "@mobilenext/mobile-mcp@latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.lock = threading.Lock()
        self._id = 1
        
        self.image_summarizer = ImageSummarizeAgent("claude-3.5-sonnet")

    def send_json_rpc(self, method: str, params: dict) -> dict:
        with self.lock:
            request = {
                "jsonrpc": "2.0",
                "id": self._id,
                "method": method,
                "params": params
            }
            print(f"\nSending request: {json.dumps(request)}")

            self._id += 1
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()

            output = ""
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                output += line
                if line.strip().endswith("}"):
                    break
            
            return json.loads(output)

    def close(self):
        self.process.stdin.close()
        self.process.terminate()

    def generate_tools(self):
        tools_list_response = self.send_json_rpc("tools/list", {})
        tools_info = tools_list_response["result"]["tools"]

        print("✅ MCP Tools Loaded:")
        for tool in tools_info:
            print(f"- {tool['name']}")

        generated_tools = []

        for tool in tools_info:
            tool_name = tool["name"]

            def make_tool_func(method_name):
                def tool_func(tool_input=None):
                    if tool_input is None:
                        tool_input = {}

                    processed_input = self.process_tool_input(tool_input)

                    result = self.send_json_rpc("tools/call", {
                        "name": method_name,
                        "arguments": processed_input
                    })
                    
                    try:
                        content = result['result']['content'][0]
                        resulttype = content.get('type')
                        if resulttype == 'image':
                            image = content.get('data')
                            image_summary = self.image_summarizer.summarize(image)
                            content['data'] = image_summary
                            content['type'] = 'text'
                            if 'mimeType' in content:
                                del content['mimeType']
                    except Exception:
                        pass
                        
                    return result
                return tool_func

            tool_description = "\n".join([f"{k}: {v}" for k, v in tool.items()])
            
            generated_tools.append(
                Tool(
                    name=tool_name,
                    func=make_tool_func(tool_name),
                    description=tool_description,
                )
            )

        return generated_tools

    def process_tool_input(self, tool_input):
        matches = re.findall(r"```json(.*?)```", tool_input, re.DOTALL)
        if matches:
            tool_input = matches[0]

        tool_input = tool_input.strip()
        tool_input = json.loads(tool_input)
        return tool_input
        
