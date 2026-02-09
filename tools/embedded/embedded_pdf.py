from langchain_core.tools import tool
import logging
import subprocess
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def embedded_pdf(pdf_path: str) -> str:
    """Run PDF embedding in a new terminal window and return PID/log info."""
    try:
        logger.info(f"[TOOL] Launching PDF embedding for {pdf_path} in a new terminal")

        # Build the command to run the worker script in a new terminal
        python_executable = sys.executable  # current python interpreter
        worker_script = os.path.abspath("pdf_worker_runner.py")  # we'll create this next

        # Cross-platform terminal launching
        if sys.platform.startswith("linux") or sys.platform == "darwin":
            # Linux / macOS: gnome-terminal / xterm
            cmd = ["gnome-terminal", "--", python_executable, worker_script, pdf_path]
        elif sys.platform.startswith("win"):
            # Windows: use start cmd
            cmd = ["cmd", "/c", "start", "python", worker_script, pdf_path]
        else:
            return "Unsupported OS for opening a new terminal."

        # Launch the new terminal
        process = subprocess.Popen(cmd)
        logger.info(f"[TOOL] Background process started in new terminal with PID: {process.pid}")

        return f"PDF embedding started in a new terminal (PID: {process.pid})"

    except Exception as e:
        logger.exception(f"[TOOL] Error launching background PDF embedding")
        return f"Error starting background process: {e}"
