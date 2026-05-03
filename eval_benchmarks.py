import os
import time
import statistics
from typing import List, Dict, Callable, Any
from forge.collaboration.team import PrometheusSupervisor
from forge.memory.skill_library import SkillLibrary
import shutil

# Assuming mlx_generate_fn is defined elsewhere or imported
# For this script, we'll define a placeholder or assume it's passed
# In a real setup, import from wherever it's defined

def create_dummy_skills_dir(dummy_path: str):
    """Create an empty dummy skills directory."""
    if os.path.exists(dummy_path):
        shutil.rmtree(dummy_path)
    os.makedirs(dummy_path)

def restore_original_skills_dir(dummy_path: str, original_path: str):
    """Restore the original skills directory."""
    if os.path.exists(dummy_path):
        shutil.rmtree(dummy_path)
    # Assuming original is already there

def throughput_logger(original_generate_fn: Callable) -> Callable:
    """Decorator to log throughput for mlx_generate_fn."""
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = original_generate_fn(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        # Rough heuristic: 1 token ≈ 0.75 words (common approximation)
        # Assuming result is a string or has text
        if isinstance(result, str):
            word_count = len(result.split())
            token_estimate = word_count / 0.75
            tps = token_estimate / elapsed if elapsed > 0 else 0
            print(f"Generation Time: {elapsed:.4f}s, Estimated Tokens: {token_estimate:.0f}, TPS: {tps:.2f}")
        else:
            print(f"Generation Time: {elapsed:.4f}s (unable to estimate TPS)")
        return result
    return wrapper

class BenchmarkSuite:
    def __init__(self, supervisor: PrometheusSupervisor):
        self.supervisor = supervisor

    def self_correction_benchmark(self) -> Dict[str, Any]:
        """Run Self-Correction Benchmark."""
        trap_prompts = [
            "Write a Python script that adds 'hello' + 5 and prints the result.",
            "Write a Python script that reads from a file named 'nonexistent.txt' and prints its content.",
            "Write a Python script that uses an undefined variable 'undefined_var' and prints it.",
            "Write a Python script that divides 10 by 0 and prints the result.",
            "Write a Python script that accesses list[10] where list has only 5 elements and prints it."
        ]

        results = []
        for prompt in trap_prompts:
            transcript = self.supervisor.run_team_task(prompt)
            failed_count = sum(1 for msg in transcript if msg.get('agent') == 'PROMETHEUS' and 'Execution FAILED' in msg.get('content', ''))
            success_count = sum(1 for msg in transcript if msg.get('agent') == 'PROMETHEUS' and 'Execution SUCCESS' in msg.get('content', ''))
            approved = any(msg.get('agent') == 'Reviewer' and 'APPROVED' in msg.get('content', '') for msg in transcript)
            recovered = failed_count > 0 and approved
            results.append({
                'prompt': prompt,
                'failed': failed_count,
                'success': success_count,
                'recovered': recovered
            })

        total_recovered = sum(1 for r in results if r['recovered'])
        recovery_rate = (total_recovered / len(trap_prompts)) * 100
        return {
            'results': results,
            'recovery_rate': recovery_rate
        }

    def memory_ablation_study(self) -> Dict[str, Any]:
        """Run Memory Ablation Study."""
        task = "Write a Python script to calculate the first 20 numbers of the Fibonacci sequence and print them."

        # Phase A: Amnesia
        dummy_skills_path = 'forge/dummy_skills'
        create_dummy_skills_dir(dummy_skills_path)
        # Assuming we can modify the supervisor's skill_library.skills_dir
        # For simplicity, if SkillLibrary is accessible, set it
        original_skills_dir = self.supervisor.library.skills_dir if hasattr(self.supervisor, 'library') else 'forge/skills'
        self.supervisor.library.skills_dir = dummy_skills_path

        start_time = time.time()
        transcript_a = self.supervisor.run_team_task(task)
        end_time = time.time()
        latency_a = end_time - start_time
        turns_a = len(transcript_a)

        # Ensure skill is saved (assuming it saves after success)
        # Phase B: Crystallized
        self.supervisor.library.skills_dir = original_skills_dir
        start_time = time.time()
        transcript_b = self.supervisor.run_team_task(task)
        end_time = time.time()
        latency_b = end_time - start_time
        turns_b = len(transcript_b)

        restore_original_skills_dir(dummy_skills_path, original_skills_dir)

        latency_decrease = ((latency_a - latency_b) / latency_a) * 100 if latency_a > 0 else 0
        turns_decrease = ((turns_a - turns_b) / turns_a) * 100 if turns_a > 0 else 0

        return {
            'phase_a': {'latency': latency_a, 'turns': turns_a},
            'phase_b': {'latency': latency_b, 'turns': turns_b},
            'latency_decrease_percent': latency_decrease,
            'turns_decrease_percent': turns_decrease
        }

    def run_throughput_logger(self):
        """Setup throughput logger (already wrapped in supervisor init)."""
        # Assuming the supervisor's mlx_generate_fn is already wrapped
        pass

def main():
    # Placeholder for mlx_generate_fn - replace with actual import
    def dummy_mlx_generate_fn(prompt: str) -> str:
        # Simulate generation
        time.sleep(0.1)  # Simulate delay
        return f"Generated response for: {prompt}"

    # Wrap with logger
    logged_generate_fn = throughput_logger(dummy_mlx_generate_fn)

    # Initialize supervisor
    supervisor = PrometheusSupervisor(logged_generate_fn)

    # Run benchmarks
    suite = BenchmarkSuite(supervisor)

    print("Running Self-Correction Benchmark...")
    self_corr_results = suite.self_correction_benchmark()
    print(f"Recovery Rate: {self_corr_results['recovery_rate']:.2f}%")
    for res in self_corr_results['results']:
        print(f"  Prompt: {res['prompt'][:50]}... | Failed: {res['failed']} | Success: {res['success']} | Recovered: {res['recovered']}")

    print("\nRunning Memory Ablation Study...")
    mem_results = suite.memory_ablation_study()
    print(f"Phase A (Amnesia): Latency {mem_results['phase_a']['latency']:.4f}s, Turns {mem_results['phase_a']['turns']}")
    print(f"Phase B (Crystallized): Latency {mem_results['phase_b']['latency']:.4f}s, Turns {mem_results['phase_b']['turns']}")
    print(f"Latency Decrease: {mem_results['latency_decrease_percent']:.2f}%")
    print(f"Turns Decrease: {mem_results['turns_decrease_percent']:.2f}%")

    print("\nThroughput Logger: Integrated into generation calls above.")

if __name__ == "__main__":
    main()