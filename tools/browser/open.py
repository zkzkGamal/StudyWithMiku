from langchain_core.tools import tool
import subprocess , logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def open_browser(url: str) -> str:
    """Open a URL in the default web browser."""
    try:
        subprocess.Popen(["xdg-open", url])
        logger.info(f"[TOOL] Opened browser to {url}")
        return f"Opened browser to {url}"
    except Exception as e:
        logger.error(f"[TOOL] open_browser error: {e}")
        return f"Error opening browser: {e}"

