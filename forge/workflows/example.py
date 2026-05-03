# Example workflow that PROMETHEUS supervises
def example_full_workflow(user_request: str):
    print(f"[Forge] Starting workflow for: {user_request}")
    # Simulate multi-step workflow
    step1 = "Planning done"
    step2 = "Code generated"
    step3 = "PROMETHEUS supervised and corrected"
    return f"Workflow completed: {step1} -> {step2} -> {step3}"
