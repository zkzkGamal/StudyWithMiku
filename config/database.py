import logging , environ , pathlib
from langchain_chroma import Chroma

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#initialize the environment variables
env = environ.Env()
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / '.env') 

CHROMA_COLLECTION_NAME = env("CHROMA_COLLECTION_NAME" , default="")
DB_LOCATION = env("DB_LOCATION" , default="")

class Database:
    def __init__(self):
        try:
            self.vector_store = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=embedding_function_ollama,
                persist_directory=DB_LOCATION,
                relevance_score_fn=lambda d: 1 - d, 
            )
            logger.info("Chroma vector store initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize Chroma vector store")
            raise e
        
    def get_vector_store(self):
        return self.vector_store
    
    def add_document(self, document):
        self.vector_store.add_documents([document])
        