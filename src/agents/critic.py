from mlx_lm import generate

def critic_agent(model, tokenizer, code, plan):
    prompt = f"""You are the CRITIC agent for PROMETHEUS.

Plan:
{plan}

Generated code:
{code}

Review the code:
- Is it correct?
- Does it follow the plan?
- Any bugs or security issues?

Reply with: "APPROVED" if good, or "NEEDS FIX: [specific issues]" if not.

Review:"""

    review = generate(model, tokenizer, prompt=prompt, max_tokens=300)
    return review.strip()