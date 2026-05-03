import os
import logging
try:
    from mlx_lm import load, generate
except ImportError:
    print("Error: mlx_lm not installed.")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PROMETHEUS-Archivist")

def get_system_context():
    """Gathers context about the project to feed to the LLM."""
    context = "Project Name: PROMETHEUS (Forge)\n"
    context += "Architecture: 100% Local Apple Silicon (MLX), Multi-Agent Supervisor, Execution Sandbox, Long-Term Skill Crystallization.\n\n"
    
    # Check learned skills
    skills_dir = "forge/skills"
    if os.path.exists(skills_dir):
        skills = [f for f in os.listdir(skills_dir) if f.endswith('.md')]
        context += f"Number of Autonomous Skills Mastered: {len(skills)}\n"
        context += "Recent Skills:\n"
        for s in skills[:5]:
            context += f"- {s.replace('.md', '').replace('_', ' ')}\n"
            
    return context

def build_readme():
    logger.info("Initializing MLX Model for README generation...")
    model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
    
    context = get_system_context()
    
    prompt = f"""<|im_start|>system
You are a Staff-Level Developer Advocate at a top-tier tech company. Your job is to write a highly professional, engaging, and "viral-ready" GitHub README.md for an open-source project.
Use Markdown, badges, emojis, and clear architectural explanations. Make it sound extremely impressive but technically accurate.
<|im_end|>
<|im_start|>user
Write a comprehensive README.md for my project based on this context:
{context}

Include the following sections:
1. An eye-catching header and description.
2. Key Features (Highlighting the local MLX aspect, the Sandbox, and Skill Memory).
3. System Architecture.
4. Getting Started / Installation.
5. Example Agent Loop Output.

Only output the raw Markdown for the README. Do not wrap it in a code block.<|im_end|>
<|im_start|>assistant
"""

    logger.info("Archivist is analyzing the codebase and drafting the README...")
    response = generate(model, tokenizer, prompt=prompt, max_tokens=1500)
    
    # Clean up the output if the model wrapped it in markdown tags
    if response.startswith("```markdown"):
        response = response.split("```markdown")[1]
    if response.endswith("```"):
        response = response.rsplit("```", 1)[0]
        
    with open("README.md", "w") as f:
        f.write(response.strip())
        
    logger.info("✅ Viral README.md successfully generated in the root directory!")

if __name__ == "__main__":
    print("🚀 Waking up The Archivist...")
    build_readme()
