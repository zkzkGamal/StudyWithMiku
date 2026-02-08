import logging, environ, psycopg2, pathlib , ollama
import google.generativeai as genai
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
genai.configure(api_key=env("api_key"))
EMBEDDING_MODEL_NAME = env("EMBEDDING_MODEL_NAME")

class EmbeddingConfig:
    def __init__(self):
        self.embedding_model_name = env("EMBEDDING_MODEL_NAME")
        self.embedding_model_type = env("EMBEDDING_MODEL_TYPE")
    
    def __call__(self, text: str) -> list[float]:
        if self.embedding_model_type == "google":
            return self.get_text_embedding(text, self.embedding_model_name, genai)
        elif self.embedding_model_type == "ollama":
            return self.get_text_embedding_ollama(text, self.embedding_model_name)


    def get_text_embedding(self,text: str, EMBEDDING_MODEL_NAME, genai) -> list[float]:
        if not text:
            return []
        try:
            embedding_result = genai.embed_content(model=EMBEDDING_MODEL_NAME, content=text)
            return embedding_result["embedding"]
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
            response = ollama.embeddings(
                model=model,
                prompt=text,
            )
            return response["embedding"]

        except Exception as e:
            logger.error(f"Ollama embedding error: {e}", exc_info=True)
            return []

