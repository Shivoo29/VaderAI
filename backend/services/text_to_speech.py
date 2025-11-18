"""Text-to-Speech service with Darth Vader voice"""
import logging
from pathlib import Path
from typing import Optional
import numpy as np
from pydub import AudioSegment
from pydub.effects import low_pass_filter, speedup
import tempfile
import os

logger = logging.getLogger(__name__)


class VaderTTSService:
    """Service for converting text to speech with Darth Vader voice"""

    def __init__(self, pitch_shift: int = -50, speed: float = 0.9):
        """
        Initialize Vader TTS Service

        Args:
            pitch_shift: Pitch shift in semitones (negative = lower)
            speed: Speed multiplier (< 1.0 = slower)
        """
        self.pitch_shift = pitch_shift
        self.speed = speed
        self.breathing_sound = None
        self._load_breathing_sound()

    def _load_breathing_sound(self):
        """Load or generate Vader's breathing sound effect"""
        try:
            # Generate a simple breathing sound effect
            # In production, replace with actual Vader breathing sample
            from scipy import signal
            import numpy as np

            duration = 1.5  # seconds
            sample_rate = 22050

            # Generate brown noise (simulates breathing)
            samples = int(duration * sample_rate)
            noise = np.random.randn(samples)

            # Apply low-pass filter for breathing effect
            b, a = signal.butter(4, 200 / (sample_rate / 2), btype='low')
            breathing = signal.filtfilt(b, a, noise)

            # Add envelope for breathing pattern
            envelope = signal.windows.hann(samples)
            breathing = breathing * envelope

            # Normalize
            breathing = breathing / np.max(np.abs(breathing))
            breathing = (breathing * 32767).astype(np.int16)

            # Convert to AudioSegment
            self.breathing_sound = AudioSegment(
                breathing.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )

            logger.info("Vader breathing sound generated")

        except Exception as e:
            logger.error(f"Error generating breathing sound: {e}", exc_info=True)
            self.breathing_sound = None

    def synthesize(self, text: str, output_path: Optional[str] = None, add_breathing: bool = True) -> str:
        """
        Synthesize text to speech with Vader voice

        Args:
            text: Text to synthesize
            output_path: Output file path (if None, uses temp file)
            add_breathing: Whether to add breathing sound effect

        Returns:
            Path to generated audio file
        """
        try:
            from gtts import gTTS

            # Generate base TTS
            logger.info(f"Generating TTS for: {text}")
            tts = gTTS(text=text, lang='en', slow=False)

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)

            # Load and process audio
            audio = AudioSegment.from_mp3(temp_path)

            # Apply Vader voice effects
            audio = self._apply_vader_effects(audio)

            # Add breathing sound if enabled
            if add_breathing and self.breathing_sound:
                audio = self._add_breathing(audio)

            # Determine output path
            if output_path is None:
                output_path = tempfile.mktemp(suffix='.wav')

            # Export processed audio
            audio.export(output_path, format='wav')

            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

            logger.info(f"Audio saved to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}", exc_info=True)
            raise

    def _apply_vader_effects(self, audio: AudioSegment) -> AudioSegment:
        """
        Apply voice effects to sound like Darth Vader

        Args:
            audio: Input audio segment

        Returns:
            Processed audio segment
        """
        try:
            # Lower pitch (deeper voice)
            # Note: Pitch shifting is complex; this is a simplified approach
            # Slowing down creates a deeper effect
            if self.speed < 1.0:
                speed_factor = 1.0 / self.speed
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * speed_factor)
                })
                audio = audio.set_frame_rate(44100)

            # Apply low-pass filter for that "helmet" effect
            audio = low_pass_filter(audio, 3000)

            # Increase volume slightly
            audio = audio + 3  # 3 dB boost

            # Add slight reverb effect (simulated)
            audio = self._add_reverb(audio)

            return audio

        except Exception as e:
            logger.error(f"Error applying Vader effects: {e}", exc_info=True)
            return audio

    def _add_reverb(self, audio: AudioSegment, decay: float = 0.3) -> AudioSegment:
        """
        Add simple reverb effect

        Args:
            audio: Input audio
            decay: Reverb decay factor

        Returns:
            Audio with reverb
        """
        try:
            # Simple delay-based reverb
            delay_ms = 50
            echo = audio - (20 * decay)  # Reduce volume for echo

            # Combine original with delayed version
            combined = audio.overlay(echo, position=delay_ms)

            return combined

        except Exception as e:
            logger.error(f"Error adding reverb: {e}", exc_info=True)
            return audio

    def _add_breathing(self, audio: AudioSegment) -> AudioSegment:
        """
        Add Vader's breathing sound before speech

        Args:
            audio: Input audio

        Returns:
            Audio with breathing prepended
        """
        try:
            if self.breathing_sound is None:
                return audio

            # Add breathing before speech
            combined = self.breathing_sound + AudioSegment.silent(duration=200) + audio

            return combined

        except Exception as e:
            logger.error(f"Error adding breathing: {e}", exc_info=True)
            return audio

    def synthesize_streaming(self, text: str) -> bytes:
        """
        Synthesize text and return audio bytes for streaming

        Args:
            text: Text to synthesize

        Returns:
            Audio data as bytes
        """
        try:
            temp_path = self.synthesize(text)
            with open(temp_path, 'rb') as f:
                audio_data = f.read()

            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

            return audio_data

        except Exception as e:
            logger.error(f"Error in streaming synthesis: {e}", exc_info=True)
            raise

    def update_settings(self, pitch_shift: Optional[int] = None, speed: Optional[float] = None):
        """
        Update voice settings

        Args:
            pitch_shift: New pitch shift value
            speed: New speed value
        """
        if pitch_shift is not None:
            self.pitch_shift = pitch_shift
        if speed is not None:
            self.speed = speed

        logger.info(f"Updated settings: pitch={self.pitch_shift}, speed={self.speed}")


# Global instance
_tts_service_instance = None


def get_tts_service(pitch_shift: int = -50, speed: float = 0.9) -> VaderTTSService:
    """Get or create TTS service instance"""
    global _tts_service_instance
    if _tts_service_instance is None:
        _tts_service_instance = VaderTTSService(pitch_shift=pitch_shift, speed=speed)
    return _tts_service_instance
