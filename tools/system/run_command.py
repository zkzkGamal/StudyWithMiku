from langchain_core.tools import tool
import subprocess , logging

@tool
def run_command(command: str) -> str:
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"