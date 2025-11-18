"""Voice processing API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import logging
import os
import tempfile
import aiofiles

from backend.core import get_db, get_current_user_id, settings
from backend.models import User, Conversation, Message, MessageRole
from backend.services import SpeechToTextService, AIResponseService, VaderTTSService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Voice Processing"])

# Initialize services
stt_service = SpeechToTextService()
ai_service = AIResponseService(api_key=settings.OPENAI_API_KEY if settings.OPENAI_API_KEY else None)
tts_service = VaderTTSService()


class VoiceRequest(BaseModel):
    """Voice processing request"""
    conversation_id: Optional[int] = None


class TextRequest(BaseModel):
    """Text-based request (for testing/debugging)"""
    text: str
    conversation_id: Optional[int] = None


class VoiceResponse(BaseModel):
    """Voice processing response"""
    transcribed_text: str
    vader_response: str
    audio_url: str
    conversation_id: int
    message_id: int


@router.post("/process", response_model=VoiceResponse)
async def process_voice(
    audio: UploadFile = File(...),
    conversation_id: Optional[int] = None,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Process voice input end-to-end

    1. Transcribe audio to text (STT)
    2. Generate AI response
    3. Convert response to Vader voice (TTS)
    4. Save conversation history
    """
    try:
        # Get user preferences
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Save uploaded audio
        temp_audio_path = tempfile.mktemp(suffix='.wav')
        async with aiofiles.open(temp_audio_path, 'wb') as f:
            content = await audio.read()
            await f.write(content)

        logger.info(f"Processing audio for user {user_id}")

        # Step 1: Speech to Text
        transcribed_text = stt_service.transcribe_audio(temp_audio_path)
        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        logger.info(f"Transcribed: {transcribed_text}")

        # Get or create conversation
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(user_id=user_id, title=transcribed_text[:50])
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=transcribed_text,
            audio_file_path=temp_audio_path
        )
        db.add(user_message)
        db.commit()

        # Step 2: Generate AI response
        # Get conversation history
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()

        conversation_history = [
            {"role": msg.role.value, "content": msg.content}
            for msg in history[:-1]  # Exclude the current message
        ]

        vader_response = ai_service.generate_response(transcribed_text, conversation_history)
        logger.info(f"Vader response: {vader_response}")

        # Step 3: Text to Speech
        # Update TTS settings from user preferences
        tts_service.update_settings(
            pitch_shift=user.vader_voice_pitch,
            speed=user.vader_voice_speed / 100.0
        )

        audio_output_path = os.path.join(settings.UPLOAD_FOLDER, f"vader_{conversation.id}_{user_message.id + 1}.wav")
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

        tts_service.synthesize(
            vader_response,
            output_path=audio_output_path,
            add_breathing=user.vader_breathing_enabled
        )

        logger.info(f"Generated audio: {audio_output_path}")

        # Save Vader's response
        vader_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=vader_response,
            audio_file_path=audio_output_path
        )
        db.add(vader_message)
        db.commit()
        db.refresh(vader_message)

        # Clean up temp file
        try:
            os.unlink(temp_audio_path)
        except:
            pass

        return {
            "transcribed_text": transcribed_text,
            "vader_response": vader_response,
            "audio_url": f"/voice/audio/{vader_message.id}",
            "conversation_id": conversation.id,
            "message_id": vader_message.id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing voice: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")


@router.post("/text", response_model=VoiceResponse)
def process_text(
    request: TextRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Process text input (for testing without audio)

    Similar to /process but takes text directly instead of audio file.
    """
    try:
        # Get user preferences
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(user_id=user_id, title=request.text[:50])
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.text
        )
        db.add(user_message)
        db.commit()

        # Generate AI response
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()

        conversation_history = [
            {"role": msg.role.value, "content": msg.content}
            for msg in history[:-1]
        ]

        vader_response = ai_service.generate_response(request.text, conversation_history)

        # Generate audio
        tts_service.update_settings(
            pitch_shift=user.vader_voice_pitch,
            speed=user.vader_voice_speed / 100.0
        )

        audio_output_path = os.path.join(settings.UPLOAD_FOLDER, f"vader_{conversation.id}_{user_message.id + 1}.wav")
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

        tts_service.synthesize(
            vader_response,
            output_path=audio_output_path,
            add_breathing=user.vader_breathing_enabled
        )

        # Save Vader's response
        vader_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=vader_response,
            audio_file_path=audio_output_path
        )
        db.add(vader_message)
        db.commit()
        db.refresh(vader_message)

        return {
            "transcribed_text": request.text,
            "vader_response": vader_response,
            "audio_url": f"/voice/audio/{vader_message.id}",
            "conversation_id": conversation.id,
            "message_id": vader_message.id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.get("/audio/{message_id}")
def get_audio(message_id: int, db: Session = Depends(get_db)):
    """
    Get audio file for a message

    Returns the Vader voice audio file for playback.
    """
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message or not message.audio_file_path:
        raise HTTPException(status_code=404, detail="Audio not found")

    if not os.path.exists(message.audio_file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        message.audio_file_path,
        media_type="audio/wav",
        filename=f"vader_response_{message_id}.wav"
    )


@router.get("/conversations")
def get_conversations(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get user's conversation history

    Returns all conversations for the authenticated user.
    """
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc()).all()

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": len(conv.messages)
        }
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get messages from a conversation

    Returns all messages from a specific conversation.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()

    return [
        {
            "id": msg.id,
            "role": msg.role.value,
            "content": msg.content,
            "audio_url": f"/voice/audio/{msg.id}" if msg.audio_file_path else None,
            "created_at": msg.created_at
        }
        for msg in messages
    ]
