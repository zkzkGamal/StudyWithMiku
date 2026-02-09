import logging
import os
import pathlib
from typing import List

import environ
from langchain_chroma import Chroma
from langchain_core.documents import Document

from models.embedding import EmbeddingConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize environment variables
env = environ.Env()
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / '.env')

CHROMA_COLLECTION_NAME = env("CHROMA_COLLECTION_NAME", default="default_collection")
DB_LOCATION = env("DB_LOCATION", default="./chroma_db")

embedding_model = EmbeddingConfig()

class Database:
    def __init__(self):
        try:
            self.vector_store = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=embedding_model.get_embedding_model(),
                persist_directory=DB_LOCATION,
                relevance_score_fn=lambda d: 1 - d,
            )
            self.min_relevance_threshold = float(env("EMBEDDEDING_TRESHOLD", default=0.0))
            logger.info("Chroma vector store initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize Chroma vector store")
            raise e

    def get_vector_store(self):
        return self.vector_store

    def add_documents(self, documents: List[Document]):
        if not documents:
            logger.info("No documents provided, skipping addition")
            return

        source = documents[0].metadata.get("source")
        if not source:
            logger.warning("No source metadata found in documents, skipping addition")
            return

        # Generate unique IDs for documents if not set
        for i, doc in enumerate(documents):
            if doc.id is None:
                doc.id = f"{os.path.basename(source)}:{i}"

        # Check existing documents for this source
        existing = self.vector_store.get(where={"source": source})
        existing_count = len(existing.get("documents", []))

        if existing_count == len(documents):
            logger.info(f"Documents for source '{source}' already exist with matching count, skipping addition")
            return

        # If mismatch, delete existing and add new
        if existing_count > 0:
            logger.info(f"Count mismatch for source '{source}' (existing: {existing_count}, new: {len(documents)}), replacing documents")
            self.vector_store.delete(ids=existing["ids"])

        logger.info(f"Adding {len(documents)} documents for source '{source}' to the vector store")
        self.vector_store.add_documents(documents)
        self.vector_store.persist()

    def get_content(self, query: str, k: int = 4, min_relevance: float = 0.0) -> List[Document]:
        results = self.vector_store.similarity_search_with_relevance_scores(query, k=k)
        filtered = [doc for doc, score in results if score >= min_relevance]
        if not filtered:
            logger.info(f"No documents met the relevance threshold of {min_relevance}")
        return filtered