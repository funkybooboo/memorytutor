#!/bin/bash
# MemoryTutor Configuration Validator
# Checks if your setup is ready to run

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "=============================================="
echo "  🔍 MemoryTutor Configuration Validator"
echo "=============================================="
echo ""

ERRORS=0
WARNINGS=0

# Check Python
echo -n "Checking Python... "
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Not found${NC}"
    echo "   Install from: https://www.python.org/downloads/"
    ERRORS=$((ERRORS + 1))
else
    python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
    required_version="3.11"
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        echo -e "${RED}✗ Version $python_version (need 3.11+)${NC}"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}✓ Python $python_version${NC}"
    fi
fi

# Check virtual environment
echo -n "Checking virtual environment... "
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Not found${NC}"
    echo "   Run: python3 -m venv venv"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✓ Found${NC}"
fi

# Check dependencies
echo -n "Checking dependencies... "
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Skipped (no venv)${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    source venv/bin/activate
    if python -c "import openai, mem0, dotenv" 2>/dev/null; then
        echo -e "${GREEN}✓ Installed${NC}"
    else
        echo -e "${RED}✗ Missing packages${NC}"
        echo "   Run: pip install -r requirements.txt"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Check .env file
echo -n "Checking .env file... "
if [ ! -f .env ]; then
    echo -e "${RED}✗ Not found${NC}"
    echo "   Run: cp .env.example .env"
    echo "   Or run: ./scripts/interactive-setup.sh"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ Found${NC}"

    # Load .env
    source .env 2>/dev/null

    # Check OpenAI API key
    echo -n "Checking OpenAI API key... "
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" == "sk-your-openai-api-key-here" ]; then
        echo -e "${RED}✗ Not set${NC}"
        echo "   Get your key from: https://platform.openai.com/api-keys"
        echo "   Add it to .env file"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}✓ Set${NC}"
    fi

    # Check memory mode
    echo -n "Checking memory mode... "
    MEM0_MODE=${MEM0_MODE:-self-hosted}
    if [ "$MEM0_MODE" == "hosted" ]; then
        echo -e "${BLUE}Hosted (Mem0 cloud)${NC}"
        echo -n "Checking Mem0 API key... "
        if [ -z "$MEM0_API_KEY" ] || [ "$MEM0_API_KEY" == "your-mem0-api-key-here" ]; then
            echo -e "${RED}✗ Not set${NC}"
            echo "   Get your key from: https://mem0.dev/keys-beau"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "${GREEN}✓ Set${NC}"
        fi
    else
        echo -e "${GREEN}Self-hosted (local)${NC}"
    fi

    # Check language
    TUTOR_LANGUAGE=${TUTOR_LANGUAGE:-Spanish}
    echo "Tutor language: ${BLUE}$TUTOR_LANGUAGE${NC}"

    # Check user ID
    USER_ID=${USER_ID:-default_student}
    echo "User ID: ${BLUE}$USER_ID${NC}"
fi

# Check Docker (if applicable)
if [ -f docker-compose.yml ]; then
    echo -n "Checking Docker... "
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓ Installed${NC}"
    else
        echo -e "${YELLOW}⚠ Not installed (optional)${NC}"
    fi
fi

# Summary
echo ""
echo "=============================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration is valid!${NC}"
    echo ""
    echo "You're ready to run MemoryTutor:"
    echo "  ./scripts/run.sh"
    echo "  or"
    echo "  python tutor.py"
    echo ""
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}Note: $WARNINGS warning(s) found but not critical.${NC}"
    fi
else
    echo -e "${RED}✗ Found $ERRORS error(s)${NC}"
    echo ""
    echo "To fix issues automatically, run:"
    echo "  ./scripts/interactive-setup.sh"
    echo ""
    exit 1
fi
echo "=============================================="
echo ""
