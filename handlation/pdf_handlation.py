from preprocessing.pdf import extract_text_from_pdf, split_text_into_chunks
from langchain_core.documents import Document
from config.database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_config = Database()

def embedded_pdf(pdf_path: str) -> str:
    """Embedded PDF content into the vector store. Returns a proccess id of the pdf file."""
    try:
        pdf_data = extract_text_from_pdf(pdf_path)
        if pdf_data is None:
            return "Failed to extract text from the PDF."
        chunks = split_text_into_chunks(pdf_data)
        documents = [Document(page_content=chunk , metadata={"source": pdf_path} , id=i) for i, chunk in enumerate(chunks)]
        database_config.add_documents(documents)
        return f"PDF content embedded successfully with {len(chunks)} chunks."
    except Exception as e:
        return f"Error embedded PDF: {e}"