"""WebSocket handler for ESP32 devices"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional
import logging
import json
from datetime import datetime

from backend.core import get_db, verify_esp32_api_key
from backend.models import Device
from backend.services import SpeechToTextService, AIResponseService, VaderTTSService

logger = logging.getLogger(__name__)

router = APIRouter()

# Connected ESP32 devices
connected_devices: Dict[str, WebSocket] = {}

# Initialize services
stt_service = SpeechToTextService()
ai_service = AIResponseService()
tts_service = VaderTTSService()


@router.websocket("/ws/esp32/{device_id}")
async def esp32_websocket(
    websocket: WebSocket,
    device_id: str,
    api_key: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for ESP32 devices

    Handles real-time communication with ESP32 microcontrollers:
    1. Receives audio from ESP32
    2. Processes through STT -> AI -> TTS pipeline
    3. Sends audio response back to ESP32
    """
    # Verify API key
    if not verify_esp32_api_key(api_key):
        await websocket.close(code=1008, reason="Invalid API key")
        return

    # Accept connection
    await websocket.accept()
    logger.info(f"ESP32 device {device_id} connected")

    # Update device status in database
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if device:
        device.is_online = True
        device.last_seen = datetime.utcnow()
        db.commit()

    # Store connection
    connected_devices[device_id] = websocket

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Vader AI",
            "device_id": device_id
        })

        while True:
            # Receive data from ESP32
            data = await websocket.receive()

            if "bytes" in data:
                # Audio data received
                audio_data = data["bytes"]
                await handle_audio_data(websocket, device_id, audio_data, db)

            elif "text" in data:
                # JSON command received
                message = json.loads(data["text"])
                await handle_json_message(websocket, device_id, message, db)

    except WebSocketDisconnect:
        logger.info(f"ESP32 device {device_id} disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}", exc_info=True)
    finally:
        # Clean up
        if device_id in connected_devices:
            del connected_devices[device_id]

        # Update device status
        if device:
            device.is_online = False
            device.last_seen = datetime.utcnow()
            db.commit()


async def handle_audio_data(
    websocket: WebSocket,
    device_id: str,
    audio_data: bytes,
    db: Session
):
    """
    Handle audio data from ESP32

    Args:
        websocket: WebSocket connection
        device_id: ESP32 device identifier
        audio_data: Raw audio bytes
        db: Database session
    """
    try:
        logger.info(f"Received {len(audio_data)} bytes of audio from {device_id}")

        # Send processing status
        await websocket.send_json({
            "type": "status",
            "message": "Processing your command..."
        })

        # Save audio to temp file for processing
        import tempfile
        import wave
        import numpy as np

        temp_path = tempfile.mktemp(suffix='.wav')

        # Assume audio is 16-bit PCM at 16kHz
        with wave.open(temp_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(16000)
            wav_file.writeframes(audio_data)

        # Speech to Text
        transcribed_text = stt_service.transcribe_audio(temp_path)

        if not transcribed_text:
            await websocket.send_json({
                "type": "error",
                "message": "Could not understand audio"
            })
            return

        logger.info(f"Transcribed: {transcribed_text}")

        await websocket.send_json({
            "type": "transcription",
            "text": transcribed_text
        })

        # Generate AI response
        vader_response = ai_service.generate_response(transcribed_text)
        logger.info(f"Vader response: {vader_response}")

        await websocket.send_json({
            "type": "response",
            "text": vader_response
        })

        # Generate TTS audio
        audio_output_path = tts_service.synthesize(vader_response, add_breathing=True)

        # Read audio file and send back
        with open(audio_output_path, 'rb') as f:
            audio_response = f.read()

        await websocket.send_bytes(audio_response)

        await websocket.send_json({
            "type": "complete",
            "message": "Processing complete"
        })

        # Clean up temp files
        import os
        try:
            os.unlink(temp_path)
            os.unlink(audio_output_path)
        except:
            pass

    except Exception as e:
        logger.error(f"Error processing audio: {e}", exc_info=True)
        await websocket.send_json({
            "type": "error",
            "message": "Error processing audio"
        })


async def handle_json_message(
    websocket: WebSocket,
    device_id: str,
    message: dict,
    db: Session
):
    """
    Handle JSON messages from ESP32

    Args:
        websocket: WebSocket connection
        device_id: ESP32 device identifier
        message: JSON message
        db: Database session
    """
    try:
        msg_type = message.get("type")

        if msg_type == "ping":
            # Heartbeat
            await websocket.send_json({"type": "pong"})

        elif msg_type == "status":
            # Device status update
            device = db.query(Device).filter(Device.device_id == device_id).first()
            if device:
                device.firmware_version = message.get("firmware_version")
                device.ip_address = message.get("ip_address")
                device.last_seen = datetime.utcnow()
                db.commit()

            await websocket.send_json({
                "type": "status_ack",
                "message": "Status updated"
            })

        elif msg_type == "text":
            # Text-based command (for testing)
            text = message.get("text")
            if text:
                vader_response = ai_service.generate_response(text)
                await websocket.send_json({
                    "type": "response",
                    "text": vader_response
                })

        else:
            logger.warning(f"Unknown message type: {msg_type}")

    except Exception as e:
        logger.error(f"Error handling JSON message: {e}", exc_info=True)


@router.get("/ws/devices")
def get_connected_devices():
    """
    Get list of currently connected ESP32 devices

    Returns device IDs of all connected ESP32 devices.
    """
    return {
        "connected_devices": list(connected_devices.keys()),
        "count": len(connected_devices)
    }
