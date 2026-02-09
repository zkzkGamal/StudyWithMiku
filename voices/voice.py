import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import sys , time , webrtcvad , logging
import sounddevice as sd
import numpy as np
import noisereduce as nr
from models.voice import whisper_model


from scipy.io.wavfile import write
from uuid import uuid4

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

vad = webrtcvad.Vad()
vad.set_mode(3)

class VoiceModule:
    def __init__(self):
        self.SAMPLE_RATE = 16000
        self.FRAME_DURATION = 30  # ms
        self.FRAME_SIZE = int(self.SAMPLE_RATE * self.FRAME_DURATION / 1000)
        
    
    def __call__(self, *args, **kwds):
        try:
            audio = self.record_until_silence()
            if audio is None:
                logger.info("No voice detected.")
                return None
            transcription = self.transcribe(audio)
            return transcription
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    
    def is_speech(self,frame):
        pcm = (np.clip(frame, -1, 1) * 32767).astype(np.int16).tobytes()
        return vad.is_speech(pcm, self.SAMPLE_RATE)

    def record_until_silence(self,silence_limit=5.0, max_seconds=5):
        logger.info("Recording...")

        frames = []
        silence_start = None
        start = time.time()

        collected_duration = 0
        required_samples = max_seconds * self.SAMPLE_RATE
        
        with sd.InputStream(
            channels=1, samplerate=self.SAMPLE_RATE, dtype="float32",
            blocksize=self.FRAME_SIZE , device=None , latency="low"
        ) as stream:

            while True:
                frame, _ = stream.read(self.FRAME_SIZE)
                frame = frame.flatten()

                speaking = self.is_speech(frame)

                if speaking:
                    frames.append(frame)
                    silence_start = None
                else:
                    if silence_start is None:
                        silence_start = time.time()
                    else:
                        if time.time() - silence_start >= silence_limit:
                            logger.info("Stopped (silence).")
                            break
                
                if time.time() - start > max_seconds:
                    logger.info("Stopped (time limit).")
                    break
                collected_duration += len(frame)

                progress = min(collected_duration / required_samples * 100, 100)
                sys.stdout.write(f"\rVoice captured: {collected_duration/self.SAMPLE_RATE:.1f}/{max_seconds}s [{int(progress)}%]")

        if len(frames) == 0:
            return None

        raw = np.concatenate(frames)
        clean = nr.reduce_noise(y=raw, sr=self.SAMPLE_RATE)

        return clean
    
    def transcribe(self,audio):
        temp = f"{uuid4()}_temp.wav"
        write(temp, self.SAMPLE_RATE, (audio * 32767).astype(np.int16))
        result = whisper_model.transcribe(temp, language="en" , verbose=True ,temperature=0.7)
        os.remove(temp)
        return result["text"].strip()