#!/bin/bash
# MemoryTutor Setup Script
# This script helps set up the MemoryTutor environment

set -e  # Exit on error

echo "=========================================="
echo "  MemoryTutor Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.11 or higher."
    exit 1
fi

python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.11"

# Version comparison
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher required."
    echo "Found: Python $python_version"
    echo "Please upgrade Python."
    exit 1
fi

echo "✓ Python $python_version detected"
echo ""

# Create .env from example
echo "Setting up environment file..."
if [ -f .env ]; then
    echo "⚠ .env file already exists."
    read -p "Do you want to overwrite it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✓ .env file created from .env.example"
    else
        echo "Keeping existing .env file"
    fi
else
    cp .env.example .env
    echo "✓ .env file created from .env.example"
fi
echo ""

# Create virtual environment
echo "Setting up virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists."
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    else
        echo "Using existing virtual environment"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - Add your OpenAI API key (required)"
echo "   - Add Mem0 API key if using hosted mode (optional)"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the tutor:"
echo "   python tutor.py"
echo ""
echo "For more information, see README.md"
echo ""
