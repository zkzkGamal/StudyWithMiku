from preprocessing.pdf import extract_text_from_pdf, split_text_into_chunks
from langchain_core.documents import Document
from config.database import Database
import logging

logger = logging.getLogger(__name__)

database_config = Database()

def embed_pdf_worker(pdf_path: str) -> str:
    """Actual function that extracts and embeds PDF content."""
    try:
        logger.info(f"[WORKER] Starting PDF embedding for: {pdf_path}")

        pdf_data = extract_text_from_pdf(pdf_path)
        if pdf_data is None:
            logger.error(f"[WORKER] Failed to extract text from PDF: {pdf_path}")
            return "Failed to extract text from the PDF."

        chunks = split_text_into_chunks(pdf_data)
        documents = [
            Document(page_content=chunk, metadata={"source": pdf_path}, id=i)
            for i, chunk in enumerate(chunks)
        ]

        database_config.add_documents(documents)

        logger.info(f"[WORKER] Successfully embedded PDF with {len(chunks)} chunks.")
        return f"PDF content embedded successfully with {len(chunks)} chunks."

    except Exception as e:
        logger.exception(f"[WORKER] Error embedding PDF: {e}")
        return f"Error embedding PDF: {e}"
