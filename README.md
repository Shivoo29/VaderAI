# Darth Vader AI Voice Assistant

"**You don't know the power of the Dark Side...**"

A complete, production-ready AI voice assistant platform that speaks with the commanding voice of Darth Vader. This project includes a web application for browser-based interaction and ESP32 firmware for hardware voice control.

## **Features**

### **Core Capabilities**

1. **Vader's Iconic Voice**:
   - Deep, commanding voice synthesis with breathing effects
   - Customizable pitch and speed settings
   - Authentic Sith Lord personality in all responses

2. **Advanced Voice Recognition**:
   - OpenAI Whisper for high-accuracy speech-to-text
   - Real-time audio processing
   - Supports multiple languages

3. **AI Intelligence**:
   - Context-aware conversations using GPT or local LLM
   - Conversation history tracking
   - Star Wars-themed responses with personality

4. **Multi-Platform Support**:
   - **Web Application**: Browser-based voice interaction
   - **ESP32 Hardware**: Physical voice assistant device
   - **WebSocket API**: Real-time bidirectional communication

5. **User Management**:
   - Secure authentication with JWT tokens
   - User profiles and preferences
   - Conversation history

### **Platform Architecture**

- **Backend**: FastAPI (Python) with SQLAlchemy
- **Frontend**: React with Tailwind CSS
- **AI Services**: Whisper (STT), GPT/DialoGPT (AI), gTTS (TTS)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Hardware**: ESP32 with I2S microphone and speaker

---

## **Quick Start**

### **Option 1: Automated Setup (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/VaderAI.git
cd VaderAI

# Run the start script
chmod +x start.sh
./start.sh
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### **Option 2: Docker**

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Start with Docker Compose
docker-compose up -d
```

### **Option 3: Manual Installation**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed manual installation instructions.

---

## **System Requirements**

### **Minimum Requirements**

- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.9 or higher
- **Node.js**: 18 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 5GB free space (for AI models)
- **FFmpeg**: Required for audio processing

### **Optional**

- **GPU**: NVIDIA GPU with CUDA for faster AI processing
- **OpenAI API Key**: For enhanced AI responses (optional)
- **PostgreSQL**: For production deployment
- **Redis**: For caching and job queuing

---

## **Installation**

### **1. Backend Setup**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download AI models (first time only)
python download_model.py

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run backend
python -m uvicorn backend.main:app --reload
```

### **2. Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### **3. ESP32 Setup (Optional)**

See [esp32/README.md](esp32/README.md) for hardware assembly and firmware installation.

---

## **Usage**

### **Web Application**

1. **Register an Account**:
   - Visit http://localhost:3000
   - Click "Join the Empire"
   - Create your account

2. **Start Interacting**:
   - Click the microphone button on the dashboard
   - Speak your command
   - Wait for Vader's response (audio + text)

3. **Customize Settings**:
   - Adjust voice pitch and speed
   - Enable/disable breathing sounds
   - View conversation history

### **ESP32 Hardware**

1. Power on your ESP32 device
2. Press and hold the button
3. Speak your command: "Vader, what time is it?"
4. Release the button
5. Vader responds through the speaker

### **Example Commands**

- "Vader, tell me the weather"
- "Vader, what is the Force?"
- "Vader, tell me a joke"
- "Vader, who shot first?"
- "Vader, recite the Sith Code"

**Example Response**:
User: "Vader, who shot first?"
Vader: "Han shot first... but the Empire always shoots last. Do not question the ways of the Dark Side."

---

## **Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  Web Frontend    │         │   ESP32 Device   │     │
│  │  (React + Vite)  │         │  (Arduino/C++)   │     │
│  └────────┬─────────┘         └────────┬─────────┘     │
└───────────┼──────────────────────────────┼──────────────┘
            │                              │
            │ HTTP/REST                    │ WebSocket
            │                              │
┌───────────┼──────────────────────────────┼──────────────┐
│           ▼                              ▼               │
│  ┌────────────────────────────────────────────────┐    │
│  │         FastAPI Backend (Python)               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │    │
│  │  │   Auth   │  │   Voice  │  │ WebSocket│    │    │
│  │  │   API    │  │   API    │  │ Handler  │    │    │
│  │  └──────────┘  └──────────┘  └──────────┘    │    │
│  └─────────────────────┬──────────────────────────┘    │
│                        │                                │
│  ┌─────────────────────┼──────────────────────────┐    │
│  │         AI Services Pipeline                    │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │    │
│  │  │ Whisper │→ │   GPT   │→ │  Vader TTS  │    │    │
│  │  │  (STT)  │  │  (AI)   │  │   (Audio)   │    │    │
│  │  └─────────┘  └─────────┘  └─────────────┘    │    │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│  ┌─────────────────────┴──────────────────────────┐    │
│  │         SQLAlchemy Database (SQLite/PG)        │    │
│  │   Users | Conversations | Messages | Devices   │    │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### **Processing Flow**

