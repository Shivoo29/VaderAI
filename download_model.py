"""Download required AI models"""
import whisper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_whisper_model(model_size: str = "base"):
    """
    Download Whisper model for speech recognition

    Args:
        model_size: Model size (tiny, base, small, medium, large)
    """
    logger.info(f"Downloading Whisper {model_size} model...")
    try:
        model = whisper.load_model(model_size)
        logger.info(f"Whisper {model_size} model downloaded successfully!")
        return model
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise


def download_transformers_models():
    """Download transformer models for AI responses"""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM

        logger.info("Downloading DialoGPT model...")
        model_name = "microsoft/DialoGPT-medium"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        logger.info("DialoGPT model downloaded successfully!")
        return tokenizer, model

    except Exception as e:
        logger.error(f"Error downloading transformer models: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("Vader AI - Model Download Script")
    print("=" * 60)
    print()

    # Download Whisper model
    print("Step 1: Downloading Whisper model for speech recognition...")
    download_whisper_model("base")
    print()

    # Download transformer models
    print("Step 2: Downloading AI response generation models...")
    download_transformers_models()
    print()

    print("=" * 60)
    print("All models downloaded successfully!")
    print("You can now run the Vader AI platform.")
    print("=" * 60)
