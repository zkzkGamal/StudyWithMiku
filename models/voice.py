import logging
import whisper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Loading Whisper...")
whisper_model = whisper.load_model("small", device="cpu").cpu()
logger.info("Whisper loaded.\n")