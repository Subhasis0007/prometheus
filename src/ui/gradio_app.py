from mlx_lm import generate
import gradio as gr
import os
import subprocess

TOOLS_DIR = "src/tools/auto_generated"

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

def launch_ui(model, tokenizer, memory):
    def chat(message, history):
        memory.add(message, {"type": "user"})
        context = memory.search(message, n_results=6)
        memory_context = "\n".join(context)

        if message.lower() == "list tools":
            tools = list_tools()
            response = f"Available tools: {', '.join(tools) if tools else 'No tools yet.'}"
        elif message.lower().startswith("run ") or message.lower().startswith("execute "):
            tool_name = message.split()[-1]
            response = execute_tool(tool_name)
        else:
            prompt = f"""You are PROMETHEUS Week 3.

CRITICAL RULES:
- Be SHORT. Max 2-3 sentences.
- NEVER repeat yourself.
- ALWAYS remember: User's name is Subhasis from Bengaluru. Goal is to become world famous by building PROMETHEUS.

Context:
{memory_context}

User: {message}

Your response:"""
            response = generate(model, tokenizer, prompt=prompt, max_tokens=300)

        memory.add(response, {"type": "agent"})
        
        if history is None:
            history = []
        history.append((message, response))
        return history

    with gr.Blocks(title="PROMETHEUS", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🚀 PROMETHEUS Phase 4
        **Self-Evolving Multi-Agent AI System**
        
        Built by **Subhasis from Bengaluru**  
        Goal: Become World Famous AI Builder
        """)
        
        chatbot = gr.Chatbot(height=600, label="Chat with PROMETHEUS")
        msg = gr.Textbox(placeholder="Try: Create a new tool... or list tools", label="Your Message")
        clear = gr.Button("Clear Chat")

        msg.submit(chat, [msg, chatbot], chatbot)
        clear.click(lambda: [], None, chatbot)

    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)