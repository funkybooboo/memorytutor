# MemoryTutor 🌍

A personalized AI language tutor with persistent memory that remembers everything about your learning journey.

[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Learn any language**: Spanish, French, German, Italian, Japanese, Chinese, and more!

## 🚀 Quick Start

```bash
git clone <repository-url>
cd memorytutor
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
./run.sh
```

That's it! 🎉

## Two Deployment Options

### Option 1: Docker (Default - Recommended)

**Best for**: Everyone - easiest setup, runs locally with full privacy

Runs everything locally in Docker containers. Your data stays on your machine.

**Setup:**
```bash
# 1. Add to .env:
OPENAI_API_KEY=sk-your-key-here
TUTOR_LANGUAGE=Spanish  # or German, French, Japanese, etc.

# 2. Run:
./run.sh
```

**Requirements:** Docker installed ([get it here](https://docs.docker.com/get-docker/))

---

### Option 2: Mem0 Hosted Platform

**Best for**: Don't want to run Docker, prefer managed cloud service

Uses Mem0's cloud platform for memory storage (requires Mem0 account).

**Setup:**
```bash
# 1. Add to .env:
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=hosted
MEM0_API_KEY=your-mem0-key-here
TUTOR_LANGUAGE=Spanish

# 2. Run:
./run.sh --local
```

**Requirements:**
- Python 3.11+
- Mem0 API key ([sign up here](https://mem0.dev/beau-yt))

---

## What You Get

- **Persistent Memory**: The tutor remembers everything across sessions
- **Personalized Learning**: Adapts to your level, goals, and preferences
- **Any Language**: Spanish, French, German, Japanese, Chinese, and more
- **Privacy**: With Docker mode, all data stays on your machine

## Available Commands

Once running, you can use these commands:

| Command | Description |
|---------|-------------|
| `/memories` | See what the tutor knows about you |
| `/search [query]` | Search your memories |
| `/forget [num]` | Delete a specific memory |
| `/add [text]` | Manually add a fact to memory |
| `/help` | Show all commands |
| `exit` | Quit |

## Docker Tips

```bash
./run.sh                 # Start and connect to tutor
docker compose down      # Stop Qdrant database
docker compose logs      # View database logs
```

Type `exit` or `quit` to end your session.

## Configuration

Edit `.env` to customize:

```bash
OPENAI_API_KEY=sk-your-key-here    # Required
TUTOR_LANGUAGE=Spanish             # Default: Spanish
USER_ID=your_name                  # Default: default_student
MEM0_MODE=self-hosted              # or "hosted" for Mem0 platform
```

## Architecture

**Docker Mode (Default):**
```
Your Terminal → memorytutor-app (Python + OpenAI + Mem0)
                     ↓
                memorytutor-qdrant (Vector Database)
```
Everything runs locally in isolated containers.

**Hosted Mode:**
```
Your Terminal → Python (local) → OpenAI API + Mem0 Platform (cloud)
```
Memory stored on Mem0's cloud platform.

## Example Session

```
============================================================
🇪🇸  PERSONALIZED AI SPANISH TUTOR
Status: Memory Persistent | Mode: Self-Hosted | Storage: Qdrant (Docker)
User: default_student
Commands: /help for full list | exit to quit
============================================================

You: Hi! I'm learning Spanish because I'm moving to Barcelona next year.

AI: ¡Hola! That's wonderful that you're moving to Barcelona! I'll help you
prepare with practical Spanish for daily life in Spain...

You: /memories

🧠 KNOWLEDGE BASE:
1. User is learning Spanish for moving to Barcelona next year
2. User is interested in practical Spanish for daily life
```

## Troubleshooting

**Docker containers won't start:**
```bash
docker compose logs
```

**Port already in use:**
Edit `docker-compose.yml` and change the port mappings.

**Reset everything:**
```bash
docker compose down -v  # Warning: deletes all stored memories
```

## Resources

- **OpenAI API Keys**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Mem0 Platform**: [mem0.dev](https://mem0.dev/beau-yt)
- **Tutorial Video**: [YouTube](https://youtu.be/m4ZnZXlOOYM)

## License

MIT License - see repository for details

---

**Made with ❤️ for language learners everywhere**
