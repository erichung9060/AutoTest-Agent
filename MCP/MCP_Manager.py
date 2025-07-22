import json
import os
from langchain.tools import Tool
from typing import Dict, List, Any
from MCP.MCP_Instance import MCPInstance

class MCPManager:
    def __init__(self, config_file: str = "MCP/mcp_settings.json"):
        self.config_file = config_file
        self.mcp_instances: Dict[str, MCPInstance] = {}
        self.all_tools: List[Tool] = []
        self.initialize_all_mcps()

    def load_config(self) -> Dict[str, Any]:
        config_path = os.path.join(os.path.dirname(__file__), "..", self.config_file)
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    
    def initialize_all_mcps(self):
        config = self.load_config()
        mcp_servers = config.get("mcpServers", {})

        print(f"🚀 Initializing {len(mcp_servers)} MCP servers...")
        
        for server_name, server_config in mcp_servers.items():
            command = server_config.get("command")
            args = server_config.get("args", [])

            mcp_instance = MCPInstance(server_name, command, args)
            
            if mcp_instance.start():
                self.mcp_instances[server_name] = mcp_instance
            else:
                print(f"❌ Failed to start MCP server '{server_name}'")
    
    def get_all_tools(self) -> List[Tool]:
        self.all_tools = []
        
        for instance in self.mcp_instances.values():
            tools = instance.generate_tools()
            self.all_tools.extend(tools)
            
        print(f"Total {len(self.all_tools)} tools loaded from {len(self.mcp_instances)} MCP servers")
        return self.all_tools
    
    def close_all(self):
        for instance in self.mcp_instances.values():
            instance.close()
        self.mcp_instances.clear()
        self.all_tools.clear()