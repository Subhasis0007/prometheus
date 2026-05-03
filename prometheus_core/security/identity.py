import uuid
from datetime import datetime

def generate_agent_identity():
    agent_id = str(uuid.uuid4())
    return {
        "agent_id": agent_id,
        "created_at": datetime.now().isoformat(),
        "type": "PROMETHEUS_Agent"
    }

def verify_identity(identity: dict) -> bool:
    return "agent_id" in identity and "created_at" in identity
