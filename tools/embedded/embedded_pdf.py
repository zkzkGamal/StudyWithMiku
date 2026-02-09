from langchain_core.tools import tool
import logging
import multiprocessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def embedded_pdf(pdf_path: str) -> str:
    """Embedded PDF content into the vector store. Returns a process id of the pdf file."""
    try:
        from handlation.pdf_handlation import embedded_pdf as embed_func
        process = multiprocessing.Process(target=embed_func, args=(pdf_path,))
        process.start()
        return f"Background process started with PID: {process.pid}"
    except Exception as e:
        logger.error(f"[TOOL] Embedded PDF error: {e}")
        return f"Error starting background process: {e}"