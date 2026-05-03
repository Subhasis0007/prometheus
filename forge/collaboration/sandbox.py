import subprocess
import os
import logging
from typing import Tuple

logger = logging.getLogger("PROMETHEUS-Sandbox")

class ExecutionSandbox:
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = workspace_dir
        # Ensure the sandbox directory exists
        os.makedirs(self.workspace_dir, exist_ok=True)

    def execute_python_code(self, code: str, filename: str = "generated_script.py", timeout: int = 10) -> Tuple[bool, str]:
        """
        Saves the code to a file and executes it safely.
        Returns (success_boolean, console_output_or_error)
        """
        filepath = os.path.join(self.workspace_dir, filename)
        
        # Clean the code safely without breaking strings
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        # Write the code to the sandbox
        with open(filepath, 'w') as f:
            f.write(code)
            
        logger.info(f"Sandbox executing {filename}...")

        try:
            # Run the script in a subprocess
            result = subprocess.run(
                ["python3", filepath],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                logger.info("Execution successful.")
                return True, result.stdout
            else:
                logger.warning("Execution failed with errors.")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            logger.error("Execution timed out.")
            return False, f"Error: Script execution exceeded the {timeout}-second timeout limit."
        except Exception as e:
            logger.error(f"Unexpected execution error: {e}")
            return False, str(e)