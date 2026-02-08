from langchain_ollama import ChatOllama
import environ , pathlib , logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#initialize the environment variables
env = environ.Env()
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / '.env') 

MODEL_NAME = env("MODEL_NAME" , default="")
MODEL_TYPE = env("MODEL_TYPE" , default="")

class LLM:
    def __init__(self):
        self.model = None
        if MODEL_TYPE == "ollama":
            self.model = ChatOllama(
                model=MODEL_NAME,
                temperature=0.5,
                timeout=30,
                base_url=env("OLLAMA_BASE_URL"),
                num_thread=6,
                num_gpu=1,
                top_k=20,
                use_mmap=True,
                keep_alive=1000000
            )
        elif MODEL_TYPE == "google":
            self.model = ChatGoogleGenerativeAI(
                model=MODEL_NAME,
                temperature=0.5,
                timeout=30,
                api_key=env("GOOGLE_API_KEY"),
            )
        elif MODEL_TYPE == "openai":
            self.model = ChatOpenAI(
                model=MODEL_NAME,
                temperature=0.5,
                timeout=30,
                api_key=env("OPENAI_API_KEY"),
            )
        else:
            raise ValueError("Invalid model type")
        
        return self.model
    
    