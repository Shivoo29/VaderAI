# Vader AI Deployment Guide

This guide covers different deployment options for Vader AI Voice Assistant.

## Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [ESP32 Setup](#esp32-setup)

---

## Local Development

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- FFmpeg (for audio processing)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/VaderAI.git
   cd VaderAI
   ```

2. **Run the start script**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

If you prefer manual setup:

#### Backend

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download AI models
python download_model.py

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run backend
python -m uvicorn backend.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## Production Deployment

### Backend (FastAPI)

1. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with production settings:
   # - Set ENVIRONMENT=production
   # - Set DEBUG=False
   # - Configure DATABASE_URL for PostgreSQL
   # - Set strong SECRET_KEY and JWT_SECRET_KEY
   # - Add OPENAI_API_KEY if using OpenAI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python download_model.py
   ```

3. **Run with Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

### Frontend (React)

1. **Build for production**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Serve with Nginx**:

   Create `/etc/nginx/sites-available/vader-ai`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # Frontend
       location / {
           root /path/to/VaderAI/frontend/dist;
           try_files $uri $uri/ /index.html;
       }

       # Backend API
       location /api/ {
           proxy_pass http://127.0.0.1:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # WebSocket
       location /ws/ {
           proxy_pass http://127.0.0.1:8000/ws/;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   Enable and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/vader-ai /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Systemd Service

Create `/etc/systemd/system/vader-ai.service`:

```ini
[Unit]
Description=Vader AI Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/VaderAI
Environment="PATH=/path/to/VaderAI/venv/bin"
ExecStart=/path/to/VaderAI/venv/bin/gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vader-ai
sudo systemctl start vader-ai
```

---

## Docker Deployment

### Using Docker Compose

1. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Build and run**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

4. **View logs**:
   ```bash
   docker-compose logs -f
   ```

5. **Stop services**:
   ```bash
   docker-compose down
   ```

### Manual Docker Build

```bash
# Build backend
docker build -t vader-ai-backend .

# Run backend
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/vader_ai.db:/app/vader_ai.db \
  --name vader-ai-backend \
  vader-ai-backend
```

---

## Cloud Deployment

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04, t3.medium or larger)

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv nodejs npm nginx ffmpeg
   ```

4. **Clone and deploy** (follow Production Deployment steps above)

5. **Configure security group**:
   - Allow inbound: Port 80 (HTTP), 443 (HTTPS), 8000 (API)

### Heroku

1. **Create Procfile**:
   ```
   web: gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Deploy**:
   ```bash
   heroku create vader-ai
   git push heroku main
   ```

### DigitalOcean

1. **Create Droplet** (Ubuntu 22.04)
2. Follow Production Deployment steps
3. Configure firewall and domain

---

## ESP32 Setup

### Hardware Assembly

See [esp32/README.md](esp32/README.md) for detailed hardware setup.

### Firmware Configuration

1. **Open `esp32/vader_ai_esp32.ino` in Arduino IDE**

2. **Configure WiFi**:
   ```cpp
   const char* WIFI_SSID = "Your_WiFi_Name";
   const char* WIFI_PASSWORD = "Your_WiFi_Password";
   ```

3. **Configure Server**:
   ```cpp
   const char* SERVER_HOST = "192.168.1.100";  // Your server IP
   const int SERVER_PORT = 8000;
   const char* API_KEY = "change-this-esp32-api-key";  // Match backend
   ```

4. **Upload to ESP32**

### Testing ESP32 Connection

1. **Check backend .env**:
   ```
   ESP32_API_KEY=change-this-esp32-api-key
   ```

2. **Monitor Serial output** (115200 baud)

3. **Test voice command**:
   - Press button on ESP32
   - Speak command
   - Release button
   - Wait for Vader's response

---

## Troubleshooting

### Backend Issues

**Import errors**:
```bash
pip install --upgrade -r requirements.txt
```

**Database errors**:
```bash
rm vader_ai.db
python -c "from backend.core import init_db; init_db()"
```

**Audio processing errors**:
```bash
sudo apt install ffmpeg portaudio19-dev
```

### Frontend Issues

**Build errors**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

**API connection errors**:
- Check CORS settings in backend/.env
- Verify proxy configuration in vite.config.js

### ESP32 Issues

**WiFi connection fails**:
- Check SSID and password
- Use 2.4GHz network only
- Move closer to router

**WebSocket fails**:
- Verify server IP and port
- Check API key matches
- Ensure backend is running

---

## Security Considerations

1. **Change default secrets**:
   - SECRET_KEY
   - JWT_SECRET_KEY
   - ESP32_API_KEY

2. **Use HTTPS** in production:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

3. **Configure firewall**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

4. **Regular updates**:
   ```bash
   pip install --upgrade -r requirements.txt
   cd frontend && npm update
   ```

---

## Performance Optimization

1. **Use GPU for AI processing** (if available):
   - Install CUDA and cuDNN
   - Install PyTorch with CUDA support

2. **Use PostgreSQL** instead of SQLite for production

3. **Enable caching** with Redis:
   ```bash
   sudo apt install redis-server
   # Update REDIS_URL in .env
   ```

4. **Configure Nginx caching** for static files

---

## Monitoring

### Logs

**Backend**:
```bash
# Systemd
sudo journalctl -u vader-ai -f

# Docker
docker logs -f vader-ai-backend
```

**Frontend**:
```bash
# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

---

## Backup

### Database

```bash
# SQLite
cp vader_ai.db vader_ai.db.backup

# PostgreSQL
pg_dump vader_ai > vader_ai_backup.sql
```

### User Data

```bash
tar -czf vader_ai_backup_$(date +%Y%m%d).tar.gz \
  vader_ai.db uploads/ audio_cache/ .env
```

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/VaderAI/issues
- Documentation: See README.md

---

**May the Force be with you!**
