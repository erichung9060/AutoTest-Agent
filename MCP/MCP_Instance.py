import subprocess
from agents.image import ImageSummarizeAgent
import re
from typing import Dict, List, Any
import json
from langchain.tools import Tool

class MCPInstance:
    def __init__(self, name: str, command: str, args: List[str]):
        self.name = name
        self.command = command
        self.args = args
        self.process = None
        self._id = 1
        self.image_summarizer = ImageSummarizeAgent()
        
    def start(self):
        try:
            cmd = [self.command] + self.args
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print(f"MCP Server '{self.name}' started with command: {' '.join(cmd)}")
            return True
        except Exception as e:
            print(f"Failed to start MCP Server '{self.name}': {e}")
            return False

    def process_mcp_request(self, method: str, params: dict) -> dict:
        request = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params
        }
        print(f"\n[{self.name}] Sending request: {json.dumps(request)}")

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
        
        result = json.loads(output)
        
        # Process image content with summarizer
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

    def close(self):
        if self.process is None and self.process.poll() is not None:
            self.process.stdin.close()
            self.process.terminate()

    def generate_tools(self) -> List[Tool]:
        try:
            tools_list_response = self.process_mcp_request("tools/list", {})
            tools_info = tools_list_response["result"]["tools"]

            print(f"✅ MCP Tools Loaded from '{self.name}':")
            for tool in tools_info:
                print(f"- {tool['name']}")

            generated_tools = []

            for tool in tools_info:
                tool_name = tool["name"]

                def make_tool_func(method_name, mcp_instance):
                    def tool_func(tool_input=None):
                        processed_input = self.preprocess_tool_input(tool_input)

                        result = mcp_instance.process_mcp_request("tools/call", {
                            "name": method_name,
                            "arguments": processed_input
                        })
                        return result
                    return tool_func

                tool_description = f"[{self.name}] " + "\n".join([f"{k}: {v}" for k, v in tool.items()])
                
                generated_tools.append(
                    Tool(
                        name=tool["name"],
                        func=make_tool_func(tool_name, self),
                        description=tool_description,
                    )
                )

            return generated_tools
        except Exception as e:
            print(f"❌ Failed to generate tools for '{self.name}': {e}")
            return []

    def preprocess_tool_input(self, tool_input):
        matches = re.findall(r"```json(.*?)```", tool_input, re.DOTALL)
        if matches:
            tool_input = matches[0]
        tool_input = tool_input.strip()
        tool_input = json.loads(tool_input)
        return tool_input
