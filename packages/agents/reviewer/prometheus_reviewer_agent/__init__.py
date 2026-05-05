from mlx_lm import generate

class ThoughtStream:
    def __init__(self, task: str, artifact: str = None):
        self.task = task
        self.artifact = artifact

class Traceback:
    def __init__(self, error_class: str, error_message: str, origin_agent: str, origin_task: str):
        self.error_class = error_class
        self.error_message = error_message
        self.origin_agent = origin_agent
        self.origin_task = origin_task

def evaluate(stream: ThoughtStream, model, tokenizer):
    system_prompt = (
        "You are a senior code reviewer. "
        "Check two things only: "
        "1. Is the code syntactically correct and does it solve the task? "
        "2. Is the code reasonably clean and professional (has docstrings where appropriate, decent variable names)? "
        "Reply exactly with: APPROVED if both are good. "
        "If there are real problems, reply with a short explanation. "
        "Do NOT be overly strict on style."
    )

    user_prompt = f"Task: {stream.task}\n\nCode:\n```python\n{stream.artifact}\n```"

    full_prompt = f"""<|im_start|>system
{system_prompt}
<|im_end|>
<|im_start|>user
{user_prompt}
<|im_end|>
<|im_start|>assistant
"""

    res = generate(model, tokenizer, prompt=full_prompt, max_tokens=256, verbose=False).strip()

    if "APPROVED" in res.upper():
        return stream.artifact
    else:
        return Traceback("ReviewerRejection", res, "Reviewer", stream.task)
