from langchain_core.tools import tool
import logging , subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def find_process(process_name: str) -> str:
    """Find a process by name."""
    logger.info(f"[TOOL] find_process called with process_name={process_name}")
    try:
        result = subprocess.run(["pgrep", process_name], stdout=subprocess.PIPE)
        if result.returncode == 0:
            return f"Process {process_name} found with PID {result.stdout.decode().strip()}"
        else:
            return f"Process {process_name} not found"
    except Exception as e:
        logger.error(f"[TOOL] find_process error for process_name={process_name}: {e}")
        return f"Error finding process {process_name}: {e}"
