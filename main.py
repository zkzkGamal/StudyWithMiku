import logging, os, sys
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from core.agent import app
from config.database import Database

database_config = Database()


# from modules.voice_module import VoiceModule
from langchain_core.prompts import load_prompt

# from models.tts import speak

# -------------------------
# Configure logging
# -------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

logger = logging.getLogger(__name__)

# voice_module = VoiceModule()


prompt = load_prompt("prompt.yaml")
prompt = prompt.format(home=os.path.expanduser("~"))


# -------------------------
# Imports for file watching and queuing
# -------------------------
from queue import Queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ContentFolderHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"New file detected: {event.src_path}")
            self.event_queue.put(("file", event.src_path))


def user_input_thread(event_queue):
    while True:
        try:
            user_input = input("Enter your request: ").strip()
            # logger.info("Listening for voice input...")
            # user_input = voice_module()
            # if user_input is None:
            #     logger.info("No valid input detected. Please try again.")
            #     continue
            # logger.info(f"[USER]: {user_input}")
            if not user_input or user_input.lower() in ["exit", "quit"]:
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
    logger.info("[MAIN] Starting AI assistant")

    # Warm-up the model
    logger.info("Initializing and loading local AI model...")

    # Initial State
    messages = [SystemMessage(content=prompt)]

    current_state = {
        "messages": messages,
        "running_processes": {},
    }

    # Set up event queue and threads
    event_queue = Queue()

    # User input thread
    input_thread = threading.Thread(target=user_input_thread, args=(event_queue,))
    input_thread.daemon = True
    input_thread.start()

    # File watcher
    content_path = os.path.join(os.getcwd(), "content")
    if not os.path.exists(content_path):
        os.makedirs(content_path)
        logger.info(f"Created content folder at: {content_path}")

    handler = ContentFolderHandler(event_queue)
    observer = Observer()
    observer.schedule(handler, content_path, recursive=False)
    observer.start()

    logger.info("AI Assistant Ready. Type 'exit' or 'quit' to stop.")
    logger.info(f"Watching content folder: {content_path}")

    while True:
        try:
            event = event_queue.get()
            if event[0] == "exit":
                logger.info("Exiting...")
                break

            if event[0] == "user":
                msg_content = event[1]
                msg = HumanMessage(content=msg_content)
            elif event[0] == "file":
                file_path = os.path.abspath(event[1])
                msg_content = f"user added file to content and path is {file_path} to embedded"
                msg = HumanMessage(content=msg_content)
                logger.info(f"Injecting file addition prompt: {msg_content}")

            current_state["messages"].append(msg)
            final_state = app.invoke(current_state)
            current_state = final_state

            last_msg = current_state["messages"][-1]
            if isinstance(last_msg, AIMessage):
                logger.info(f"\n[AI]: {last_msg.content}\n")
                # speak(last_msg.content)
            elif isinstance(last_msg, HumanMessage):
                logger.info(f"\n[SYSTEM]: {last_msg.content}\n")
                # speak(last_msg.content)

        except KeyboardInterrupt:
            logger.info("\nExiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            continue

    # Cleanup
    observer.stop()
    observer.join()
    input_thread.join(timeout=1)


if __name__ == "__main__":
    main()