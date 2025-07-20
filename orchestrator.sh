#!/bin/bash
set -eo pipefail

# --- 1. Path Configuration ---
export PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Framework-managed paths
FRAMEWORK_DIR="$PROJECT_ROOT/configs/robot"
FRAMEWORK_LIBS="$FRAMEWORK_DIR/libraries"
FRAMEWORK_RESOURCES="$FRAMEWORK_DIR/resources"
REQUIREMENTS_PATH="$PROJECT_ROOT/requirements"
VIRTUAL_ENV_LIBS="$PROJECT_ROOT/.venv/lib/python3.12/site-packages/robot/libraries/"

# User-defined paths
USER_TESTS_DIR="$PROJECT_ROOT/tests/3_system"
USER_LIBS="$USER_TESTS_DIR/libraries"
USER_RESOURCES="$USER_TESTS_DIR/resources"

# Output paths (auto-created)
LOGS_DIR="$PROJECT_ROOT/logs/3_system/robot_framework"
RESULTS_DIR="$PROJECT_ROOT/results/3_system/robot_framework"
mkdir -p "$LOGS_DIR" "$RESULTS_DIR"

# --- 2. Setup Virtual Environment ---
setup_virtual_environment(){
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        echo "Creating virtual environment..."
        python -m venv "$PROJECT_ROOT/.venv" || { echo "Error: venv creation failed"; exit 1; }
        source "$PROJECT_ROOT/.venv/bin/activate" || { echo "Error: venv activation failed"; exit 1; }
        python -m pip install --upgrade pip || { echo "Error: pip upgrade failed"; exit 1; }
        python -m pip install -r "$REQUIREMENTS_PATH/python-requirements.txt" || { echo "Error: pip install failed"; exit 1; }
    else
        source "$PROJECT_ROOT/.venv/bin/activate"  # Activate existing venv
        python -m pip install --upgrade pip || { echo "Error: pip upgrade failed"; exit 1; }
        python -m pip install -r "$REQUIREMENTS_PATH/python-requirements.txt" || { echo "Error: pip install failed"; exit 1; }
    fi
}

# --- 3. Dynamic Robot Execution ---
run_robot() {
    setup_virtual_environment
    # Add both framework and user paths to Robot's search
    PYTHONPATH="$FRAMEWORK_LIBS:$USER_LIBS:$VIRTUAL_ENV_LIBS:$PYTHONPATH" \
    robot \
        --outputdir "$RESULTS_DIR" \
        --pythonpath "$FRAMEWORK_LIBS:$USER_LIBS" \
        --variablefile "$FRAMEWORK_DIR/configs/env_config.yaml" \
        "$USER_TESTS_DIR/test_suites/"
}

# --- 4. Main ---
run_robot