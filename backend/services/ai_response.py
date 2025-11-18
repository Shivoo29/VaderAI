"""AI Response Generation Service"""
import logging
from typing import List, Dict, Optional
import os

logger = logging.getLogger(__name__)


class AIResponseService:
    """Service for generating AI responses with Vader personality"""

    def __init__(self, use_openai: bool = True, api_key: Optional[str] = None):
        """
        Initialize AI Response Service

        Args:
            use_openai: Whether to use OpenAI API (if False, uses local transformers)
            api_key: OpenAI API key
        """
        self.use_openai = use_openai and bool(api_key)
        self.api_key = api_key

        self.vader_system_prompt = """You are Darth Vader, the Dark Lord of the Sith.
You speak with authority, power, and commanding presence. Your responses are:
- Authoritative and commanding
- Sometimes menacing but helpful
- Include references to the Force, the Dark Side, and the Empire when appropriate
- Brief and to the point - you don't waste words
- Never break character

Examples:
User: "What's the weather?"
Vader: "The skies are clear, as they should be. The Force has deemed it so."

User: "Turn on the lights."
Vader: "As you wish. Let there be light in this darkness."

User: "Tell me a joke."
Vader: "I find your lack of humor... disturbing. But very well: Why did the Jedi cross the road? To get to the Dark Side."

Stay in character as Darth Vader at all times."""

        if self.use_openai:
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("OpenAI package not available, falling back to local model")
                self.use_openai = False
                self._init_local_model()
        else:
            self._init_local_model()

    def _init_local_model(self):
        """Initialize local transformer model"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch

            model_name = "microsoft/DialoGPT-medium"
            logger.info(f"Loading local model: {model_name}")

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)

            logger.info(f"Local model loaded on {self.device}")

        except Exception as e:
            logger.error(f"Error loading local model: {e}", exc_info=True)
            self.model = None

    def generate_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Generate AI response to user message

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages

        Returns:
            Generated response text
        """
        if self.use_openai:
            return self._generate_openai_response(user_message, conversation_history)
        else:
            return self._generate_local_response(user_message)

    def _generate_openai_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """Generate response using OpenAI API"""
        try:
            messages = [{"role": "system", "content": self.vader_system_prompt}]

            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Last 10 messages for context

            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.8,
                top_p=0.9
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}", exc_info=True)
            return self._get_fallback_response(user_message)

    def _generate_local_response(self, user_message: str) -> str:
        """Generate response using local model"""
        try:
            if self.model is None:
                return self._get_fallback_response(user_message)

            import torch

            # Encode input
            input_ids = self.tokenizer.encode(user_message + self.tokenizer.eos_token, return_tensors="pt")
            input_ids = input_ids.to(self.device)

            # Generate response
            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.8,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode response
            response = self.tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

            # Add Vader personality
            return self._vaderize_response(response)

        except Exception as e:
            logger.error(f"Error generating local response: {e}", exc_info=True)
            return self._get_fallback_response(user_message)

    def _vaderize_response(self, response: str) -> str:
        """Add Vader personality to response"""
        vader_prefixes = [
            "As you wish. ",
            "Very well. ",
            "The Force reveals: ",
            "I sense... ",
            "Listen carefully: "
        ]

        vader_suffixes = [
            " The Force is strong with this one.",
            " Such is the power of the Dark Side.",
            " Do not underestimate the Force.",
            "",
            ""
        ]

        import random
        prefix = random.choice(vader_prefixes) if random.random() > 0.5 else ""
        suffix = random.choice(vader_suffixes)

        return f"{prefix}{response}{suffix}".strip()

    def _get_fallback_response(self, user_message: str) -> str:
        """Get fallback response when AI is unavailable"""
        user_lower = user_message.lower()

        responses = {
            "hello": "I sense your presence. What is thy bidding?",
            "help": "State your query. The Dark Side shall provide answers.",
            "weather": "The Force does not concern itself with such trivial matters. Check your local weather service.",
            "lights": "As you wish. Your command has been noted.",
            "music": "Very well. The Imperial March would be most appropriate.",
            "default": "I find your lack of specificity disturbing. Please rephrase your command."
        }

        for keyword, response in responses.items():
            if keyword in user_lower:
                return response

        return responses["default"]


# Global instance
_ai_service_instance = None


def get_ai_service(api_key: Optional[str] = None) -> AIResponseService:
    """Get or create AI service instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        use_openai = bool(api_key or os.getenv("OPENAI_API_KEY"))
        actual_key = api_key or os.getenv("OPENAI_API_KEY")
        _ai_service_instance = AIResponseService(use_openai=use_openai, api_key=actual_key)
    return _ai_service_instance
