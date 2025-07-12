import subprocess
import threading
import json
from jsonschema import ValidationError, validate
from langchain.tools import Tool
import tiktoken
import base64, io
from PIL import Image
from io import BytesIO
import re

class MCPClient:
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
            
            result = json.loads(output)
            try:
                resulttype = result['result']['content'][0]['type']
                if resulttype == 'image':
                    image = result['result']['content'][0]['data']
                    result['result']['content'][0]['data'] = self.resize_image(image, 0.5, 10)
            except Exception as e:
                print(f"Error processing image data: {e}")

            return result

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

                    return self.send_json_rpc("tools/call", {
                        "name": method_name,
                        "arguments": processed_input
                    })
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
        
    def resize_image(self, image, resize_factor=0.5, quality=20):
        print("Processing image compressed...")
        image_data = base64.b64decode(image)
        image = Image.open(BytesIO(image_data))
        
        # resize
        new_size = (int(image.width * resize_factor), int(image.height * resize_factor))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        compressed_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        with open("screenshot.jpg", "wb") as f:
            f.write(buffer.getvalue())

        enc = tiktoken.encoding_for_model("gpt-4")
        tokens = enc.encode(compressed_image)
        token_count = len(tokens)
        print(f"Compressed Token Count: {token_count}")

        return compressed_image