import re
from mlx_lm import generate

class ThoughtStream:
    def __init__(self, task: str, campaign_context: str = ""):
        self.task = task
        self.campaign_context = campaign_context

def execute(stream: ThoughtStream, model, tokenizer):
    error_section = ""
    if "[PREVIOUS ATTEMPT FAILED WITH THIS ERROR]" in stream.campaign_context:
        error_section = """
ERROR FEEDBACK: Previous attempt failed. Analyze the error and fix the root cause.
"""

    prompt = f"""<|im_start|>system
You are an expert senior Python developer building code incrementally.

Rules:
- Extend or modify the existing code from context.
- When error feedback is given, fix the root cause.
- Write clean Python with docstrings and type hints.
- Output ONLY valid Python code. No extra text.
<|im_end|>
<|im_start|>user
{error_section}
Existing code so far:
{stream.campaign_context if stream.campaign_context.strip() else "(No previous code)"}

Task: {stream.task}

Extend or fix the code to complete the task.
Output only the full updated code.
<|im_end|>
<|im_start|>assistant
"""
    res = generate(model, tokenizer, prompt=prompt, max_tokens=1536, verbose=False)
    res = re.sub(r'```python\s*', '', res)
    res = re.sub(r'```\s*', '', res)
    return res.strip()
