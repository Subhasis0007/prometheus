from mlx_lm import generate

def planner_agent(model, tokenizer, user_input, memory):
    relevant = memory.search(user_input, n_results=5)
    memory_context = "\n".join(relevant) if relevant else "No memory."

    prompt = f"""You are the PLANNER agent for PROMETHEUS.

Memories:
{memory_context}

User request: {user_input}

Create a clear, step-by-step plan to solve this. Be concise.

Plan:"""

    plan = generate(model, tokenizer, prompt=prompt, max_tokens=400)
    return plan.strip()