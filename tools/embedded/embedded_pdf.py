from langchain_core.tools import tool
import logging
import multiprocessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def embedded_pdf(pdf_path: str) -> str:
    """Run PDF embedding in background and return process ID."""
    try:
        from handlation.pdf_handlation import embed_pdf_worker  # <-- renamed function

        logger.info(f"[TOOL] Launching background process for {pdf_path}")

        process = multiprocessing.Process(
            target=embed_pdf_worker,
            args=(pdf_path,)
        )
        process.start()

        logger.info(f"[TOOL] Background process started with PID: {process.pid}")

        return f"Background embedding started with PID: {process.pid}"

    except Exception as e:
        logger.exception(f"[TOOL] Embedded PDF error")
        return f"Error starting background process: {e}"