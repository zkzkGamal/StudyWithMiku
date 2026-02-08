import warnings , logging , environ , pathlib
warnings.filterwarnings("ignore", module="librosa")

from TTS.api import TTS
import sounddevice as sd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#initialize the environment variables
env = environ.Env()
base_dir = pathlib.Path(__file__).parent.parent
environ.Env.read_env(base_dir / '.env') 

MODEL_TTS_NAME = env("MODEL_TTS_NAME" , default="")
MODEL_TTS_TYPE = env("MODEL_TTS_TYPE" , default="tts")

import DiffSinger.utils.hparams as hs
from DiffSinger.inference.ds_variance import DiffSingerVarianceInfer  # Adjust based on actual module

class TTS_INSTANCE:
    def __init__(self):
        if MODEL_TTS_TYPE == "tts":
            self.tts = TTS(MODEL_TTS_NAME, progress_bar=False, gpu=True)
        elif MODEL_TTS_TYPE == "vocoder":
            hs.load_config('DiffSinger/dsconfig.yaml')  # Load config
            self.tts = DiffSingerVarianceInfer()
        else:
            raise ValueError("Invalid model type")

    def speak(self, text):
        if MODEL_TTS_TYPE == "tts":
            speaker = self.tts.speakers[11]
            wav = self.tts.tts(
                text=text,
                speaker=speaker
            )
            sd.play(wav, samplerate=self.tts.synthesizer.output_sample_rate)
            sd.wait()
        elif MODEL_TTS_TYPE == "vocoder":
            pass
            # self.tts.run_inference('path/to/test.ds', out_path='output/test.wav')
        else:
            raise ValueError("Invalid model type")