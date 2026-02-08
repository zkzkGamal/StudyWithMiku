import logging , environ , pathlib , os
from langchain_chroma import Chroma
from models.embedding import EmbeddingConfig
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

embedding_model=EmbeddingConfig()

class Database:
    def __init__(self):
        self.documents = not os.path.exists(DB_LOCATION) or not os.listdir(DB_LOCATION)
        try:
            self.vector_store = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=embedding_model.get_embedding_model(),
                persist_directory=DB_LOCATION,
                relevance_score_fn=lambda d: 1 - d, 
            )
            logger.info("Chroma vector store initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize Chroma vector store")
            raise e
        
    def get_vector_store(self):
        return self.vector_store

    def add_document(self, documents):
        if self.documents:
            logger.info("get all documents from the directory")
            loaded_documents = self.vector_store.get()
            if len(documents) >= len(loaded_documents):
                logger.info("Adding documents to the vector store")
                self.vector_store.add_documents(documents)
            else:
                logger.info("Documents already exist in the vector store, skipping addition")
            self.vector_store.persist()
            self.documents = False
        else:
            logger.info("Vector store is already initialized, skipping document addition")
        