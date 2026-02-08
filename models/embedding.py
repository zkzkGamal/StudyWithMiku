import logging, environ, pathlib
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# initialize the environment variables
env = environ.Env(DEBUG=(bool, False))
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / ".env")

# Initialize the Google Generative AI client and Database
EMBEDDING_MODEL_NAME = env("EMBEDDING_MODEL_NAME")

class EmbeddingConfig:
    def __init__(self):
        self.embedding_model_name = env("EMBEDDING_MODEL_NAME")
        self.embedding_model_type = env("EMBEDDING_MODEL_TYPE")
    
    def __call__(self, text: str) -> list[float]:
        if self.embedding_model_type == "google":
            return self.get_text_embedding(text, self.embedding_model_name)
        elif self.embedding_model_type == "ollama":
            return self.get_text_embedding_ollama(text, self.embedding_model_name)
    
    def get_embedding_model(self):
        if self.embedding_model_type == "google":
            return GoogleGenerativeAIEmbeddings(model=self.embedding_model_name, api_key=env("api_key"))
        elif self.embedding_model_type == "ollama":
            return OllamaEmbeddings(model=self.embedding_model_name, base_url=env("OLLAMA_BASE_URL"))
        else:
            raise ValueError("Invalid embedding model type")

    def get_text_embedding(self,text: str, EMBEDDING_MODEL_NAME) -> list[float]:
        if not text:
            return []
        try:
            embedding = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME, api_key=env("api_key"))
            embedding_result = embedding.embed_query(text=text)
            return embedding_result
        except Exception as e:
            logger.error(f"Embedding Error: sleep for 60 seconds")
            import time

            time.sleep(60)
            return []

    def get_text_embedding_ollama(self,text: str, model: str = EMBEDDING_MODEL_NAME) -> list[float]:
        """Generate an embedding for a given text using Ollama."""
        if not text:
            return []

        try:
            response = OllamaEmbeddings(
                model=model,
                base_url=env("OLLAMA_BASE_URL"),
                
            )
            return response.embed_query(text)

        except Exception as e:
            logger.error(f"Ollama embedding error: {e}", exc_info=True)
            return []
    
    

