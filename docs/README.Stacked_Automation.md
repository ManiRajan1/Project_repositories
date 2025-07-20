# :control_knobs: Stacked Test Automation

A **hybrid test automation framework** for testing from individual components to simulated ECU (Electronic Control Unit) functionalities. Designed for extensibility, this project integrates multiple tools under a unified orchestrator while maintaining isolation of logs/results per testing level.

---

## :hammer_and_wrench: Tech Stack
| Category       | Tools                                                                 |
|----------------|-----------------------------------------------------------------------|
| **E2E/Integration** | Robot Framework, Perl + C Sockets (ECU Sim)                           |
| **Unit Testing**   | pytest (Python), GTest/GMock (C++), Gcov (Coverage)                   |
| **Linting**       | clang-tidy (C), pylint/black (Python), clippy (Rust)                  |
| **Orchestration** | Bash (`orchestrator.sh`)                                              |

---

## :open_file_folder: Folder Structure
```bash
stacked-test-automation/
├── orchestrator.sh            # Master script to trigger frameworks
├── configs/                   # Tool-specific configurations
│   ├── robot/
│   ├── pytest/
│   └── gtest/
├── src/                       # Source code under test
│   ├── ecu_sim/               # C/Perl ECU simulator
│   ├── components/            # Isolated components
│   └── libs/                  # Shared libraries
├── tests/
│   ├── 1_unit/                # Unit tests (per language)
│   │   ├── python/
│   │   ├── cpp/
│   │   └── rust/
│   ├── 2_integration/         # Component integration
│   └── 3_system/              # System-level (Robot Framework)
├── results/                   # **Isolated results by level**
│   ├── unit/
│   ├── integration/
│   └── system/
├── logs/                      # **Separated logs**
│   ├── linter/
│   ├── coverage/
│   ├── interfaces/
|   └── E2E/
└── requirements/              # Tool dependency specs
    ├── python_requirements.txt
    ├── c_toolchain.txt
    └── rust_tools.toml
```

## :arrows_counterclockwise:Integration Rules
New tools must comply with:
- Log/Result Isolation: Outputs must respect the `logs/ and results/ hierarchy`.
- Dependency Specs: Provide a `requirements.txt`-like manifest in `configs/<tool>/`.
- Namespace Safety: No hardcoded paths; use env vars from `orchestrator.sh`.

### Design Philosophy
- Modularity: Each framework operates independently but can be orchestrated.
- Traceability: Clear separation of test levels for debugging.
- Extensibility: New tools integrate via configuration, not code modification.

### Key Features:
- **Level-Based Isolation**: Results/logs auto-sorted by test phase (unit/integration/system).
- **Orchestrator Control**: Centralized toolchain management via `orchestrator.sh`.
- **Language-Agnostic**: Built to support C/Python/Rust with linting/coverage.
- **ECU Simulation Ready**: Includes Perl/C socket components for automotive testing.
