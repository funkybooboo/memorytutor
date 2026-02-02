# Quick Start Guide 🚀

Get MemoryTutor running in **5 minutes or less**!

## TL;DR - Fastest Setup

```bash
# Clone and setup
git clone <repository-url>
cd memorytutor
./scripts/interactive-setup.sh

# Run
./scripts/run.sh
```

That's it! The interactive setup will guide you through everything.

---

## Prerequisites

You only need **two things**:

1. **Python 3.11+** - [Download here](https://www.python.org/downloads/)
2. **OpenAI API Key** - [Get free credits here](https://platform.openai.com/signup)

> **Note**: The OpenAI API key requires a payment method, but new users get free credits to start!

---

## Step-by-Step Setup (5 Minutes)

### Step 1: Get Your OpenAI API Key (2 minutes)

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

**Keep this key safe!** You'll need it in the next step.

### Step 2: Clone and Setup (2 minutes)

Open your terminal and run:

```bash
# Clone the repository
git clone <repository-url>
cd memorytutor

# Run interactive setup
./scripts/interactive-setup.sh
```

The setup script will:
- ✅ Check Python is installed
- ✅ Create a virtual environment
- ✅ Install dependencies
- ✅ Ask for your OpenAI API key
- ✅ Let you choose a language to learn
- ✅ Configure everything automatically

Just follow the prompts and press Enter to accept defaults!

### Step 3: Start Learning (1 minute)

```bash
./scripts/run.sh
```

You'll see:
```
🇪🇸  PERSONALIZED AI SPANISH TUTOR
Status: Memory Persistent | Mode: Self-Hosted | Storage: Qdrant (Local)
User: default_student
Commands: /memories, /forget [num], /help, exit

You:
```

**Start chatting!** Try:
- "Hi! I'm a complete beginner in Spanish."
- "How do I say 'hello' in Spanish?"
- "I want to learn Spanish for travel."

---

## Common First Commands

| What to Try | Why |
|-------------|-----|
| `Hi! I'm learning Spanish for a trip to Mexico.` | Tell the tutor about yourself |
| `/memories` | See what the tutor remembers |
| `/search [keyword]` | Find specific memories |
| `/stats` | View your memory statistics |
| `/help` | View all available commands |
| `¿Cómo estás?` | Practice what you've learned |

## Exploring Memory Commands

The tutor has powerful memory management features:

- **`/memories`** - List all memories
- **`/search Barcelona`** - Search for "Barcelona" in memories
- **`/add I prefer formal Spanish`** - Manually add a preference
- **`/forget 3`** - Delete memory #3
- **`/stats`** - See how many memories you have
- **`/export`** - Backup your memories to a file
- **`/clear`** - Start fresh (deletes everything)

---

## Choose a Different Language

Want to learn French instead of Spanish?

During setup, when asked:
```
Which language would you like to learn?
Language [Spanish]:
```

Just type your language:
- `French` → 🇫🇷
- `Japanese` → 🇯🇵
- `German` → 🇩🇪
- `Italian` → 🇮🇹
- `Chinese` → 🇨🇳
- And many more!

---

## Troubleshooting

### "Python 3 is not installed"

**Solution**: Install Python 3.11+ from [python.org/downloads](https://www.python.org/downloads/)

### "OpenAI API key is required"

**Solution**:
1. Get your key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Run `./scripts/interactive-setup.sh` again
3. Paste your key when prompted

### "Command not found: ./scripts/interactive-setup.sh"

**Solution**: Make sure you're in the `memorytutor` directory:
```bash
cd memorytutor
chmod +x scripts/*.sh
./scripts/interactive-setup.sh
```

### Script doesn't work on Windows

**Solution**: Use one of these methods:

**Option 1: WSL (Recommended)**
```bash
# Install WSL, then run:
wsl
cd /mnt/c/path/to/memorytutor
./scripts/interactive-setup.sh
```

**Option 2: Manual Setup**
```bash
# In PowerShell or Command Prompt:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Copy .env.example to .env
copy .env.example .env

# Edit .env with notepad
notepad .env
# Add your OPENAI_API_KEY

# Run
python tutor.py
```

---

## What's Happening Behind the Scenes?

When you run MemoryTutor:

1. **OpenAI GPT-4** powers the language teaching
2. **Mem0 + Qdrant** stores memories about you locally
3. **Every conversation** adds to your profile
4. **Memory persists** between sessions

Your data stays on your computer (unless you choose hosted mode).

---

## Next Steps

Once you're up and running:

- 📖 Read [README.md](../README.md) for full documentation
- ⚙️ See [CONFIGURATION.md](configuration.md) for advanced options
- 🐳 Try [Docker setup](deployment.md) for production use
- 🔧 Learn about [memory management](configuration.md#memory-management)

---

## Quick Reference

### Run the Tutor
```bash
./scripts/run.sh
```

### Reconfigure
```bash
./scripts/interactive-setup.sh
```

### Check Status
```bash
./scripts/validate.sh
```

### Use Docker Instead
```bash
cp .env.example .env
# Edit .env with your API key
docker-compose up
```

---

## Help & Support

- **Questions?** Check [README.md](../README.md) troubleshooting section
- **Issues?** Open an issue on GitHub
- **Tutorial**: Watch the [original video](https://youtu.be/m4ZnZXlOOYM)

---

**Ready?** Run `./scripts/interactive-setup.sh` and start learning! 🎉
