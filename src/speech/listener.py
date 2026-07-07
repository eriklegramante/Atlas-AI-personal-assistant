import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from config.settings import settings
from config.logger import logger


class AtlasListener:
    """Manages raw audio hardware ingestion and coordinates automated speech-to-text processing.

    Utilizes localized sounddevice input streams to capture sound pressure arrays,
    and forwards flattened float structures down into an int8-quantized Faster-Whisper
    pipeline featuring pre-compiled phonetic injection tokens.

    Attributes:
        model_size (str): Scale tag tracking the depth of the whisper transformer architecture.
        model (WhisperModel): Local execution layout handling speech decoding actions.
        sample_rate (int): Digitization pulse parameter tracking input stream slices.
        phonetic_prompt (str): Keyword vocabulary arrays forcing target word recognition.
    """

    def __init__(self):
        self.model_size = "small"
        logger.info(
            f"Loading phonetic transcription template Faster-Whisper ({self.model_size})..."
        )

        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.sample_rate = 16000

        self.phonetic_prompt = "ATLAS, Root, Root-Alpha, Linux, Ubuntu, Python, White Hat, hardware, CPU, RAM."

    def listen(self, duration: int = 4) -> str:
        """Captures realtime hardware acoustic signals and converts them to digital strings.

        Blocks execution for the assigned duration, captures hardware audio buffers via
        sounddevice, flattens mathematical arrays, and applies a beam search transcription
        pass bound to explicit language rules.

        Args:
            duration (int, optional): The timeline width allocating device window capture. Defaults to 4.

        Returns:
            str: Evaluated text representation extracted from the recorded vocal wave,
                or empty string if anomalies occur.
        """
        try:
            logger.debug(
                f"Microphone activated. Capturing stream by {duration} seconds..."
            )

            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
            )
            sd.wait()

            audio_segments = audio_data.flatten()

            segments, info = self.model.transcribe(
                audio_segments,
                language="pt",
                beam_size=5,
                initial_prompt=self.phonetic_prompt,
            )

            transcription = "".join([segment.text for segment in segments]).strip()

            if transcription:
                logger.info(f"[STT RAW]: {transcription}")
            return transcription

        except Exception as e:
            logger.error(f"Audio capture or transcription failure: {e}", exc_info=True)
            return ""
