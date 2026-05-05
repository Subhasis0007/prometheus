from mlx_lm import generate
from pydantic import BaseModel
from typing import List

class UserGoal(BaseModel):
    goal: str

def boot_agent():
    from mlx_lm import load
    model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
    return model, tokenizer

def create_plan(goal: UserGoal, model, tokenizer) -> List[str]:
    prompt = f"""<|im_start|>system
You are an expert AI software engineering planner.

Your ONLY job is to break down the user's goal into 4–8 high-level, actionable coding steps that stay 100% faithful to what the user actually asked for.

STRICT RULES:
- Never add steps for things the user did NOT ask for (e.g. do not create project structure, virtual environments, docs folders, etc. unless explicitly requested).
- Focus only on the core functionality described in the goal.
- Include key requirements mentioned by the user (CLI arguments, input validation, error handling, docstrings, type hints, etc.).
- Keep steps high-level but practical (what a senior developer would implement in one focused session).
- Output ONLY a clean numbered list. No explanations, no extra text.
<|im_end|>
<|im_start|>user
User Goal: {goal.goal}

Create 4–8 high-level coding steps that directly solve this goal. Stay strictly faithful to the request.
<|im_end|>
<|im_start|>assistant
"""
    response = generate(model, tokenizer, prompt=prompt, max_tokens=512, verbose=False)
    
    steps = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            clean = line.lstrip("0123456789.- ").strip()
            if clean:
                steps.append(clean)
    return steps
