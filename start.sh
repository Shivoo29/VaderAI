#!/bin/bash

# Vader AI - Start Script
# This script starts the Vader AI platform

set -e

echo "========================================="
echo "  Vader AI - Voice Assistant Platform"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download models if needed
if [ ! -d "$HOME/.cache/whisper" ]; then
    echo "Downloading AI models (this may take a while)..."
    python download_model.py
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env file with your configuration"
    echo "Press Enter to continue..."
    read
fi

# Create necessary directories
mkdir -p uploads audio_cache

# Start backend
echo ""
echo "Starting Vader AI backend..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start frontend
echo "Starting frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================="
echo "  Vader AI is running!"
echo "========================================="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

wait