1. **Audio Input** → User speaks (web mic or ESP32)
2. **Speech-to-Text** → Whisper transcribes audio
3. **AI Processing** → GPT generates contextual response
4. **Text-to-Speech** → Generate Vader voice audio
5. **Audio Output** → Play response to user
6. **Storage** → Save conversation to database

---

## **Project Structure**

```
VaderAI/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── voice.py        # Voice processing endpoints
│   │   └── websocket.py    # WebSocket handler
│   ├── core/               # Core configurations
│   │   ├── config.py       # App settings
│   │   ├── database.py     # Database setup
│   │   └── security.py     # Auth & security
│   ├── models/             # Database models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── device.py
│   ├── services/           # AI services
│   │   ├── speech_to_text.py
│   │   ├── ai_response.py
│   │   └── text_to_speech.py
│   └── main.py             # FastAPI app entry
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── SettingsPage.jsx
│   │   ├── context/       # React context
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── esp32/                  # ESP32 firmware
│   ├── vader_ai_esp32.ino
│   └── README.md
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── download_model.py      # Model downloader
├── .env.example           # Environment template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker composition
├── start.sh               # Quick start script
├── DEPLOYMENT.md          # Deployment guide
└── README.md              # This file
```

---

## **Configuration**

### **Environment Variables**

Copy `.env.example` to `.env` and configure:

```bash
# Application
APP_NAME="Vader AI Voice Assistant"
ENVIRONMENT=development
DEBUG=True

# Security (CHANGE THESE!)
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this

# Database
DATABASE_URL=sqlite:///./vader_ai.db

# OpenAI (Optional - for better AI)
OPENAI_API_KEY=your-openai-api-key

# Vader Voice Settings
VADER_VOICE_PITCH=-50
VADER_VOICE_SPEED=0.9
VADER_BREATHING_ENABLED=True

# ESP32
ESP32_API_KEY=change-this-esp32-api-key
```

---

## **Development**

### **Backend Development**

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python -m uvicorn backend.main:app --reload

# Run tests (coming soon)
pytest

# Format code
black backend/
```

### **Frontend Development**

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## **API Documentation**

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **Key Endpoints**

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `POST /voice/process` - Process voice command (audio file)
- `POST /voice/text` - Process text command
- `GET /voice/audio/{message_id}` - Get audio response
- `WS /ws/esp32/{device_id}` - ESP32 WebSocket connection

---

## **Deployment**

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:
- Local development setup
- Production deployment (Nginx + Gunicorn)
- Docker deployment
- Cloud deployment (AWS, Heroku, DigitalOcean)
- ESP32 hardware setup

---

## **Troubleshooting**

### **Common Issues**

1. **"Module not found" errors**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Audio processing fails**:
   ```bash
   # Install FFmpeg
   sudo apt install ffmpeg  # Ubuntu/Debian
   brew install ffmpeg      # macOS
   ```

3. **Frontend build errors**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Database errors**:
   ```bash
   rm vader_ai.db
   # Restart backend to recreate
   ```

---

## **Contributing**

We welcome contributions! Whether it's:
- Adding new voice personalities (Yoda, C-3PO, etc.)
- Improving AI responses
- Hardware integrations
- Bug fixes and optimizations

Please fork the repo and submit pull requests.

---

## **Roadmap**

- [ ] Multi-language support
- [ ] Custom wake word detection
- [ ] Smart home integrations (Home Assistant, etc.)
- [ ] Mobile app (iOS/Android)
- [ ] Voice cloning for custom voices
- [ ] Multi-user conversations
- [ ] Cloud sync for conversations

---

## **License**

MIT License - See LICENSE file for details

---

## **Acknowledgments**

- **OpenAI** for Whisper speech recognition
- **Hugging Face** for transformer models
- **FastAPI** for the excellent web framework
- **React** for the frontend framework
- **The Empire** for inspiring our pursuit of power
- **Darth Vader** for showing us what real leadership sounds like

---

## **Disclaimer**

This project is for educational and entertainment purposes. Star Wars, Darth Vader, and related characters are trademarks of Lucasfilm Ltd. This is a fan project and is not affiliated with or endorsed by Lucasfilm or Disney.

---

> **"The Force will be with you... always."**
> Or maybe not. After all, this assistant serves the Dark Side.

**May the Force be with you!**

For questions and support, open an issue on GitHub.  
