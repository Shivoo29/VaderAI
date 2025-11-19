"""Audio utility functions"""
import numpy as np
import wave
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def load_wav_file(file_path: str) -> Tuple[np.ndarray, int]:
    """
    Load WAV file and return audio data and sample rate

    Args:
        file_path: Path to WAV file

    Returns:
        Tuple of (audio_data, sample_rate)
    """
    try:
        with wave.open(file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            audio_data = wav_file.readframes(n_frames)

            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Convert to float32 and normalize
            audio_array = audio_array.astype(np.float32) / 32768.0

            return audio_array, sample_rate
    except Exception as e:
        logger.error(f"Error loading WAV file {file_path}: {e}")
        raise


def save_wav_file(file_path: str, audio_data: np.ndarray, sample_rate: int):
    """
    Save audio data to WAV file

    Args:
        file_path: Path to save WAV file
        audio_data: Audio data as numpy array
        sample_rate: Sample rate in Hz
    """
    try:
        # Ensure audio is in the correct format
        if audio_data.dtype != np.int16:
            # Convert float to int16
            audio_data = (audio_data * 32767).astype(np.int16)

        with wave.open(file_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        logger.info(f"Saved audio to {file_path}")
    except Exception as e:
        logger.error(f"Error saving WAV file {file_path}: {e}")
        raise


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    """
    Normalize audio data to [-1, 1] range

    Args:
        audio_data: Audio data as numpy array

    Returns:
        Normalized audio data
    """
    max_val = np.abs(audio_data).max()
    if max_val > 0:
        return audio_data / max_val
    return audio_data


def calculate_audio_duration(audio_data: np.ndarray, sample_rate: int) -> float:
    """
    Calculate duration of audio in seconds

    Args:
        audio_data: Audio data as numpy array
        sample_rate: Sample rate in Hz

    Returns:
        Duration in seconds
    """
    return len(audio_data) / sample_rate
