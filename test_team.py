from forge.collaboration.team import PrometheusSupervisor

# Mock MLX generation function (replace with your actual MLX import when ready)
def dummy_mlx_generator(prompt: str) -> str:
    print(f"\n--- Model Input ---\n{prompt[:100]}...\n-------------------")
    if "researcher" in prompt.lower():
        return "1. Create structure. 2. Define endpoints."
    elif "coder" in prompt.lower():
        return "def main():\n    print('Hello World')\n"
    return "APPROVED. Code looks solid."

if __name__ == "__main__":
    supervisor = PrometheusSupervisor(mlx_generate_fn=dummy_mlx_generator)
    print("\n🚀 STARTING PROMETHEUS TEAM LOOP 🚀\n")
    results = supervisor.run_team_task("Build a basic Python CLI tool.")
    
    print("\n✅ FINAL TRANSCRIPT ✅")
    for r in results:
        print(f"[{r['agent']}]: {r['content']}")
