import subprocess
import tempfile
import os

def run_code(code: str):
    """
    Execute Python code and return (success, output).
    If the code appears to be a CLI tool (uses argparse/sys.argv), 
    it will be run with a sample argument.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        # Detect if this looks like a CLI tool
        is_cli = any(kw in code for kw in ["argparse", "add_argument", "sys.argv"])

        if is_cli:
            # Run with a sample argument (e.g. number 5)
            result = subprocess.run(
                ["python", temp_file, "5"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )

        output = result.stdout + result.stderr
        success = result.returncode == 0
        return success, output

    except subprocess.TimeoutExpired:
        return False, "Execution timed out after 10 seconds"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
