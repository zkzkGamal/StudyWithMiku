import logging
from langchain_chroma import Chroma
logger.info("Initializing Chroma vector store")
try:
    vector_store = Chroma(
        collection_name=chroma_collection_name,
        embedding_function=embedding_function_ollama,
        persist_directory=db_location,
        relevance_score_fn=lambda d: 1 - d, 
    )
    logger.info("Chroma vector store initialized successfully")
except Exception as e:
    logger.exception("Failed to initialize Chroma vector store")
    raise e