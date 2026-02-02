# MemoryTutor 🌍

A personalized AI language tutor with persistent memory that remembers everything about your learning journey.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Based on the tutorial**: [https://youtu.be/m4ZnZXlOOYM](https://youtu.be/m4ZnZXlOOYM)
> **Mem0 Platform**: [Sign up here](https://mem0.dev/beau-yt) | [Get API keys](https://mem0.dev/keys-beau)

## Overview

MemoryTutor is an interactive language tutoring application powered by OpenAI's GPT-4 and enhanced with Mem0's persistent memory system. Unlike traditional chatbots that forget everything between sessions, MemoryTutor remembers your learning preferences, progress, and personal context to provide truly personalized language instruction.

**Learn any language**: Spanish, French, German, Italian, Japanese, Chinese, Portuguese, and more!

### Key Features

- **Multi-Language Support**: Learn any language (Spanish, French, German, Italian, Japanese, Chinese, etc.)
- **Persistent Memory**: Remembers facts about you across sessions
- **Personalized Learning**: Adapts responses based on your history and preferences
- **Flexible Deployment**: Run locally, in Docker, or use hosted services
- **Memory Management**: View and manage what the tutor knows about you
- **Interactive CLI**: Simple, intuitive command-line interface
- **Multiple Storage Options**: Choose between local storage or cloud-hosted memory

## ⚡ 5-Minute Setup

**New to MemoryTutor?** Use our interactive setup for the easiest experience:

```bash
git clone <repository-url>
cd memorytutor
./scripts/interactive-setup.sh
```

The script will guide you through everything! Then run:

```bash
./scripts/run.sh
```

**That's it!** 🎉

### 📚 Documentation

Choose the guide that fits your experience level:

- 🚀 **[QUICKSTART.md](docs/quickstart.md)** - Complete beginner? Start here! (5-minute walkthrough)
- 📖 **[SETUP_GUIDE.md](docs/setup_guide.md)** - Detailed setup methods and first-run guide
- 📋 **[COMMANDS.md](docs/commands.md)** - Complete command reference with examples
- ⚙️ **[docs/CONFIGURATION.md](docs/configuration.md)** - Advanced configuration options
- 🐳 **[docs/DEPLOYMENT.md](docs/deployment.md)** - Production deployment guide

---

## Prerequisites

- **Python 3.11 or higher**
- **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))
- **Optional**: Mem0 API Key for hosted mode (get one at [mem0.dev](https://mem0.dev))
- **Optional**: Docker and Docker Compose for containerized deployment

## Manual Setup

### Option 1: Automated (Recommended)

```bash
./scripts/interactive-setup.sh  # Guides you through everything
./scripts/run.sh                 # Start the tutor
```

### Option 2: Manual Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd memorytutor
   ```

2. **Install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Run the tutor**
   ```bash
   python tutor.py
   ```

### Option 3: Docker Setup

1. **Clone and configure**
   ```bash
   git clone <repository-url>
   cd memorytutor
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up
   ```

That's it! Start chatting with your personalized language tutor.

## Helpful Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/interactive-setup.sh` | Interactive setup wizard (recommended for first time) |
| `./scripts/run.sh` | Quick start (auto-detects if setup needed) |
| `./scripts/validate.sh` | Check if configuration is correct |
| `./scripts/docker-run.sh` | Docker helper (up, down, logs, etc.) |

## Configuration

MemoryTutor supports three operational modes:

### 1. Local Self-Hosted (Default)

Stores all memory data locally on your machine.

```bash
# .env configuration
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=self-hosted
USE_DOCKER_QDRANT=false
```

**Pros**: Complete privacy, works offline (after setup), no additional costs
**Best for**: Development, testing, privacy-conscious users

### 2. Docker Self-Hosted

Runs everything in Docker containers with persistent storage.

```bash
# .env configuration
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=self-hosted
# USE_DOCKER_QDRANT is set automatically in docker-compose
```

**Pros**: Easy deployment, isolated environment, production-ready
**Best for**: Production deployments, team environments

### 3. Hosted Mode

Uses Mem0's cloud platform for memory storage.

```bash
# .env configuration
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=hosted
MEM0_API_KEY=your-mem0-key-here
```

**Pros**: No infrastructure to manage, automatic scaling, managed backups
**Best for**: Quick setup, managed service preference

### Configuration Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `MEM0_MODE` | No | `self-hosted` | Mode: `hosted` or `self-hosted` |
| `MEM0_API_KEY` | Conditional* | - | Mem0 API key (for hosted mode) |
| `USER_ID` | No | `default_student` | Unique user identifier |
| `USE_DOCKER_QDRANT` | No | `false` | Use Docker Qdrant (set to `true` for Docker) |
| `QDRANT_PATH` | No | `.qdrant_data` | Local storage path |
| `QDRANT_COLLECTION_NAME` | No | `language_tutor_session` | Collection name |
| `TUTOR_LANGUAGE` | No | `Spanish` | Language to learn (e.g., French, German, Japanese) |

*Required only when `MEM0_MODE=hosted`

See [docs/CONFIGURATION.md](docs/configuration.md) for complete configuration reference.

## Usage

### Choosing Your Language

Set your target language in the `.env` file:
```bash
TUTOR_LANGUAGE=Spanish    # or French, German, Japanese, Italian, Chinese, etc.
```

### Starting a Session

Run the tutor and start chatting in your target language (or ask questions in English):

```bash
python tutor.py
```

### Available Commands

#### Memory Management
| Command | Description |
|---------|-------------|
| `/memories` | List all stored memories about you |
| `/search [query]` | Search for specific memories using keywords |
| `/forget [num]` | Delete a specific memory by number |
| `/clear` | Delete ALL memories (asks for confirmation) |
| `/add [text]` | Manually add a fact to memory |
| `/stats` | View memory statistics (count, user ID, etc.) |

#### Data Management
| Command | Description |
|---------|-------------|
| `/export` | Export all memories to a JSON file |
| `/import [file]` | Import memories from a JSON file |

#### General
| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `exit` or `quit` | Exit the tutor |

> 📋 **See [COMMANDS.md](docs/commands.md) for detailed usage examples and workflows!**

### Example Session

```
===========================================================
🇪🇸  PERSONALIZED AI SPANISH TUTOR
Status: Memory Persistent | Mode: Self-Hosted | Storage: Qdrant (Local)
User: default_student
Commands: /help for full list | exit to quit
===========================================================

You: Hi! I'm learning Spanish because I'm moving to Barcelona next year.

AI: ¡Hola! That's wonderful that you're moving to Barcelona! I'll help you
prepare with practical Spanish for daily life in Spain. Let's start with
some basics...

You: /memories

🧠 KNOWLEDGE BASE:
1. User is learning Spanish for moving to Barcelona next year
2. User is interested in practical Spanish for daily life
-------------------------

You: /search Barcelona

🔍 Searching for: 'Barcelona'...

📋 SEARCH RESULTS (1 found):
1. User is learning Spanish for moving to Barcelona next year
--------------------------------------------------

You: /stats

📊 MEMORY STATISTICS:
  Total memories: 2
  User ID: default_student
  Language: Spanish
  Storage mode: self-hosted
  Collection: language_tutor_session
--------------------------------------------------
```

### Language Examples

**Learning French:**
```bash
# .env
TUTOR_LANGUAGE=French
```
Banner: `🇫🇷  PERSONALIZED AI FRENCH TUTOR`

**Learning Japanese:**
```bash
# .env
TUTOR_LANGUAGE=Japanese
```
Banner: `🇯🇵  PERSONALIZED AI JAPANESE TUTOR`

**Learning German:**
```bash
# .env
TUTOR_LANGUAGE=German
```
Banner: `🇩🇪  PERSONALIZED AI GERMAN TUTOR`

### Tips for Effective Learning

1. **Set your target language**: Configure `TUTOR_LANGUAGE` in `.env` before starting
2. **Tell the tutor about yourself**: Share your goals, level, and interests
3. **Use it regularly**: Memory improves with more conversations
4. **Review memories**: Use `/memories` to see what the tutor knows
5. **Search memories**: Use `/search [keyword]` to find specific facts
6. **Add manual facts**: Use `/add [fact]` to explicitly store information
7. **Export for backup**: Use `/export` to save your progress
8. **Update preferences**: Tell the tutor when your goals or interests change

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│                   (CLI - tutor.py)                  │
└─────────────────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐         ┌──────────────────┐
│   OpenAI GPT-4   │         │   Memory System   │
│                  │         │   (Mem0 Library)  │
└──────────────────┘         └──────────────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      │                               │
                      ▼                               ▼
             ┌─────────────────┐         ┌─────────────────┐
             │ Qdrant (Local)  │         │  Mem0 Platform  │
             │ Vector Database │         │   (Cloud API)   │
             └─────────────────┘         └─────────────────┘
              Self-Hosted Mode               Hosted Mode
```

### How It Works

1. **User sends a message** → The tutor receives your input
2. **Memory search** → Relevant facts about you are retrieved
3. **Context building** → Your message + relevant memories = personalized context
4. **AI response** → OpenAI generates a response based on the context
5. **Memory update** → New facts are automatically extracted and stored

## Installation

### Local Python Installation

1. **System Requirements**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Docker Installation

1. **System Requirements**
   ```bash
   docker --version  # Should be 20.10+
   docker-compose --version  # Should be 2.0+
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and run**
   ```bash
   docker-compose up --build
   ```

4. **Interact with the tutor**
   ```bash
   docker attach memorytutor-app
   # Press Ctrl+P then Ctrl+Q to detach without stopping
   ```

## Troubleshooting

### Common Issues

**Error: "OPENAI_API_KEY not set"**
- Ensure `.env` file exists in the project root
- Check the file has `OPENAI_API_KEY=sk-...` with your actual key
- No spaces around the `=` sign

**Error: "Failed to initialize memory system"**
- **Self-hosted**: Check if Qdrant is accessible
  ```bash
  # For Docker: docker-compose ps
  # For local: check .qdrant_data/ directory exists
  ```
- **Hosted**: Verify `MEM0_API_KEY` is correct

**Qdrant Connection Refused (Docker)**
```bash
# Check if services are running
docker-compose ps

# View logs
docker-compose logs qdrant

# Restart services
docker-compose restart
```

**Port Already in Use**
```bash
# Check what's using port 6333
lsof -i :6333

# Change port in docker-compose.yml if needed
```

### Self-Diagnosis

Run the validation script to check your setup:

```bash
./scripts/validate.sh
```

This will tell you exactly what's wrong and how to fix it!

### Getting Help

- 🚀 **New users**: See [QUICKSTART.md](docs/quickstart.md)
- ⚙️ **Configuration**: See [docs/CONFIGURATION.md](docs/configuration.md)
- 🐳 **Deployment**: See [docs/DEPLOYMENT.md](docs/deployment.md)
- 🐛 **Issues**: Submit on GitHub repository

## Development

### Project Structure

```
memorytutor/
├── tutor.py              # Main application
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Multi-container setup
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── docs/
│   ├── CONFIGURATION.md # Configuration reference
│   └── DEPLOYMENT.md    # Deployment guide
└── scripts/
    ├── setup.sh         # Setup helper
    └── docker-run.sh    # Docker helper
```

### Running Tests

Currently, testing is manual. See the verification section in [docs/DEPLOYMENT.md](docs/deployment.md).

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security

- Never commit `.env` file to version control
- Keep API keys secure and rotate them regularly
- Use environment-specific configurations
- Review [docs/DEPLOYMENT.md](docs/deployment.md) for production security practices

## License

This project is licensed under the MIT License.

## Credits

- Original tutorial: [YouTube Tutorial](https://youtu.be/m4ZnZXlOOYM)
- Powered by [OpenAI](https://openai.com)
- Memory management by [Mem0](https://mem0.dev)
- Vector database by [Qdrant](https://qdrant.tech)

## Resources

- **Mem0 Platform**: [mem0.dev](https://mem0.dev/beau-yt)
- **Mem0 API Keys**: [mem0.dev/keys-beau](https://mem0.dev/keys-beau)
- **OpenAI API Keys**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Qdrant Documentation**: [qdrant.tech/documentation](https://qdrant.tech/documentation/)

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Review the documentation in the `docs/` directory
- Check the troubleshooting section above

---

**Made with ❤️ for language learners everywhere**