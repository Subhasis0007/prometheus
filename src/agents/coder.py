from mlx_lm import generate

def coder_agent(model, tokenizer, plan, user_input):
    prompt = f"""You are the CODER agent for PROMETHEUS.

Plan from Planner:
{plan}

User request: {user_input}

Write clean, complete Python code that follows the plan exactly.
Output ONLY valid Python code. No explanations, no markdown.

Code:"""

    code = generate(model, tokenizer, prompt=prompt, max_tokens=900)
    return code.strip()