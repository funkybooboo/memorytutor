#!/bin/bash
# Quick run script for MemoryTutor
# Defaults to Docker for the best experience

set -e

# Parse command line arguments
USE_LOCAL=false
if [ "$1" == "--local" ]; then
    USE_LOCAL=true
    shift
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Configuration file not found!"
    echo ""
    echo "Please create .env file:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Try Docker first (recommended)
if [ "$USE_LOCAL" = false ] && command -v docker &> /dev/null && (command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1); then
    echo "🐳 Starting MemoryTutor with Docker..."
    echo ""

    # Determine docker compose command
    if docker compose version &> /dev/null 2>&1; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi

    # Start Qdrant first in background
    echo "Starting Qdrant database..."
    $DOCKER_COMPOSE up -d qdrant

    # Wait for Qdrant to be healthy
    echo "Waiting for database to be ready..."
    sleep 3

    echo "✓ Database ready!"
    echo ""

    # Run the tutor in foreground (properly connected to terminal)
    $DOCKER_COMPOSE run --rm memorytutor

    # After exiting, ask if user wants to stop Qdrant
    echo ""
    read -p "Stop Qdrant database? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping database..."
        $DOCKER_COMPOSE down
        echo "✓ Database stopped"
    else
        echo "Database still running. Use 'docker compose down' to stop later."
    fi
else
    # Fall back to local Python
    if [ "$USE_LOCAL" = true ]; then
        echo "🐍 Running MemoryTutor locally (as requested)..."
    else
        echo "🐍 Docker not available, running MemoryTutor locally..."
        echo "💡 Tip: Install Docker for the best experience!"
    fi
    echo ""

    # Check if venv exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        echo "Installing dependencies..."
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi

    # Run the tutor
    python tutor.py
fi
