import os

file_path = 'forge/forge.py'
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
    exit(1)

with open(file_path, 'r') as f:
    content = f.read()

# 1. Prepare the MLX injection block
mlx_code = """
# --- PROMETHEUS MLX ENGINE ---
try:
    from mlx_lm import load, generate
    import logging
    logger = logging.getLogger("PROMETHEUS-MLX")
    logger.info("Initializing Qwen2.5-7B MLX model into memory... This may take a moment.")
    
    # Load globally to persist across API calls
    model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
    logger.info("✅ MLX Engine Online.")

    def generate_text(prompt: str, max_tokens=512) -> str:
        # Wrap the MLX generate call
        response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens)
        return response
except ImportError:
    print("⚠️ mlx_lm not found. Run: pip install mlx-lm")
    def generate_text(prompt: str, max_tokens=512) -> str:
        return "Error: mlx-lm not installed."
# -----------------------------
"""

# 2. Inject MLX imports and model loading near the top, after standard imports
if "from mlx_lm import load" not in content:
    # Find a good place to inject: right after FastAPI imports
    if "from fastapi" in content:
        parts = content.split("from fastapi", 1)
        # Split on the next newline to safely insert after the import
        sub_parts = parts[1].split("\n", 1)
        new_content = parts[0] + "from fastapi" + sub_parts[0] + "\n" + mlx_code + sub_parts[1]
        content = new_content
        print("✅ MLX Engine block injected.")
    else:
        # Fallback: put it at the very top
        content = mlx_code + "\n" + content
        print("✅ MLX Engine block injected at the top of the file.")
else:
    print("⚠️ MLX Engine block already exists.")

# 3. Ensure the /run/team endpoint points to the real `generate_text`
if "def local_mlx_call(prompt):" in content and "return generate_text(prompt)" in content:
    print("✅ Supervisor is already wired to generate_text.")
else:
    print("⚠️ Make sure PrometheusSupervisor(mlx_generate_fn=generate_text) is set in your /run/team route!")

with open(file_path, 'w') as f:
    f.write(content)

print("🚀 Patch complete. Start your Forge server to load the weights into Apple Silicon.")
