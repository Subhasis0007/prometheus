# Prometheus: Deterministic Multi-Agent State Machine for Edge-Compute

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: MLX](https://img.shields.io/badge/Engine-MLX-blue.svg)](https://github.com/ml-explore/mlx)
[![Hardware: Apple Silicon](https://img.shields.io/badge/Hardware-Apple%20Silicon-silver.svg)]()

**Prometheus** is a zero-dependency, local-first cognitive architecture for multi-agent systems, optimized specifically for Apple Silicon via the **MLX** framework. Unlike traditional agent frameworks that rely on cloud-hosted inference and probabilistic orchestration, Prometheus implements a deterministic state machine with a closed-loop execution environment.

---

## 🧠 Key Research Innovations

### 1. Isolated Execution Environment (IEE) & Self-Correction
Prometheus does not treat code generation as a terminal act. All generated Python artifacts are subjected to runtime evaluation within an isolated sandbox.

- **Closed-Loop Debugging:** Standard error (stderr) tracebacks are captured and fed directly back to the Coder agent.  
- **Autonomous Recovery:** The system achieves a **100.00% Recovery Rate** on common failure modes (TypeErrors, ZeroDivision, FileNotFoundError, etc.) within a 3-iteration limit.

---

### 2. Non-Parametric Skill Crystallization
To solve "Agent Amnesia" without the overhead of Vector RAG, Prometheus employs **Skill Crystallization**. Verified, execution-proven code is extracted from the transcript and persisted as structured Markdown artifacts. These are injected directly into the Researcher's context on subsequent runs, bypassing trial-and-error reasoning cycles.

---

### 3. High-Throughput Edge Orchestration
By leveraging Unified Memory on Apple Silicon, Prometheus eliminates the network latency inherent in cloud-based multi-agent systems.

- **Peak Throughput:** Over **21,000+ Tokens Per Second (TPS)**  
- **Reasoning Baseline:** Sustained **~1,300 TPS** during complex multi-agent coordination  

---

## 🏗 System Architecture

Prometheus orchestrates a deterministic transition between three specialized agents:

1. **The Researcher:** Analyzes tasks and queries the **Skill Library** for existing verified solutions.  
2. **The Coder:** Generates executable Python artifacts based on the research plan.  
3. **The Reviewer:** Validates code logic and observes IEE output to issue an `APPROVED` token.  

---

## ⚡ Getting Started

### Prerequisites
- **Hardware:** Apple Silicon (M1, M2, M3, M4)  
- **Environment:** macOS 14.0+  
- **Inference Engine:** MLX-LM  

---

### Installation

```bash
# Clone the repository
git clone https://github.com/Subhasis0007/prometheus.git
cd prometheus

# Initialize the virtual environment
python3 -m venv forge_venv
source forge_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Running the Supervisor

Launch the local dashboard to begin task orchestration:

```bash
python3 -m forge.forge
```

---

## 📊 Benchmarking Results (Empirical Data)

The following metrics were gathered locally on a MacBook Air (M-series) using the `eval_benchmarks.py` suite:

| Category     | Metric                          | Result      |
|--------------|--------------------------------|------------|
| Robustness   | Self-Correction Recovery Rate  | 100.00%    |
| Speed        | Peak Throughput (Local)        | 21,331 TPS |
| Efficiency   | Compute Cost per Task          | $0.00      |
| Reliability  | Verification Protocol          | IEE Sandbox + Reviewer Feedback |

---

## 📚 Academic Citation

If you use this architecture in your research, please cite our preprint:

```bibtex
@article{nanda2026prometheus,
  title={Prometheus: A Deterministic Multi-Agent State Machine with Non-Parametric Skill Crystallization for Edge-Compute},
  author={Nanda, Subhasis},
  journal={arXiv preprint},
  year={2026}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.