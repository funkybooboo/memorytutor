# MemoryTutor Setup Guide

## 🎯 Three Ways to Get Started

Choose the method that works best for you:

### 1. Absolute Easiest (Recommended) ⭐

```bash
git clone <repository-url>
cd memorytutor
./scripts/interactive-setup.sh
./scripts/run.sh
```

**What happens:**
- Interactive wizard guides you through setup
- Prompts for your OpenAI API key
- Asks which language you want to learn
- Configures everything automatically
- Takes 2-3 minutes total

**Perfect for:** First-time users, beginners, anyone who wants zero hassle

---

### 2. Quick Manual Setup

```bash
git clone <repository-url>
cd memorytutor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env - add your OPENAI_API_KEY
python tutor.py
```

**What you need:** Basic command line knowledge

**Perfect for:** Developers who prefer manual control

---

### 3. Docker Setup

```bash
git clone <repository-url>
cd memorytutor
cp .env.example .env
# Edit .env - add your OPENAI_API_KEY
docker-compose up
```

**What you need:** Docker and Docker Compose installed

**Perfect for:** Production deployments, containerized environments

---

## 📋 Prerequisites

**Required:**
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- OpenAI API key ([Get one](https://platform.openai.com/api-keys))

**Optional:**
- Docker ([Install](https://docs.docker.com/get-docker/)) - only if using Docker method
- Mem0 API key ([Get one](https://mem0.dev/keys-beau)) - only if using hosted mode

---

## 🔧 Configuration

### Default Configuration (Works Out of the Box)

The application comes with sensible defaults:

- **Language**: Spanish (easily changed to any language)
- **Storage**: Local (self-hosted, no external dependencies except OpenAI)
- **User ID**: `default_student`
- **Memory**: Persistent across sessions

### Customizing Your Setup

Edit `.env` file to change settings:

```bash
# Change language
TUTOR_LANGUAGE=French    # or German, Japanese, Italian, Chinese, etc.

# Change user ID (useful for multiple users)
USER_ID=john_student

# Use hosted Mem0 instead of local storage
MEM0_MODE=hosted
MEM0_API_KEY=your-mem0-api-key
```

See [CONFIGURATION.md](configuration.md) for all options.

---

## 🚀 Running MemoryTutor

### Easiest Way

```bash
./scripts/run.sh
```

This script:
- Checks if setup is complete
- Runs interactive setup if needed
- Activates virtual environment
- Starts the tutor

### Manual Way

```bash
source venv/bin/activate  # Activate virtual environment
python tutor.py           # Run the tutor
```

### Docker Way

```bash
docker-compose up         # Start in foreground
# OR
docker-compose up -d      # Start in background
docker attach memorytutor-app  # Attach to interact
```

---

## ✅ Verifying Your Setup

Run the validation script to check everything:

```bash
./scripts/validate.sh
```

This checks:
- ✓ Python version
- ✓ Virtual environment
- ✓ Dependencies installed
- ✓ Configuration file exists
- ✓ API keys are set
- ✓ Settings are valid

---

## 🎓 Your First Session

When you start MemoryTutor for the first time, you'll see:

```
============================================================
🇪🇸  PERSONALIZED AI SPANISH TUTOR
Status: Memory Persistent | Mode: Self-Hosted | Storage: Qdrant (Local)
User: default_student
Commands: /memories, /forget [num], /help, exit
============================================================

👋 Welcome! This appears to be your first session.
I'm your personal Spanish tutor with persistent memory.

💡 Quick Tips:
  • Start by telling me about yourself and your Spanish learning goals
  • I'll remember everything across sessions
  • Use /help to see all commands
  • Use /memories to see what I know about you

Let's begin! Tell me about yourself...

You:
```

### What to Say First

Good first messages:
- "Hi! I'm a complete beginner in Spanish."
- "I'm learning Spanish because I'm moving to Mexico next year."
- "I want to focus on conversational Spanish for travel."
- "I studied Spanish in school but haven't practiced in years."

The tutor will remember this context and personalize all future lessons!

---

## 📚 Available Commands

| Command | What It Does |
|---------|--------------|
| `/help` | Show all available commands |
| `/memories` | List everything the tutor knows about you |
| `/search [query]` | Search for specific memories |
| `/add [text]` | Manually add a fact to memory |
| `/forget [num]` | Delete a specific memory by number |
| `/clear` | Delete ALL memories (with confirmation) |
| `/stats` | View memory statistics |
| `/export` | Export memories to JSON file |
| `/import [file]` | Import memories from JSON file |
| `exit` or `quit` | Exit the tutor |

---

## 🛠️ Helpful Utilities

### Check Configuration
```bash
./scripts/validate.sh
```
Validates your setup and shows what's wrong (if anything).

### Reconfigure
```bash
./scripts/interactive-setup.sh
```
Re-run the setup wizard to change settings.

### Docker Management
```bash
./scripts/docker-run.sh up        # Start services
./scripts/docker-run.sh down      # Stop services
./scripts/docker-run.sh logs      # View logs
./scripts/docker-run.sh status    # Check status
./scripts/docker-run.sh attach    # Attach to interactive session
```

---

## 🔥 Common Use Cases

### Learning Multiple Languages

Create separate configurations:

```bash
# Spanish configuration
cp .env .env.spanish
# Edit .env.spanish: TUTOR_LANGUAGE=Spanish, USER_ID=me_spanish

# French configuration
cp .env .env.french
# Edit .env.french: TUTOR_LANGUAGE=French, USER_ID=me_french

# Run with specific config
cp .env.spanish .env && python tutor.py
```

### Multiple Users on Same Computer

Each user gets their own profile:

```bash
# User 1
USER_ID=alice_student
TUTOR_LANGUAGE=Spanish

# User 2
USER_ID=bob_student
TUTOR_LANGUAGE=French
```

Memories are kept separate by USER_ID.

### Switching from Local to Hosted

1. Get Mem0 API key from [mem0.dev/keys-beau](https://mem0.dev/keys-beau)
2. Edit `.env`:
   ```bash
   MEM0_MODE=hosted
   MEM0_API_KEY=your-key-here
   ```
3. Restart the tutor

Your local memories won't transfer automatically (they're separate systems).

---

## 📖 Documentation Index

| Document | Purpose |
|----------|---------|
| [README.md](../README.md) | Main documentation and overview |
| [QUICKSTART.md](quickstart.md) | Beginner-friendly step-by-step guide |
| [SETUP_GUIDE.md](setup_guide.md) | This file - setup methods and first run |
| [CONFIGURATION.md](configuration.md) | Complete configuration reference |
| [DEPLOYMENT.md](deployment.md) | Production deployment guide |

---

## ❓ Troubleshooting

### "Python 3 is not installed"

**Solution:** Download and install from [python.org/downloads](https://www.python.org/downloads/)

### "OpenAI API key is required"

**Solution:**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy the key
4. Add to `.env` file: `OPENAI_API_KEY=sk-...`

### "Failed to initialize memory system"

**Solution for self-hosted mode:**
- Qdrant is starting automatically - this error usually resolves on retry
- If persistent, check `.qdrant_data/` directory permissions

**Solution for hosted mode:**
- Verify `MEM0_API_KEY` is correct
- Check internet connection

### Scripts don't run on Windows

**Option 1 - WSL (Recommended):**
```bash
wsl
cd /mnt/c/path/to/memorytutor
./scripts/interactive-setup.sh
```

**Option 2 - Manual Setup:**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env  # Add your OPENAI_API_KEY
python tutor.py
```

### Need More Help?

1. Run `./scripts/validate.sh` to diagnose issues
2. Check [QUICKSTART.md](quickstart.md) for detailed steps
3. See [README.md](../README.md) troubleshooting section
4. Submit an issue on GitHub

---

## 🎉 Success!

If you've made it this far, you should have MemoryTutor running!

**What now?**
- Start a conversation with your tutor
- Tell it about your learning goals
- Practice regularly (the memory improves over time!)
- Use `/memories` to see what it remembers
- Try different languages by changing `TUTOR_LANGUAGE`

**Happy learning!** 🌍📚✨
