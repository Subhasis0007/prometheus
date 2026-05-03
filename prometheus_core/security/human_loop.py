import getpass

def requires_approval(task: str) -> bool:
    """Check if a task requires human approval"""
    high_risk_keywords = ["delete", "remove", "format", "shutdown", "kill", "rm -rf", "format disk"]
    return any(keyword in task.lower() for keyword in high_risk_keywords)

def request_approval(task: str) -> bool:
    """Request human approval for high-risk tasks"""
    print(f"\n{'='*60}")
    print(f"⚠️  HIGH RISK TASK DETECTED")
    print(f"{'='*60}")
    print(f"Task: {task}")
    print(f"{'='*60}")
    
    response = input("\nDo you approve this action? (yes/no): ").lower().strip()
    
    if response in ["yes", "y"]:
        # Ask for confirmation with password (simulated)
        confirm = input("Type 'CONFIRM' to proceed: ")
        if confirm == "CONFIRM":
            print("✅ Task approved and executed")
            return True
    print("❌ Task cancelled by user")
    return False
