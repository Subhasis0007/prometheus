from mlx_lm import load, generate
from src.memory.advanced_memory import AdvancedMemory
from src.ui.gradio_app import launch_ui
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

print("🚀 PROMETHEUS Week 2 - Tuned Self-Reflection (Optimized)")
model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
print("✅ 7B Model loaded!")

memory = AdvancedMemory()
TOOLS_DIR = "src/tools/auto_generated"
os.makedirs(TOOLS_DIR, exist_ok=True)

def list_tools():
    return [f for f in os.listdir(TOOLS_DIR) if f.endswith(".py")]

def execute_tool(tool_name):
    filepath = os.path.join(TOOLS_DIR, tool_name)
    if not os.path.exists(filepath):
        return f"❌ Tool {tool_name} not found."
    
    try:
        result = subprocess.run(["python", filepath], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ {tool_name} executed!\n{result.stdout}"
        else:
            return f"❌ Error in {tool_name}:\n{result.stderr}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def self_reflect(model, tokenizer, code, plan):
    prompt = f"""You are the SELF-REFLECTION agent.

Plan: {plan}

Generated code:
{code}

Reply ONLY with: "APPROVED" or "NEEDS IMPROVEMENT: [issues]"

Critique:"""
    return generate(model, tokenizer, prompt=prompt, max_tokens=150).strip()

print("\n=== WEEK 2 OPTIMIZED READY ===\n")
print("Commands: 'list tools', 'run tool_8.py', 'web', 'exit'\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    if user_input.lower() == "web":
        launch_ui(model, tokenizer, memory)
        continue

    memory.add(user_input, {"type": "user"})

    context = memory.search(user_input, n_results=6)
    memory_context = "\n".join(context)

    if user_input.lower() == "list tools":
        tools = list_tools()
        response = f"Available tools: {', '.join(tools) if tools else 'No tools yet.'}"
    elif user_input.lower().startswith("run ") or user_input.lower().startswith("execute "):
        tool_name = user_input.split()[-1]
        response = execute_tool(tool_name)
    else:
        # SMART SELF-REFLECTION (only for code/tool tasks)
        if any(word in user_input.lower() for word in ["create", "tool", "code", "script", "function", "program"]):
            logger.info("Code/tool task detected - using self-reflection")
            
            plan_prompt = f"""You are the PLANNER. Plan for: {user_input}

Plan:"""
            plan = generate(model, tokenizer, prompt=plan_prompt, max_tokens=200).strip()
            
            code_prompt = f"""You are the CODER. Code for: {plan}

Output ONLY Python code:"""
            code = generate(model, tokenizer, prompt=code_prompt, max_tokens=600).strip()
            
            critique = self_reflect(model, tokenizer, code, plan)
            logger.info(f"Self-reflection: {critique}")
            
            if "APPROVED" in critique.upper():
                filename = f"tool_{len(list_tools()) + 1}.py"
                filepath = os.path.join(TOOLS_DIR, filename)
                with open(filepath, "w") as f:
                    f.write(code)
                response = f"✅ Tool {filename} created and approved!\n\n{code[:200]}..."
            else:
                response = f"🔄 Issues: {critique}\nRegenerating..."
        else:
            # Simple Q&A without self-reflection
            prompt = f"""You are PROMETHEUS Week 2.

CRITICAL RULES:
- Be SHORT and DIRECT. Max 2-3 sentences.
- NEVER repeat yourself.
- ALWAYS remember: User's name is Subhasis from Bengaluru. Goal is to become world famous by building PROMETHEUS.

Context:
{memory_context}

User: {user_input}

Your response:"""
            response = generate(model, tokenizer, prompt=prompt, max_tokens=300)

    memory.add(response, {"type": "agent"})
    print(f"\nPROMETHEUS: {response}\n")