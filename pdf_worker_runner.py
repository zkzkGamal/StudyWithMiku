import sys
import logging
from preprocessing.pdf import extract_text_from_pdf, split_text_into_chunks
from langchain_core.documents import Document
from config.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_config = Database()

def embed_pdf_worker(pdf_path: str):
    try:
        logger.info(f"[WORKER] Starting PDF embedding for: {pdf_path}")

        pdf_data = extract_text_from_pdf(pdf_path)
        if pdf_data is None:
            logger.error(f"[WORKER] Failed to extract text from PDF: {pdf_path}")
            return

        chunks = split_text_into_chunks(pdf_data)
        documents = [
            Document(page_content=chunk, metadata={"source": pdf_path}, id=i)
            for i, chunk in enumerate(chunks)
        ]

        database_config.add_documents(documents)
        logger.info(f"[WORKER] Successfully embedded PDF with {len(chunks)} chunks.")

    except Exception as e:
        logger.exception(f"[WORKER] Error embedding PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_worker_runner.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    embed_pdf_worker(pdf_path)
