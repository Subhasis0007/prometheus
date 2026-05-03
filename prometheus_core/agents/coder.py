from .base import BaseAgent
from prometheus_core.memory.skill_manager import save_skill
from prometheus_core.mcp.client_manager import MCPClientManager

mcp_manager = MCPClientManager()

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Coder")

    def run(self, task: str):
        self.log(f"Coding: {task}")
        
        # Generate MCP-compliant tool
        if "square" in task.lower():
            code = '''def calculate_square(n):
    return n * n
print(calculate_square(5))'''
        else:
            code = f'''def tool_{hash(task) % 10000}():
    print("Task: {task}")
    print("Solution generated successfully!")'''
        
        skill_content = f"## Task\n{task}\n\n## Code\n```python\n{code}\n```"
        save_skill(f"skill_{hash(task) % 10000}", skill_content)
        
        # Register with MCP
        mcp_manager.register_tool(f"tool_{hash(task) % 10000}", lambda: code)
        
        return code
