class MCPClientManager:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name: str, tool):
        self.tools[name] = tool
        print(f"[MCP] Registered tool: {name}")
    
    def call_tool(self, name: str, args: dict):
        if name in self.tools:
            return self.tools[name](**args)
        return {"error": "Tool not found"}
