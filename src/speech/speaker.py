import os
import asyncio
import edge_tts
import pygame
from pathlib import Path
from config.settings import settings
from config.logger import logger


class AtlasSpeaker:
    """Orchestrates asynchronous neural speech synthesis and hardware voice emission.

    Interfaces directly with the Edge-TTS framework to transform computational textual content
    into high-fidelity streaming audio files, managing concurrent resource pools and
    non-blocking hardware playback loops using the Pygame audio engine.

    Attributes:
        voice (str): Target neural identifier sequence detailing language and regional accent traits.
        base_path (Path): Structural root workspace boundary constraint tracking cache locations.
        temp_audio_path (Path): File descriptor tracking temporary audio storage items on disk.
    """

    def __init__(self):
        self.voice = settings.EDGE_TTS_VOICE
        self.base_path = settings.BASE_PATH

        self.temp_audio_path = self.base_path / ".atlas_voice_cache.mp3"

        if not pygame.mixer.get_init():
            pygame.mixer.init()
            logger.debug("Pygame Mixer initialized in the module of Speaker.")

    async def speak(self, text: str) -> None:
        """Transforms text matrices into audible voice data with automated cache cleanup.

        Generates an asynchronous communication pipeline, saves intermediate streams,
        loads the binary array buffer into the hardware channel mixer, and handles non-blocking
        sleep cycles until playback parameters evaluate to idle.

        Args:
            text (str): Raw response data targeted for vocal output translation.

        Returns:
            None

        Raises:
            OSError: If cache file operations are blocked by system permission structures.
            Exception: Global handler preventing audio device lockouts from crashing the execution loop.
        """
        if not text or len(text.strip()) == 0:
            return

        logger.debug(
            f"Initiating Edge-TTS speech synthesis for text.: '{text[:30]}...'"
        )

        try:
            communicate = edge_tts.Communicate(text, self.voice, rate="+5%")
            await communicate.save(str(self.temp_audio_path))

            logger.debug("Audio successfully synthesized. Playback starting....")

            pygame.mixer.music.load(str(self.temp_audio_path))
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)

            pygame.mixer.music.unload()

            if os.path.exists(self.temp_audio_path):
                os.remove(self.temp_audio_path)

            logger.debug("Voice playback complete and cache cleared..")

        except Exception as e:
            logger.error(
                f"Failure in the voice synthesis/playback pipeline.: {e}", exc_info=True
            )
