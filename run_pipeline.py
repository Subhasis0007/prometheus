import time
from prometheus_planner_agent import boot_agent as boot_global_brain, create_plan, UserGoal
from prometheus_coder_agent import execute, recover, ThoughtStream as CoderStream
from prometheus_reviewer_agent import evaluate, ThoughtStream as ReviewerStream, Traceback
from prometheus_fs_agent import write_to_disk

def run_campaign():
    print("=== PROMETHEUS DAEMON ONLINE ===")
    
    # 1. Boot the Global Silicon (Shared Memory Mode)
    print("\n[SYSTEM] Allocating Shared Unified Memory (Zero-Copy Mode)...")
    global_model, global_tok = boot_global_brain()
    
    # 2. Define the Campaign
    campaign_goal = "Create a Python class that manages a simple To-Do list. It should have methods to add an item, remove an item, and list all items."
    print(f"\n[USER GOAL] {campaign_goal}")
    
    # 3. Planning Phase
    plan = create_plan(UserGoal(campaign_goal), global_model, global_tok)
    print(f"\n[ORCHESTRATOR] Campaign Plan Received ({len(plan)} steps). Initiating Execution Loop...\n")
    
    # 4. Execution Loop (Rolling State Memory)
    working_memory = ""
    
    for step_num, task_desc in enumerate(plan, 1):
        print(f"\n==================================================")
        print(f"⚙️ EXECUTING STEP {step_num}/{len(plan)}: {task_desc}")
        print(f"==================================================")
        
        current_stream = CoderStream(task=task_desc, campaign_context=working_memory)
        max_retries = 3
        attempt = 1
        
        while attempt <= max_retries:
            print(f"\n--- ATTEMPT {attempt} ---")
            
            if attempt == 1:
                step_artifact = execute(current_stream, global_model, global_tok)
            else:
                step_artifact = recover(traceback, global_model, global_tok)
                
            result = evaluate(ReviewerStream(task=task_desc, artifact=step_artifact), global_model, global_tok)
            
            if isinstance(result, Traceback):
                print("\n[ORCHESTRATOR] 🚨 Traceback detected! Routing back to Coder...")
                traceback = result
                attempt += 1
            else:
                print("\n[ORCHESTRATOR] ✅ Step Approved by Reviewer.")
                working_memory = step_artifact.strip()
                break
        
        if attempt > max_retries:
            print(f"\n[ORCHESTRATOR] ❌ Step {step_num} failed after {max_retries} attempts. Halting.")
            return

    print("\n=== CAMPAIGN COMPLETE ===")
    print("[SYSTEM] Committing final state to disk...")
    status = write_to_disk("todo_list.py", working_memory)
    print(status)
    print("=========================")

if __name__ == "__main__":
    run_campaign()
