import subprocess
import logging
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def enable_wifi() -> str:
    """Enables Wi-Fi using nmcli."""
    try:
        subprocess.check_call(["nmcli", "radio", "wifi", "on"])
        logger.info("[TOOL] Wi-Fi enabled successfully")
        return "Wi-Fi enabled successfully. Please wait a moment for connection."
    except FileNotFoundError:
        return "Error: nmcli not found. Cannot manage Wi-Fi."
    except subprocess.CalledProcessError as e:
        logger.error(f"[TOOL] Failed to enable Wi-Fi: {e}")
        return f"Failed to enable Wi-Fi: {e}"
    except Exception as e:
        logger.error(f"[TOOL] Enable Wi-Fi error: {e}")
        return f"Error enabling Wi-Fi: {e}"