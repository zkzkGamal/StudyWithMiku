import subprocess
import logging
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def check_internet() -> str:
    """Checks if the internet is accessible by pinging a reliable host."""
    try:
        # Ping 8.8.8.8 once with a 2-second timeout
        subprocess.check_call(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info("[TOOL] Internet check: Connected")
        return "Connected"
    except subprocess.CalledProcessError:
        logger.warning("[TOOL] Internet check: Disconnected")
        return "Disconnected"
    except Exception as e:
        logger.error(f"[TOOL] Internet check error: {e}")
        return f"Error checking internet: {e}"