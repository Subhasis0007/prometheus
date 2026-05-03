import json
from datetime import datetime
import os

AUDIT_LOG = "audit.log"

def log_action(agent: str, action: str, result: str, risk_level: str = "LOW", approved: bool = True):
    """Log all agent actions for compliance and debugging"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "action": action[:500],  # Limit length
        "result": result[:200],
        "risk_level": risk_level,
        "approved": approved
    }
    
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"[Audit] {agent} | {risk_level} | Approved: {approved}")
