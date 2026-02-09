import pypdf
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=300):
    """Split text into chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)
# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        # Open the PDF file
        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return None