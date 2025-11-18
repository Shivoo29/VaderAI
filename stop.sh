#!/bin/bash

# Vader AI - Stop Script

echo "Stopping Vader AI services..."

# Kill backend
pkill -f "uvicorn backend.main:app"

# Kill frontend
pkill -f "vite"

echo "Vader AI services stopped."
