# Vader AI - Technical Implementation Guide

**Target Audience**: Developers joining the project or contributing to the codebase

**Last Updated**: 2024-11-19

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Current Implementation Status](#current-implementation-status)
3. [Architecture Deep Dive](#architecture-deep-dive)
4. [Technology Stack](#technology-stack)
5. [Development Setup](#development-setup)
6. [Code Organization](#code-organization)
7. [Component Implementation Details](#component-implementation-details)
8. [Known Issues & Bugs](#known-issues--bugs)
9. [Common Errors & Solutions](#common-errors--solutions)
10. [Testing Strategy](#testing-strategy)
11. [Performance Considerations](#performance-considerations)
12. [Security Implementation](#security-implementation)
13. [Where to Start](#where-to-start)
14. [Development Workflow](#development-workflow)
15. [Future Technical Debt](#future-technical-debt)

---

## Project Overview

### What This Project Is

Vader AI is a **full-stack voice assistant platform** that allows users to interact with an AI speaking in Darth Vader's voice. It's built as a web application with optional ESP32 hardware integration.

**Core Functionality:**
- User speaks → Whisper transcribes → GPT generates response → TTS creates Vader voice → User hears response

### What This Project Is NOT

- ❌ Not a chatbot UI (it's voice-first)
- ❌ Not using pre-recorded Vader audio clips (it's synthesized)
- ❌ Not a simple wrapper around APIs (full custom implementation)
- ❌ Not production-deployed yet (ready but not deployed)

### Project Goals

1. **Primary**: Provide a working voice assistant with Vader personality
2. **Secondary**: Support both web and hardware (ESP32) interfaces
3. **Tertiary**: Demonstrate full-stack AI integration patterns

---

## Current Implementation Status

### ✅ Fully Implemented (100% Complete)

#### Backend
- [x] FastAPI server with CORS and middleware
- [x] User authentication (JWT-based)
- [x] User registration and login endpoints
- [x] User profile management
- [x] Speech-to-Text using OpenAI Whisper
- [x] AI response generation (GPT/DialoGPT fallback)
- [x] Text-to-Speech with Vader voice effects
- [x] Conversation storage in database
- [x] WebSocket handler for ESP32 devices
- [x] File upload handling
- [x] Database models (SQLAlchemy)
- [x] Error handling and logging
- [x] Configuration management

#### Frontend
- [x] Landing page with feature showcase
- [x] User registration page
- [x] Login page
- [x] Dashboard with voice recording
- [x] Settings page for customization
- [x] Audio playback component
- [x] Conversation history display
- [x] Authentication context/state management
- [x] Responsive design
- [x] Error handling UI

#### Hardware
- [x] ESP32 firmware (Arduino)
- [x] I2S microphone integration
- [x] I2S speaker integration
- [x] WebSocket client
- [x] Button trigger
- [x] Status LED

#### Infrastructure
- [x] Docker configuration
- [x] Docker Compose setup
- [x] Environment configuration
- [x] Deployment scripts
- [x] Testing framework

### ⚠️ Partially Implemented

- **Device Management**: Database models exist but no UI for managing multiple ESP32 devices
- **Conversation Deletion**: No UI to delete conversations
- **Audio Caching**: Directory exists but no cleanup mechanism
- **Rate Limiting**: Not implemented on API endpoints
- **Email Verification**: User registration exists but no email verification

### ❌ Not Implemented

- **Password Reset**: No forgot password flow
- **OAuth Login**: No social login (Google, GitHub, etc.)
- **File Upload Limits**: Backend has config but not enforced properly
- **Audio Format Conversion**: Only supports WAV, no MP3/OGG conversion
- **Real-time Voice Activity Detection**: Records for fixed duration
- **WebRTC Support**: Uses basic recording API
- **Metrics/Analytics**: No usage tracking
- **Admin Dashboard**: No admin interface
- **Multi-language Support**: English only
- **Wake Word Detection**: No "Hey Vader" wake word

---

## Architecture Deep Dive

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  ┌──────────────────┐           ┌──────────────────┐       │
│  │   Web Browser    │           │   ESP32 Device   │       │
│  │  (React/Vite)    │           │   (Arduino/C++)  │       │
│  └────────┬─────────┘           └────────┬─────────┘       │
└───────────┼────────────────────────────────┼────────────────┘
            │                                │
            │ HTTP/REST + WebSocket          │ WebSocket Only
            │                                │
┌───────────┼────────────────────────────────┼────────────────┐
│           │         API LAYER              │                 │
│           ▼                                ▼                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              FastAPI Application                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │ │
│  │  │   Auth   │  │   Voice  │  │   WebSocket      │   │ │
│  │  │  Router  │  │  Router  │  │    Handler       │   │ │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │ │
│  └───────┼─────────────┼──────────────────┼─────────────┘ │
│          │             │                  │                 │
└──────────┼─────────────┼──────────────────┼─────────────────┘
           │             │                  │
┌──────────┼─────────────┼──────────────────┼─────────────────┐
│          │    SERVICE LAYER               │                 │
│          ▼             ▼                  ▼                 │
│  ┌─────────────┐  ┌──────────────────────────────────┐    │
│  │   Security  │  │      AI Services Pipeline        │    │
│  │   Service   │  │  ┌──────┐  ┌──────┐  ┌──────┐  │    │
│  │  (JWT/Auth) │  │  │ STT  │→ │  AI  │→ │ TTS  │  │    │
│  └─────────────┘  │  │Service│  │Service│  │Service│  │    │
│                    │  └──────┘  └──────┘  └──────┘  │    │
│                    └──────────────────────────────────┘    │
└─────────────────────────────────┬──────────────────────────┘
                                  │
┌─────────────────────────────────┼──────────────────────────┐
│          DATA LAYER             ▼                          │
│  ┌────────────────────────────────────────────────────┐   │
│  │          SQLAlchemy ORM                             │   │
│  │  ┌──────┐  ┌──────────────┐  ┌─────────┐  ┌──────┐   │
│  │  │ User │  │Conversation  │  │ Message │  │Device│   │
│  │  │Model │  │    Model     │  │  Model  │  │Model │   │
│  │  └──────┘  └──────────────┘  └─────────┘  └──────┘   │
│  └────────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Database (SQLite/PostgreSQL)               │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### Request Flow

#### Web Voice Request Flow

1. **User Action**: Clicks microphone button in browser
2. **Recording**: Browser MediaRecorder captures audio
3. **Upload**: Audio blob sent as multipart/form-data to `/voice/process`
4. **Authentication**: JWT token validated via `get_current_user_id`
5. **Audio Save**: Temp file created with audio data
6. **STT Processing**: Whisper transcribes audio to text
7. **Database Write**: User message saved to conversation
8. **AI Processing**: GPT generates Vader-personality response
9. **TTS Processing**: gTTS + pydub creates Vader voice audio
10. **Database Write**: Assistant message saved with audio path
11. **Response**: JSON with transcription, response, audio URL
12. **Playback**: Browser fetches audio from `/voice/audio/{id}`

**Average Latency**: 3-8 seconds depending on audio length and model

#### ESP32 Voice Request Flow

1. **Connection**: ESP32 connects via WebSocket with API key
2. **Button Press**: User holds button, records audio
3. **Streaming**: Raw PCM audio streamed to backend
4. **Server Processing**: Same as web flow (STT → AI → TTS)
5. **Audio Response**: Processed audio sent back via WebSocket
6. **Playback**: ESP32 plays through I2S speaker

**Average Latency**: 2-6 seconds (slightly faster, no HTTP overhead)

### Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    vader_breathing_enabled BOOLEAN DEFAULT TRUE,
    vader_voice_pitch INTEGER DEFAULT -50,
    vader_voice_speed INTEGER DEFAULT 90,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Conversations Table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR DEFAULT 'New Conversation',
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Messages Table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    audio_file_path VARCHAR,
    created_at TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Devices Table
CREATE TABLE devices (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    device_name VARCHAR NOT NULL,
    device_id VARCHAR UNIQUE NOT NULL,
    api_key VARCHAR NOT NULL,
    is_online BOOLEAN DEFAULT FALSE,
    last_seen TIMESTAMP,
    firmware_version VARCHAR,
    ip_address VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.104.0+ | REST API and WebSocket server |
| **Server** | Uvicorn | 0.24.0+ | ASGI server |
| **Database** | SQLAlchemy | 2.0.23+ | ORM |
| **Database (Dev)** | SQLite | 3.x | File-based database |
| **Database (Prod)** | PostgreSQL | 13+ | Production database |
| **Authentication** | python-jose | 3.3.0+ | JWT token handling |
| **Password Hashing** | passlib[bcrypt] | 1.7.4+ | Secure password storage |
| **STT** | openai-whisper | Latest | Speech recognition |
| **AI** | transformers | 4.35.0+ | DialoGPT model |
| **TTS** | gtts | 2.4.0+ | Google Text-to-Speech |
| **Audio Processing** | pydub | 0.25.1+ | Audio manipulation |
| **Audio Analysis** | librosa | 0.10.1+ | Audio feature extraction |

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 18.2.0 | UI library |
| **Build Tool** | Vite | 5.0.8+ | Fast build tool |
| **Styling** | Tailwind CSS | 3.3.6+ | Utility-first CSS |
| **Routing** | React Router | 6.20.0+ | Client-side routing |
| **HTTP Client** | Axios | 1.6.2+ | API requests |
| **Icons** | React Icons | 4.12.0+ | Icon library |

### Hardware

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **MCU** | ESP32 | Main microcontroller |
| **IDE** | Arduino IDE | Firmware development |
| **Microphone** | INMP441 (I2S) | Audio input |
| **Amplifier** | MAX98357A (I2S) | Audio output |
| **WebSocket** | WebSocketsClient library | Real-time communication |
| **JSON** | ArduinoJson | Data serialization |

### Development Tools

- **Python**: 3.9+
- **Node.js**: 18+
- **Docker**: 20.10+
- **Git**: 2.x
- **pytest**: Testing
- **Black**: Code formatting
- **Flake8**: Linting

---

## Development Setup

### Prerequisites

```bash
# Check versions
python3 --version  # Should be 3.9+
node --version     # Should be 18+
npm --version      # Should be 9+
docker --version   # Optional but recommended
```

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/VaderAI.git
cd VaderAI

# 2. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Download AI models (takes 5-10 minutes)
python download_model.py

# 5. Setup environment
cp .env.example .env
# Edit .env with your settings

# 6. Install frontend dependencies
cd frontend
npm install
cd ..

# 7. Initialize database
# Database is auto-created on first run

# 8. Run both backend and frontend
./start.sh
```

### Alternative: Docker Setup

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Build and run
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

### Verify Installation

```bash
# Test backend
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}

# Test frontend
curl http://localhost:3000
# Should return HTML

# Run tests
pytest
# Should show passing tests
```

---

## Code Organization

### Backend Structure

```
backend/
├── __init__.py              # Package init
├── main.py                  # FastAPI app entry point, CORS, routers
├── api/                     # API endpoints
│   ├── __init__.py
│   ├── auth.py             # /auth/* - Registration, login, profile
│   ├── voice.py            # /voice/* - Voice processing, conversations
│   └── websocket.py        # /ws/* - WebSocket handlers
├── core/                    # Core configurations
│   ├── __init__.py
│   ├── config.py           # Settings class, environment variables
│   ├── database.py         # DB engine, session management
│   └── security.py         # JWT, password hashing, auth dependencies
├── models/                  # Database models
│   ├── __init__.py
│   ├── user.py             # User model
│   ├── conversation.py     # Conversation and Message models
│   └── device.py           # Device model
├── services/                # Business logic
│   ├── __init__.py
│   ├── speech_to_text.py   # Whisper STT service
│   ├── ai_response.py      # GPT/DialoGPT response generation
│   └── text_to_speech.py   # Vader voice TTS service
└── utils/                   # Utility functions
    ├── __init__.py         # File utilities
    └── audio_utils.py      # Audio processing helpers
```

### Frontend Structure

```
frontend/
├── index.html               # HTML entry point
├── package.json             # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
└── src/
    ├── main.jsx            # React entry point
    ├── App.jsx             # Main app component with routing
    ├── index.css           # Global styles
    ├── context/            # React context providers
    │   └── AuthContext.jsx # Authentication state management
    ├── pages/              # Page components
    │   ├── LandingPage.jsx # Home page
    │   ├── LoginPage.jsx   # Login form
    │   ├── RegisterPage.jsx # Registration form
    │   ├── Dashboard.jsx   # Voice interaction dashboard
    │   └── SettingsPage.jsx # User settings
    └── components/         # Reusable components
        ├── LoadingSpinner.jsx
        └── Modal.jsx
```

### ESP32 Structure

```
esp32/
├── vader_ai_esp32.ino      # Main Arduino sketch
└── README.md               # Hardware setup guide
```

---

## Component Implementation Details

### Backend Components

#### 1. Authentication System (`backend/api/auth.py`)

**How It Works:**
- Uses JWT (JSON Web Tokens) for stateless authentication
- Passwords hashed with bcrypt (cost factor 12)
- Token expires after 30 minutes (configurable)

**Key Functions:**
```python
register()      # POST /auth/register - Creates user, returns token
login()         # POST /auth/login - Validates credentials, returns token
get_current_user() # GET /auth/me - Returns user from token
update_profile()   # PUT /auth/me - Updates user preferences
```

**Security Notes:**
- Passwords never stored in plain text
- JWT payload contains only user ID (sub claim)
- Tokens cannot be revoked (stateless design limitation)

**Known Issues:**
- No token refresh mechanism (user must re-login after 30 min)
- No email verification
- No password strength requirements enforced

#### 2. Speech-to-Text Service (`backend/services/speech_to_text.py`)

**Implementation:**
- Uses OpenAI Whisper (base model by default)
- Loads model lazily on first use
- Supports CPU and GPU (CUDA)
- Singleton pattern for model instance

**Model Sizes:**
- `tiny`: 39M params, fast but less accurate
- `base`: 74M params (default), good balance
- `small`: 244M params, better accuracy
- `medium`: 769M params, high accuracy
- `large`: 1550M params, best accuracy (slow)

**Performance:**
- Base model: ~2-4 seconds for 5-second audio on CPU
- Base model: ~0.5-1 second for 5-second audio on GPU
- Memory usage: ~1GB for base model

**Code Pattern:**
```python
# Global singleton
_stt_service_instance = None

def get_stt_service(model_size="base"):
    global _stt_service_instance
    if _stt_service_instance is None:
        _stt_service_instance = SpeechToTextService(model_size)
    return _stt_service_instance
```

**Known Issues:**
- Model loaded into memory even if not used
- No caching of transcriptions
- No support for streaming transcription
- Limited to English (can support other languages with config)

#### 3. AI Response Service (`backend/services/ai_response.py`)

**Implementation:**
- Supports both OpenAI API and local DialoGPT
- Falls back to local model if OpenAI key not provided
- Uses system prompt to enforce Vader personality
- Maintains conversation context (last 10 messages)

**System Prompt:**
```python
"""You are Darth Vader, the Dark Lord of the Sith.
You speak with authority, power, and commanding presence...
"""
```

**OpenAI Mode:**
- Uses GPT-3.5-turbo
- Max tokens: 150
- Temperature: 0.8 (creative but controlled)
- Top-p: 0.9

**Local Model Mode:**
- Uses Microsoft DialoGPT-medium
- Less Vader-like personality (generic chatbot)
- Applies post-processing to "vaderize" responses

**Known Issues:**
- Local model doesn't maintain Vader personality well
- No conversation history pruning (could grow indefinitely in DB)
- Temperature/top-p not tuned specifically for Vader voice
- Fallback responses are generic

#### 4. Text-to-Speech Service (`backend/services/text_to_speech.py`)

**Implementation:**
- Base TTS: Google Text-to-Speech (gTTS)
- Voice effects applied with pydub
- Breathing sound generated procedurally

**Voice Transformation Pipeline:**
1. Generate base audio with gTTS
2. Slow down audio (speed = 0.9)
3. Apply low-pass filter (simulates helmet)
4. Add reverb effect
5. Prepend breathing sound
6. Export as WAV

**Breathing Sound Generation:**
```python
# Brown noise filtered to sound like breathing
noise = np.random.randn(samples)
filtered = signal.filtfilt(b, a, noise)  # Low-pass filter
envelope = signal.windows.hann(samples)  # Breathing pattern
breathing = filtered * envelope
```

**Known Issues:**
- Pitch shifting not fully implemented (complex DSP)
- Voice doesn't sound exactly like Darth Vader
- gTTS quality is good but not perfect
- No support for custom voice models
- Limited emotion/emphasis control

#### 5. WebSocket Handler (`backend/api/websocket.py`)

**Implementation:**
- FastAPI WebSocket endpoint
- Handles binary (audio) and text (JSON) messages
- Tracks connected devices in memory
- Updates device status in database

**Message Flow:**
```
ESP32 → [WebSocket] → Backend
1. Connection with device_id and api_key
2. Send status JSON (firmware version, IP)
3. Stream audio bytes
4. Receive status updates (processing, transcription, response)
5. Receive audio bytes (Vader's response)
```

**Connection Management:**
```python
connected_devices = {}  # In-memory dict

@router.websocket("/ws/esp32/{device_id}")
async def esp32_websocket(websocket, device_id, api_key):
    # Verify API key
    # Accept connection
    # Store in connected_devices
    # Process messages
    # Clean up on disconnect
```

**Known Issues:**
- Connections stored in memory (lost on restart)
- No reconnection logic on server side
- No ping/pong heartbeat (can timeout silently)
- Audio streaming not optimized (large payloads)

### Frontend Components

#### 1. Authentication Context (`frontend/src/context/AuthContext.jsx`)

**Implementation:**
- React Context API for global auth state
- Stores user object and JWT token
- Token persisted in localStorage
- Axios default headers set with token

**State:**
```javascript
{
  user: { id, email, username, ... },
  token: "eyJhbGc...",
  loading: true/false
}
```

**Methods:**
```javascript
login(email, password)     // Returns {success, error}
register(email, ...)       // Returns {success, error}
logout()                   // Clears state and localStorage
refreshUser()              // Fetches current user from API
```

**Known Issues:**
- Token not refreshed automatically (user must re-login)
- No token expiration check on client side
- Axios errors not always handled gracefully

#### 2. Dashboard Page (`frontend/src/pages/Dashboard.jsx`)

**Implementation:**
- Main voice interaction interface
- Uses MediaRecorder API for audio recording
- Handles audio upload via FormData
- Displays conversation history

**Recording Flow:**
```javascript
1. startRecording()
   - getUserMedia({audio: true})
   - Create MediaRecorder
   - Store chunks in array

2. stopRecording()
   - Stop MediaRecorder
   - Combine chunks into Blob
   - Call processAudio(blob)

3. processAudio(blob)
   - Create FormData with audio
   - POST to /voice/process
   - Update UI with response
   - Play audio response
```

**Known Issues:**
- No error handling for microphone permission denied
- Recording continues even if user navigates away
- Audio chunks not cleared properly on error
- No visual feedback during long processing times

#### 3. Settings Page (`frontend/src/pages/SettingsPage.jsx`)

**Implementation:**
- User preference management
- Range sliders for voice settings
- Toggle for breathing sounds
- Saves to backend via PUT /auth/me

**State Management:**
```javascript
const [settings, setSettings] = useState({
  full_name: '',
  vader_breathing_enabled: true,
  vader_voice_pitch: -50,
  vader_voice_speed: 90
})
```

**Known Issues:**
- No preview of voice settings
- Settings not validated before save
- No indication of unsaved changes

### ESP32 Implementation

#### Hardware Setup

**Pin Connections:**
```
INMP441 Microphone:
  SCK  → GPIO 26
  WS   → GPIO 25
  SD   → GPIO 33
  VDD  → 3.3V
  GND  → GND

MAX98357A Amplifier:
  BCLK → GPIO 14
  LRC  → GPIO 15
  DIN  → GPIO 22
  VDD  → 5V
  GND  → GND

Button:
  One side → GPIO 32
  Other side → GND

LED:
  Anode → GPIO 2
  Cathode → GND (via 220Ω resistor)
```

#### Firmware Implementation

**I2S Configuration:**
```cpp
// Microphone: 16kHz, 16-bit, mono, input
i2s_config_t i2s_mic_config = {
  .mode = I2S_MODE_MASTER | I2S_MODE_RX,
  .sample_rate = 16000,
  .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
  .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
  // ...
};

// Speaker: 44.1kHz, 16-bit, stereo, output
i2s_config_t i2s_spk_config = {
  .mode = I2S_MODE_MASTER | I2S_MODE_TX,
  .sample_rate = 44100,
  .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
  .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
  // ...
};
```

**Recording Logic:**
```cpp
void startRecording() {
  unsigned long startTime = millis();
  const unsigned long recordDuration = 3000; // 3 seconds

  while (millis() - startTime < recordDuration) {
    i2s_read(I2S_MIC_PORT, micBuffer, sizeof(micBuffer), &bytesRead, portMAX_DELAY);
    if (bytesRead > 0) {
      webSocket.sendBIN((uint8_t*)micBuffer, bytesRead);
    }
  }
}
```

**Known Issues:**
- Fixed 3-second recording (not voice-activated)
- No audio compression (sends raw PCM)
- No error handling for I2S failures
- WebSocket reconnection buggy
- No feedback if server is down

---

## Known Issues & Bugs

### Critical Issues (Should Fix Before Production)

1. **🔴 No Token Refresh Mechanism**
   - **Issue**: JWT tokens expire after 30 minutes, user must re-login
   - **Impact**: Poor user experience
   - **Fix**: Implement refresh tokens or extend expiration
   - **File**: `backend/core/security.py`

2. **🔴 Audio Files Not Cleaned Up**
   - **Issue**: Uploaded audio and generated audio accumulate in `uploads/` and `audio_cache/`
   - **Impact**: Disk space fills up over time
   - **Fix**: Add cleanup job to delete old files
   - **File**: `backend/api/voice.py`

3. **🔴 No Rate Limiting**
   - **Issue**: API endpoints can be hammered
   - **Impact**: DoS vulnerability
   - **Fix**: Add rate limiting middleware (e.g., slowapi)
   - **File**: `backend/main.py`

4. **🔴 WebSocket No Heartbeat**
   - **Issue**: Connections can silently timeout
   - **Impact**: ESP32 thinks it's connected when it's not
   - **Fix**: Implement ping/pong or periodic status checks
   - **File**: `backend/api/websocket.py`

### High Priority Issues

5. **🟡 STT Model Loaded Unnecessarily**
   - **Issue**: Whisper model loaded on import even if not used
   - **Impact**: ~1GB RAM wasted on startup
   - **Fix**: Move model loading to first request
   - **File**: `backend/services/speech_to_text.py`

6. **🟡 No Password Strength Validation**
   - **Issue**: Users can set weak passwords like "123"
   - **Impact**: Security risk
   - **Fix**: Add password validation (min length, complexity)
   - **File**: `backend/api/auth.py`

7. **🟡 Frontend Recording Not Stopped on Navigation**
   - **Issue**: If user navigates away during recording, MediaRecorder keeps running
   - **Impact**: Memory leak, microphone stays active
   - **Fix**: Add cleanup in useEffect
   - **File**: `frontend/src/pages/Dashboard.jsx`

8. **🟡 ESP32 Fixed Recording Duration**
   - **Issue**: Always records for 3 seconds regardless of speech
   - **Impact**: User must wait full 3 seconds, or cuts off mid-sentence
   - **Fix**: Implement voice activity detection
   - **File**: `esp32/vader_ai_esp32.ino`

### Medium Priority Issues

9. **🟢 Local AI Model Personality Weak**
   - **Issue**: DialoGPT doesn't maintain Vader personality
   - **Impact**: Responses don't sound like Vader without OpenAI
   - **Fix**: Fine-tune DialoGPT or use better local model
   - **File**: `backend/services/ai_response.py`

10. **🟢 TTS Voice Not Accurate**
    - **Issue**: gTTS with effects doesn't sound exactly like Vader
    - **Impact**: Breaks immersion
    - **Fix**: Use voice cloning or custom TTS model
    - **File**: `backend/services/text_to_speech.py`

11. **🟢 No Conversation Deletion**
    - **Issue**: Users can't delete conversations
    - **Impact**: Privacy concern, cluttered history
    - **Fix**: Add DELETE endpoint and UI button
    - **File**: `backend/api/voice.py`, `frontend/src/pages/Dashboard.jsx`

12. **🟢 No Device Management UI**
    - **Issue**: Users can't see/manage their ESP32 devices
    - **Impact**: Can't remove old devices or check status
    - **Fix**: Add devices page in frontend
    - **File**: New `frontend/src/pages/DevicesPage.jsx`

### Low Priority Issues

13. **⚪ No Email Verification**
    - **Issue**: Users can register with fake emails
    - **Impact**: Spam accounts possible
    - **Fix**: Send verification email on registration
    - **File**: `backend/api/auth.py`

14. **⚪ No Password Reset**
    - **Issue**: If user forgets password, account is lost
    - **Impact**: Poor UX
    - **Fix**: Add forgot password flow with email
    - **File**: New `backend/api/password_reset.py`

15. **⚪ SQLite in Production**
    - **Issue**: README says SQLite is for dev, but no migration guide
    - **Impact**: File-based DB not scalable
    - **Fix**: Document PostgreSQL migration
    - **File**: `DEPLOYMENT.md`

16. **⚪ No Admin Dashboard**
    - **Issue**: Can't monitor users, conversations, or system health
    - **Impact**: Blind to usage patterns
    - **Fix**: Add admin interface or metrics
    - **File**: New admin module

---

## Common Errors & Solutions

### Development Errors

#### Error: "ModuleNotFoundError: No module named 'backend'"

**Cause**: Python not finding backend package

**Solution**:
```bash
# Make sure you're in project root
cd /path/to/VaderAI

# Activate virtual environment
source venv/bin/activate

# Install in editable mode
pip install -e .

# Or run with proper PYTHONPATH
PYTHONPATH=. python -m uvicorn backend.main:app
```

#### Error: "RuntimeError: No models found in ~/.cache/whisper"

**Cause**: Whisper models not downloaded

**Solution**:
```bash
python download_model.py
# Or manually download
python -c "import whisper; whisper.load_model('base')"
```

#### Error: "sqlite3.OperationalError: no such table: users"

**Cause**: Database not initialized

**Solution**:
```bash
# Delete old database
rm vader_ai.db

# Restart backend (auto-creates tables)
python -m uvicorn backend.main:app --reload
```

#### Error: "Error: listen EADDRINUSE: address already in use :::3000"

**Cause**: Port already in use

**Solution**:
```bash
# Find process using port
lsof -i :3000  # or netstat -ano | findstr :3000 on Windows

# Kill process
kill -9 <PID>

# Or use different port
cd frontend
npm run dev -- --port 3001
```

#### Error: "AssertionError: Torch not compiled with CUDA enabled"

**Cause**: Trying to use GPU but PyTorch is CPU-only

**Solution**:
```bash
# Install PyTorch with CUDA support
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Or force CPU usage
# In backend/services/speech_to_text.py:
self.device = "cpu"  # Force CPU
```

### Runtime Errors

#### Error: "401 Unauthorized" on API requests

**Cause**: JWT token invalid or expired

**Solution**:
```bash
# Log out and log back in
# Or check token in browser DevTools:
# Application → Local Storage → token
```

#### Error: "Could not access microphone"

**Cause**: Browser doesn't have microphone permission

**Solution**:
```bash
# Chrome: chrome://settings/content/microphone
# Firefox: about:preferences#privacy
# Allow microphone access for localhost:3000
```

#### Error: "413 Request Entity Too Large"

**Cause**: Audio file too large for server

**Solution**:
```python
# In backend/core/config.py:
MAX_UPLOAD_SIZE_MB: int = 50  # Increase from 10

# And in nginx (if using):
client_max_body_size 50M;
```

#### Error: "ESP32 won't connect to WiFi"

**Cause**: Wrong credentials or 5GHz network

**Solution**:
```cpp
// In esp32/vader_ai_esp32.ino:
// 1. Check SSID and password
// 2. Make sure using 2.4GHz WiFi (ESP32 doesn't support 5GHz)
// 3. Check serial monitor for error messages
```

#### Error: "WebSocket connection failed"

**Cause**: Wrong server IP or API key

**Solution**:
```cpp
// In esp32/vader_ai_esp32.ino:
const char* SERVER_HOST = "192.168.1.100";  // Use your actual IP
const char* API_KEY = "...";  // Must match backend .env

// Get your IP:
// Linux/Mac: ifconfig
// Windows: ipconfig
```

### Production Errors

#### Error: "500 Internal Server Error"

**Cause**: Various backend exceptions

**Solution**:
```bash
# Check logs
docker logs vader-ai-backend
# Or
sudo journalctl -u vader-ai -n 100

# Enable debug mode temporarily
# In .env:
DEBUG=True
```

#### Error: "Connection refused" on localhost:8000

**Cause**: Backend not running

**Solution**:
```bash
# Check if running
ps aux | grep uvicorn

# Check logs
tail -f /var/log/vader-ai/error.log

# Restart service
sudo systemctl restart vader-ai
```

---

## Testing Strategy

### Current Test Coverage

**Backend:**
- ✅ Authentication endpoints (registration, login, get user)
- ✅ Voice text endpoint
- ✅ Conversation retrieval
- ❌ WebSocket communication (not tested)
- ❌ STT/AI/TTS services (not unit tested)
- ❌ Database models (not tested)

**Frontend:**
- ❌ No tests yet

**ESP32:**
- ❌ No automated tests

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register_user

# View coverage report
open htmlcov/index.html
```

### Adding New Tests

**Example: Testing a new endpoint**

```python
# tests/test_new_feature.py
def test_new_endpoint(client, test_user_data):
    """Test new feature endpoint"""
    # Register user
    register_response = client.post("/auth/register", json=test_user_data)
    token = register_response.json()["access_token"]

    # Test endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/new-endpoint", json={...}, headers=headers)

    assert response.status_code == 200
    assert "expected_field" in response.json()
```

### Test Database

Tests use a separate SQLite database (`test_vader_ai.db`) that's created and destroyed for each test. Never run tests against production database.

---

## Performance Considerations

### Current Performance

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| User registration | 100-200ms | Password hashing (bcrypt) |
| User login | 100-200ms | Password verification |
| STT (5s audio) | 2-4s CPU, 0.5-1s GPU | Whisper model |
| AI response | 1-3s | GPT API or DialoGPT |
| TTS | 1-2s | gTTS + audio processing |
| Full pipeline | 5-10s | Sum of above |

### Optimization Opportunities

1. **Cache AI Responses**
   - Common questions could be cached (e.g., "what is the Force?")
   - Redis or in-memory cache
   - Could reduce AI response time to <100ms for cache hits

2. **Async Audio Processing**
   - Currently processes sequentially
   - Could run STT and save to DB in parallel
   - Celery or background tasks

3. **Model Optimization**
   - Use smaller Whisper model (tiny instead of base)
   - Quantize models (INT8 instead of FP32)
   - Use ONNX Runtime for faster inference

4. **Database Indexing**
   - Add index on `conversations.user_id`
   - Add index on `messages.conversation_id`
   - Add index on `users.email` (already unique, but explicit index)

5. **Connection Pooling**
   - SQLAlchemy pool size currently default
   - Increase for production with many concurrent users

### Load Testing

Not yet performed. Recommended tools:
- **Locust**: HTTP load testing
- **wrk**: HTTP benchmarking
- **k6**: Modern load testing

---

## Security Implementation

### Current Security Measures

1. **Authentication**: JWT with 30-min expiration
2. **Password Storage**: bcrypt with cost factor 12
3. **CORS**: Configured for localhost (must update for production)
4. **SQL Injection**: Prevented by SQLAlchemy ORM
5. **XSS**: React escapes by default
6. **CSRF**: Not needed (no cookies, using JWT)

### Security Gaps

1. **No HTTPS**: Running on HTTP (must add HTTPS in production)
2. **No Rate Limiting**: API can be spammed
3. **No Input Validation**: Only basic validation on required fields
4. **API Keys in URL**: ESP32 sends API key in query string (visible in logs)
5. **No File Type Validation**: Could upload non-audio files
6. **No Account Lockout**: No protection against brute force login attempts

### Recommended Additions

```python
# 1. Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/auth/login")
@limiter.limit("5/minute")
def login(...):
    ...

# 2. Input validation
from pydantic import validator, Field

class UserRegister(BaseModel):
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

# 3. File validation
def validate_audio_file(file: UploadFile):
    if not file.content_type.startswith('audio/'):
        raise HTTPException(400, "Only audio files allowed")
    if file.size > MAX_SIZE:
        raise HTTPException(413, "File too large")
```

---

## Where to Start

### For New Backend Developers

**Start Here:**
1. Read `backend/main.py` - Understand app structure
2. Read `backend/core/` - Understand configuration and database
3. Read `backend/api/auth.py` - Understand authentication flow
4. Read `backend/api/voice.py` - Understand main feature
5. Trace a request: Register → Login → Voice command

**First Task Ideas:**
- Add password strength validation
- Add endpoint to delete conversation
- Add rate limiting
- Improve error messages

### For New Frontend Developers

**Start Here:**
1. Read `frontend/src/App.jsx` - Understand routing
2. Read `frontend/src/context/AuthContext.jsx` - Understand auth state
3. Read `frontend/src/pages/Dashboard.jsx` - Main feature UI
4. Trace user flow: Landing → Register → Dashboard

**First Task Ideas:**
- Add loading spinners during API calls
- Improve error messages
- Add conversation deletion button
- Add voice settings preview

### For Hardware Developers

**Start Here:**
1. Read `esp32/vader_ai_esp32.ino` - Understand firmware
2. Read `esp32/README.md` - Understand hardware setup
3. Assemble hardware on breadboard
4. Test with serial monitor

**First Task Ideas:**
- Add voice activity detection (stop recording on silence)
- Add WiFi reconnection logic
- Add visual feedback (LED patterns)
- Optimize audio streaming

---

## Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Activate environment
source venv/bin/activate

# 3. Start development servers
./start.sh
# Or separately:
# Terminal 1: python -m uvicorn backend.main:app --reload
# Terminal 2: cd frontend && npm run dev

# 4. Make changes

# 5. Test changes
pytest  # Backend
# (No frontend tests yet)

# 6. Commit
git add .
git commit -m "Description of changes"
git push origin feature-branch
```

### Adding a New Feature

**Example: Add conversation deletion**

1. **Backend**:
   ```python
   # backend/api/voice.py
   @router.delete("/conversations/{conversation_id}")
   def delete_conversation(
       conversation_id: int,
       user_id: int = Depends(get_current_user_id),
       db: Session = Depends(get_db)
   ):
       conversation = db.query(Conversation).filter(
           Conversation.id == conversation_id,
           Conversation.user_id == user_id
       ).first()

       if not conversation:
           raise HTTPException(404, "Conversation not found")

       db.delete(conversation)
       db.commit()

       return {"message": "Conversation deleted"}
   ```

2. **Frontend**:
   ```jsx
   // frontend/src/pages/Dashboard.jsx
   const deleteConversation = async (convId) => {
     if (!confirm('Delete this conversation?')) return

     try {
       await axios.delete(`/api/voice/conversations/${convId}`)
       loadConversations() // Refresh list
     } catch (error) {
       alert('Error deleting conversation')
     }
   }

   // In render:
   <button onClick={() => deleteConversation(conv.id)}>
     Delete
   </button>
   ```

3. **Test**:
   ```python
   # tests/test_voice.py
   def test_delete_conversation(client, test_user_data):
       # Register
       register_response = client.post("/auth/register", json=test_user_data)
       token = register_response.json()["access_token"]
       headers = {"Authorization": f"Bearer {token}"}

       # Create conversation
       response = client.post(
           "/voice/text",
           json={"text": "Test"},
           headers=headers
       )
       conv_id = response.json()["conversation_id"]

       # Delete
       response = client.delete(
           f"/voice/conversations/{conv_id}",
           headers=headers
       )
       assert response.status_code == 200

       # Verify deleted
       response = client.get("/voice/conversations", headers=headers)
       assert conv_id not in [c["id"] for c in response.json()]
   ```

4. **Document**:
   - Update README if user-facing
   - Update IMPLEMENTATION.md (this file) with technical details
   - Update API docs (auto-generated by FastAPI)

---

## Future Technical Debt

### Things That Should Be Refactored

1. **Global Service Singletons**
   - Currently using global variables for services
   - Should use dependency injection
   - Affects: All service files

2. **Error Handling**
   - Inconsistent error responses
   - Should standardize error format
   - Create custom exception classes

3. **Logging**
   - Basic logging setup
   - Should add structured logging
   - Add request ID tracking

4. **Configuration**
   - All settings in one class
   - Should split into dev/staging/prod configs
   - Use config files instead of env vars for complex settings

5. **Database Migrations**
   - Using create_all() which doesn't support migrations
   - Should use Alembic properly
   - Create migration scripts

6. **Frontend State Management**
   - Using Context API
   - Should consider Redux/Zustand for complex state
   - Especially for conversation history

7. **Audio File Storage**
   - Storing in local filesystem
   - Should use S3 or similar for production
   - Implement cleanup policy

8. **WebSocket Scaling**
   - In-memory connection tracking
   - Won't work with multiple instances
   - Should use Redis for connection state

---

## Debugging Tips

### Enable Debug Mode

```python
# backend/core/config.py
DEBUG: bool = True

# Or in .env
DEBUG=True
```

This enables:
- Detailed error messages
- SQL query logging
- Auto-reload on code changes

### Useful Logging

```python
import logging
logger = logging.getLogger(__name__)

# In your code
logger.debug("Debug info")
logger.info("Normal info")
logger.warning("Warning")
logger.error("Error occurred", exc_info=True)  # Includes traceback
```

### Database Inspection

```bash
# Open SQLite database
sqlite3 vader_ai.db

# Useful queries
.tables  # List tables
.schema users  # Show table schema
SELECT * FROM users;
SELECT * FROM conversations WHERE user_id = 1;
SELECT * FROM messages WHERE conversation_id = 1;

# Or use a GUI tool:
# - DB Browser for SQLite (https://sqlitebrowser.org/)
# - DBeaver (https://dbeaver.io/)
```

### API Testing

```bash
# Test with curl
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123"}'

# Or use Postman/Insomnia
# Or use FastAPI's built-in docs: http://localhost:8000/docs
```

### Frontend Debugging

```javascript
// Add to Dashboard.jsx
console.log('Current user:', user)
console.log('Transcription:', transcription)
console.log('Response:', vaderResponse)

// Use React DevTools browser extension
// Use Network tab to see API requests
```

---

## Questions?

If you're stuck or have questions:

1. Check error logs (backend console or browser console)
2. Search this document (Ctrl+F)
3. Check GitHub Issues
4. Check FastAPI docs: https://fastapi.tiangolo.com
5. Check React docs: https://react.dev
6. Ask in project discussions

---

**Good luck, and may the Force be with you!**

*Last updated: 2024-11-19 by Claude*
