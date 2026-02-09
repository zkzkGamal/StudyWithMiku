import logging , environ , pathlib
from typing import Literal
from models.LLM import LLM
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from core.state import AgentState
from core.tools import __all__ as tool_functions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env = environ.Env()
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / '.env')

# -------------------------
# Initialize Model and Tools
# -------------------------
# We lazy-load the chain to avoid import-time side effects
_model_chain = None
llm = LLM().initialize()

def get_model_chain():
    global _model_chain
    if _model_chain is None:
        logger.info("[MODEL INIT] Lazily binding tools to ChatOllama")
        _model_chain = llm.bind_tools(tool_functions)
        logger.info("[MODEL INIT] Model initialized and tools bound")
    return _model_chain


# -------------------------
# Node Definitions
# -------------------------


def call_model(state: AgentState):
    """
    The main agent node.
    It handles:
    1. Checking for pending confirmations.
    2. Invoking the LLM.
    """
    messages = state["messages"]

    # Debug logging for context tracking
    logger.info(f"[AGENT] Processing with {len(messages)} messages in context")

    # 1. Normal AI Invocation
    # Lazy load the model chain if not ready
    chain = get_model_chain()
    response = chain.invoke(messages , config={"max_output_tokens": env("MAX_OUTPUT_TOKEN", default=512)})
    logger.info(f"[MODEL RESPONSE] {response.content}")

    return {"messages": [response]}


def should_continue(state: AgentState) -> Literal["tools", "__end__", "call_model"]:
    """
    Determine the next node.
    """
    messages = state["messages"]
    last_message = messages[-1]
    pending_confirmation = state.get("pending_confirmation", {})

    if pending_confirmation and pending_confirmation.get("tool_name"):
        return END

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return END


# -------------------------
# Graph Construction
# -------------------------
graph = StateGraph(AgentState)

graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools=tool_functions))

graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "__end__": END,
        "call_model": "agent",  # Not used currently but good for loops
    },
)

graph.add_edge("tools", "agent")

app = graph.compile()