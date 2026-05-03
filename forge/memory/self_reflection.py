from datetime import datetime

def self_reflect(last_action: str, result: str):
    reflection = f"[PROMETHEUS Reflection at {datetime.now().isoformat()}] Last action: {last_action}. Result: {result}. Improvement: Remember user location better."
    with open("forge/memory/reflections.log", "a") as f:
        f.write(reflection + "\n")
    print(reflection)
    return reflection
