import os
import signal
import logging
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from core.state import AgentState

logger = logging.getLogger(__name__)


@tool
def kill_process(state: AgentState, process_name: str = "deploy_script") -> AgentState:
    """Kills a running process managed by the agent."""
    running_processes = state.get("running_processes", {})
    pid = running_processes.get(process_name)

    if not pid:
        state["messages"].append(
            SystemMessage(
                content=f"[ERROR] No running process found with name: {process_name}"
            )
        )
        return state

    try:
        os.kill(pid, signal.SIGTERM)
        logger.info(f"[TOOL] Killed process {process_name} with PID {pid}")
        state["messages"].append(
            SystemMessage(
                content=f"[SUCCESS] Process {process_name} (PID: {pid}) has been terminated."
            )
        )
        del state["running_processes"][process_name]
    except ProcessLookupError:
        state["messages"].append(
            SystemMessage(
                content=f"[WARNING] Process {process_name} (PID: {pid}) was not found. It may have already exited."
            )
        )
        if process_name in state["running_processes"]:
            del state["running_processes"][process_name]
    except Exception as e:
        logger.error(f"[TOOL] Failed to kill process {process_name}: {e}")
        state["messages"].append(
            SystemMessage(content=f"[ERROR] Failed to kill process {process_name}: {e}")
        )

    return state
