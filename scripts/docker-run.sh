#!/bin/bash
# MemoryTutor Docker Runner Script
# This script helps run MemoryTutor with Docker Compose

set -e  # Exit on error

echo "=========================================="
echo "  MemoryTutor Docker Runner"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker detected"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    echo ""
    echo "Please create a .env file from the template:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env with your API keys and configuration."
    exit 1
fi

echo "✓ .env file found"
echo ""

# Check if OPENAI_API_KEY is set in .env
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "Warning: OPENAI_API_KEY not set in .env file."
    echo "Please edit .env and add your OpenAI API key."
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Parse command line arguments
MODE="${1:-up}"

case "$MODE" in
    up)
        echo "Starting MemoryTutor with Docker Compose..."
        echo ""
        docker-compose up --build
        ;;
    down)
        echo "Stopping MemoryTutor services..."
        docker-compose down
        echo "✓ Services stopped"
        ;;
    restart)
        echo "Restarting MemoryTutor services..."
        docker-compose restart
        echo "✓ Services restarted"
        ;;
    logs)
        echo "Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    status)
        echo "Service status:"
        docker-compose ps
        ;;
    clean)
        echo "Warning: This will remove all containers and volumes (including stored data)."
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            echo "✓ All services and volumes removed"
        else
            echo "Cancelled"
        fi
        ;;
    attach)
        echo "Attaching to MemoryTutor container..."
        echo "(Press Ctrl+P then Ctrl+Q to detach without stopping)"
        echo ""
        docker attach memorytutor-app
        ;;
    *)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  up       - Start services (default)"
        echo "  down     - Stop services"
        echo "  restart  - Restart services"
        echo "  logs     - View logs"
        echo "  status   - Show service status"
        echo "  attach   - Attach to interactive session"
        echo "  clean    - Remove all containers and volumes"
        echo ""
        exit 1
        ;;
esac
