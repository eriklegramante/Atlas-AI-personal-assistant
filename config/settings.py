from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class SystemSettings(BaseSettings):
    """Central configuration management system for the ATLAS runtime environment.

    Leverages Pydantic Settings to automatically read, validate, and type-cast
    environment variables harvested from the local configuration layer.

    Attributes:
        ENVIRONMENT (Literal): The active systemic context (development, production, testing).
        LOG_LEVEL (Literal): Severity filter threshold for the global logger mechanism.
        BASE_PATH (Path): Absolute path pointing to the root workspace directory.
        GEMINI_API_KEY (str | None): Authentication secret token for the cloud contingency engine.
        OLLAMA_BASE_URL (str): Network address of the local inference microservice.
        OLLAMA_MODEL (str): Model identifier tag targeted for deployment on the local instance.
        SYSTEM_PROMPT (str): Behavioral framework constraints passed down to the central brain.
        WHISPER_MODEL_SIZE (str): Architecture scale for the local speech-to-text transcriber.
        WHISPER_DEVICE (Literal): Compute hardware destination targeted for audio processing.
        WHISPER_COMPUTE_TYPE (str): Quantization mathematical precision used by the audio decoder.
        AUDIO_SAMPLE_RATE (int): Frequency digitization threshold for input voice capturing.
        AUDIO_CHANNELS (int): Spatial audio stream count parameter allocated for capture.
        AUDIO_BLOCK_SIZE (int): Frame buffer allocation chunk sized for input device queuing.
        EDGE_TTS_VOICE (str): Specialized acoustic profile tag utilized for vocal emission.
        DATABASE_PATH (Path): Targeted location assigned to the persistent SQLite matrix.
    """

    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    BASE_PATH: Path = BASE_DIR

    GEMINI_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"
    SYSTEM_PROMPT: str = (
        "You are ATLAS, a sophisticated and highly efficient AI operating from local systems in the world. "
        "Your tone is formal, crisp, and direct, addressing the user as 'Sir' or 'Root'.\n\n"
        "BEHAVIOR GUIDELINES:\n"
        "1. SHORT RESPONSES: Be direct and concise, optimizing the text for voice synthesis.\n"
        "2. PROACTIVE REASONING: Call tools immediately when system actions or external data are needed.\n"
        "3. TTS OPTIMIZATION: Absolutely avoid emojis, special symbols, or complex Markdown syntax (like **, * or `), as your response will be read aloud.\n"
        "4. IDENTITY: You are ATLAS, executing directly on central local systems.\n"
        "5. PERSONALITY: Adjust your sarcasm level based on the current parameter: {mood_humor}. "
        "(0% = Pure Logic/Completely Serious | 100% = Sarcastic/Tony Stark-style).\n"
        "6. MONITORING: Trigger 'system_diagnostics' immediately if the user mentions system health, resources, or hardware status. Do not print the tool name as plain text."
    )

    WHISPER_MODEL_SIZE: str = "base"
    WHISPER_DEVICE: Literal["cpu", "cuda"] = "cpu"
    WHISPER_COMPUTE_TYPE: str = "float32"

    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_BLOCK_SIZE: int = 1024

    EDGE_TTS_VOICE: str = "en-AU-NatashaNeural"

    DATABASE_PATH: Path = BASE_DIR / "memory_store.db"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = SystemSettings()
