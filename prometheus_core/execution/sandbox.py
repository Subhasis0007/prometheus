import subprocess
import tempfile
import os

def run_in_sandbox(code: str, timeout: int = 30):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ["python3", temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        os.unlink(temp_file)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {"success": False, "output": "", "error": "Execution timed out"}
