#!/bin/bash
# Quick run script for MemoryTutor

# Check if .env exists
if [ ! -f .env ]; then
    echo "Configuration not found. Running setup..."
    ./scripts/interactive-setup.sh
    exit 0
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/interactive-setup.sh
    exit 0
fi

# Activate and run
source venv/bin/activate
python tutor.py
