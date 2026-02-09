import logging
import os
import sys
from queue import Queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from core.agent import app
from config.database import Database
from langchain_core.prompts import load_prompt

database_config = Database()

# -------------------------
# Logging configuration
# -------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# -------------------------
# Load prompt
# -------------------------
prompt = load_prompt("prompt.yaml").format(home=os.path.expanduser("~"))

# -------------------------
# File watcher handler
# -------------------------
class ContentFolderHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def on_created(self, event):
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            logger.info(f"📄 New file detected → {file_path}")
            self.event_queue.put(("file", file_path))

# -------------------------
# User input thread
# -------------------------
def user_input_thread(event_queue):
    while True:
        try:
            user_input = input("🧑‍💻 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                event_queue.put(("exit", None))
                break
            event_queue.put(("user", user_input))
        except Exception as e:
            logger.error(f"Error in user input thread: {e}")
            event_queue.put(("exit", None))
            break

# -------------------------
# Main Execution
# -------------------------
def main():
    logger.info("🤖 [MAIN] Starting AI assistant...")
    logger.info("Initializing and loading local AI model...")

    # Initialize conversation state
    messages = [SystemMessage(content=prompt)]
    current_state = {"messages": messages, "running_processes": {}}

    # Set up event queue and threads
    event_queue = Queue()

    # Start user input thread
    input_thread = threading.Thread(target=user_input_thread, args=(event_queue,))
    input_thread.daemon = True
    input_thread.start()

    # Set up content folder watcher
    content_path = os.path.join(os.getcwd(), "content")
    os.makedirs(content_path, exist_ok=True)
    logger.info(f"Watching content folder: {content_path}")

    handler = ContentFolderHandler(event_queue)
    observer = Observer()
    observer.schedule(handler, content_path, recursive=False)
    observer.start()

    logger.info("AI Assistant Ready. Type 'exit' or 'quit' to stop.\n")

    # -------------------------
    # Main event loop
    # -------------------------
    while True:
        try:
            event_type, data = event_queue.get()

            if event_type == "exit":
                logger.info("Shutting down assistant...")
                break

            elif event_type == "user":
                user_input = data
                vector_context = database_config.get_content(user_input)
                if vector_context:
                    context_str = "\n\n".join([f"Source: {doc.metadata.get('source', 'unknown')}\nContent: {doc.page_content}" for doc in vector_context])
                    user_input += f"\n\n[Context from vector store]:\n{context_str}"
                msg = HumanMessage(content=f"{user_input}")
                logger.info(f"💬 User prompt injected: {user_input}")

            elif event_type == "file":
                file_path = data
                msg_content = f"user added file to content → {file_path} (embedding in background)"
                msg = HumanMessage(content=msg_content)
                logger.info(f"📥 File addition prompt injected for: {file_path}")

            # Append message to conversation
            current_state["messages"].append(msg)

            # Invoke agent
            current_state = app.invoke(current_state)
            last_msg = current_state["messages"][-1]

            # Display last message
            if isinstance(last_msg, AIMessage):
                print("\n🤖 AI:")
                print(last_msg.content)
                print("\n")
                logger.info(f"📝 AI Response delivered.")

            elif isinstance(last_msg, HumanMessage):
                logger.info(f"[SYSTEM]: {last_msg.content}")

        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt detected. Exiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            continue

    # -------------------------
    # Cleanup
    # -------------------------
    observer.stop()
    observer.join()
    input_thread.join(timeout=1)
    logger.info("Assistant shutdown complete.")


if __name__ == "__main__":
    main()
