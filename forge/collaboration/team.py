import json
import logging
from typing import List, Dict
from forge.collaboration.sandbox import ExecutionSandbox
from forge.memory.skill_library import SkillLibrary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PROMETHEUS-Team")

class Agent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    def generate_response(self, context: str, mlx_generate_fn) -> str:
        prompt = f"<|im_start|>system\n{self.system_prompt}<|im_end|>\n<|im_start|>user\nContext:\n{context}\n\nProvide your contribution:<|im_end|>\n<|im_start|>assistant\n"
        return mlx_generate_fn(prompt)

class PrometheusSupervisor:
    def __init__(self, mlx_generate_fn):
        self.mlx_generate_fn = mlx_generate_fn
        self.sandbox = ExecutionSandbox()
        self.library = SkillLibrary()
        
        # Inject known skills directly into the Researcher's brain
        known_skills = self.library.get_available_skills()
        
        self.agents: Dict[str, Agent] = {
            "Researcher": Agent(
                "Researcher", 
                "Data & Logic Gatherer", 
                f"You are an expert technical researcher. Analyze the request. Check if we already have a skill for this in memory:\n\n{known_skills}\n\nIf we do, instruct the Coder to use the known approach. Otherwise, provide a new structured breakdown."
            ),
            "Coder": Agent(
                "Coder", 
                "Implementation Specialist", 
                "You are a senior software engineer. Write clean, production-ready Python code based on the context. ALWAYS wrap your final code in a ```python block. If you receive an error log from a previous execution, analyze it and provide the fixed code."
            ),
            "Reviewer": Agent(
                "Reviewer", 
                "Quality Assurance", 
                "You are a strict code reviewer. Review the execution results and the final code. If perfect and the sandbox execution succeeded, reply ONLY with 'APPROVED'. Otherwise, provide strict feedback."
            )
        }

    def run_team_task(self, task_description: str) -> List[Dict[str, str]]:
        transcript = []
        context = f"Main Task: {task_description}\n"
        
        logger.info(f"PROMETHEUS initiating team task: {task_description}")

        logger.info("Agent: Researcher is thinking...")
        research_output = self.agents["Researcher"].generate_response(context, self.mlx_generate_fn)
        transcript.append({"agent": "Researcher", "content": research_output})
        context += f"\nResearcher says: {research_output}"

        max_retries = 3
        success = False
        
        for attempt in range(max_retries):
            logger.info(f"Agent: Coder is building (Attempt {attempt + 1}/{max_retries})...")
            code_output = self.agents["Coder"].generate_response(context, self.mlx_generate_fn)
            transcript.append({"agent": "Coder", "content": code_output})
            context += f"\nCoder says: {code_output}"

            logger.info("PROMETHEUS executing code in Sandbox...")
            transcript.append({"agent": "PROMETHEUS", "content": f"Executing iteration {attempt + 1} in Sandbox..."})
            
            success, execution_result = self.sandbox.execute_python_code(code_output)
            
            if success:
                logger.info("Sandbox Execution: SUCCESS")
                sandbox_msg = f"Execution SUCCESS. Output:\n{execution_result}"
                transcript.append({"agent": "PROMETHEUS", "content": sandbox_msg})
                context += f"\nSandbox Result: {sandbox_msg}"
                break
            else:
                logger.warning(f"Sandbox Execution: FAILED. Feeding errors back to Coder.")
                sandbox_msg = f"Execution FAILED. Error Traceback:\n{execution_result}\nCoder, please fix the errors and provide updated code."
                transcript.append({"agent": "PROMETHEUS", "content": sandbox_msg})
                context += f"\nSandbox Result: {sandbox_msg}"

        logger.info("Agent: Reviewer is evaluating...")
        review_output = self.agents["Reviewer"].generate_response(context, self.mlx_generate_fn)
        transcript.append({"agent": "Reviewer", "content": review_output})
        
        if "APPROVED" in review_output.upper():
            logger.info("PROMETHEUS: Task successfully approved by Reviewer. Crystallizing Skill.")
            transcript.append({"agent": "PROMETHEUS", "content": "Task completed and verified successfully. Crystallizing code into Long-Term Memory."})
            
            # TRIGGER LONG TERM MEMORY
            self.library.crystallize_skill(task_description, transcript)
        else:
            logger.warning("PROMETHEUS: Final review flagged issues.")
            transcript.append({"agent": "PROMETHEUS", "content": "Task requires manual review. Code execution and verification loop complete."})

        return transcript
