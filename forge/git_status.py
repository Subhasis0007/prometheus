import subprocess
def get_git_status():
    try:
        branch = subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()
        return f"Git branch: {branch}"
    except:
        return "Git not initialized"
