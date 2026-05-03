PERMISSION_LEVELS = {
    "GUEST": ["read", "view", "list"],
    "USER": ["read", "view", "list", "write", "create", "update"],
    "ADMIN": ["read", "view", "list", "write", "create", "update", "delete", "remove", "execute"],
    "SUPERADMIN": ["*"]  # All permissions
}

def get_user_permission_level() -> str:
    """Get current user permission level (simulated)"""
    # In production, this would check actual user credentials
    return "ADMIN"

def has_permission(task: str, user_level: str = "ADMIN") -> bool:
    """Check if user has permission for this task"""
    if user_level == "SUPERADMIN":
        return True
    
    task_lower = task.lower()
    
    if user_level == "ADMIN":
        return True  # Admin can do everything with approval
    
    if user_level == "USER":
        restricted = ["delete", "remove", "format", "shutdown", "kill"]
        return not any(kw in task_lower for kw in restricted)
    
    # GUEST - read only
    return any(kw in task_lower for kw in ["read", "view", "list", "show"])
