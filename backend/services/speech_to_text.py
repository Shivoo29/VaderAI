"""Speech-to-Text service using OpenAI Whisper"""
import whisper
import torch
import numpy as np
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechToTextService:
    """Service for converting speech to text using Whisper"""

    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model

        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing Whisper model on {self.device}")

    def load_model(self):
        """Load Whisper model"""
        if self.model is None:
            logger.info(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")

    def transcribe_audio(self, audio_path: str, language: str = "en") -> Optional[str]:
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to audio file
            language: Language code (default: en)

        Returns:
            Transcribed text or None if error
        """
        try:
            self.load_model()

            logger.info(f"Transcribing audio: {audio_path}")
            result = self.model.transcribe(
                audio_path,
                language=language,
                fp16=False if self.device == "cpu" else True
            )

            text = result["text"].strip()
            logger.info(f"Transcription result: {text}")
            return text

        except Exception as e:
            logger.error(f"Error transcribing audio: {e}", exc_info=True)
            return None

    def transcribe_audio_array(self, audio_array: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """
        Transcribe audio from numpy array

        Args:
            audio_array: Audio data as numpy array
            sample_rate: Sample rate of audio

        Returns:
            Transcribed text or None if error
        """
        try:
            self.load_model()

            # Ensure audio is float32 and normalized
            if audio_array.dtype != np.float32:
                audio_array = audio_array.astype(np.float32)

            # Normalize to [-1, 1] if needed
            if audio_array.max() > 1.0 or audio_array.min() < -1.0:
                audio_array = audio_array / np.abs(audio_array).max()

            logger.info(f"Transcribing audio array of length {len(audio_array)}")
            result = self.model.transcribe(
                audio_array,
                language="en",
                fp16=False if self.device == "cpu" else True
            )

            text = result["text"].strip()
            logger.info(f"Transcription result: {text}")
            return text

        except Exception as e:
            logger.error(f"Error transcribing audio array: {e}", exc_info=True)
            return None

    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_size": self.model_size,
            "device": self.device,
            "is_loaded": self.model is not None
        }


# Global instance
_stt_service_instance = None


def get_stt_service(model_size: str = "base") -> SpeechToTextService:
    """Get or create STT service instance"""
    global _stt_service_instance
    if _stt_service_instance is None:
        _stt_service_instance = SpeechToTextService(model_size=model_size)
    return _stt_service_instance
