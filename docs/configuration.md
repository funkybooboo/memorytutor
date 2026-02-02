# Configuration Reference

Complete reference for configuring MemoryTutor.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Configuration Modes](#configuration-modes)
- [Advanced Qdrant Configuration](#advanced-qdrant-configuration)
- [Memory Management](#memory-management)
- [OpenAI Configuration](#openai-configuration)

## Environment Variables

All configuration is done through environment variables in the `.env` file.

### Core Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key from platform.openai.com |
| `MEM0_MODE` | No | `self-hosted` | Memory backend mode: `hosted` or `self-hosted` |
| `USER_ID` | No | `default_student` | Unique identifier for the student/user |
| `TUTOR_LANGUAGE` | No | `Spanish` | Language to learn (Spanish, French, German, Italian, Japanese, Chinese, etc.) |

### Hosted Mode Configuration

Only required when `MEM0_MODE=hosted`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MEM0_API_KEY` | Yes* | - | Mem0 Platform API key from mem0.dev |
| `MEM0_ORG_ID` | No | - | Organization ID (optional) |
| `MEM0_PROJECT_ID` | No | - | Project ID (optional) |

*Required only when using hosted mode.

### Self-Hosted Mode Configuration

Only required when `MEM0_MODE=self-hosted`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `USE_DOCKER_QDRANT` | No | `false` | Set to `true` when using Docker Compose |
| `QDRANT_HOST` | No | `localhost` | Qdrant server hostname |
| `QDRANT_PORT` | No | `6333` | Qdrant REST API port |
| `QDRANT_PATH` | No | `.qdrant_data` | Local file path for Qdrant storage |
| `QDRANT_COLLECTION_NAME` | No | `language_tutor_session` | Name of the vector collection |

## Configuration Modes

MemoryTutor supports three operational modes:

### 1. Local Self-Hosted Mode

**Use Case:** Development, full control, no external dependencies except OpenAI

**Configuration:**
```bash
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=self-hosted
USE_DOCKER_QDRANT=false
QDRANT_PATH=.qdrant_data
```

**Characteristics:**
- Stores vectors in local `.qdrant_data/` directory
- No additional services required
- Data persists between runs
- Fastest startup time
- Full data privacy

**When to Use:**
- Local development
- Testing and experimentation
- Offline usage (after initial setup)
- When you need complete control over data

### 2. Docker Self-Hosted Mode

**Use Case:** Production deployment, containerized environments, easy scaling

**Configuration:**
```bash
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=self-hosted
USE_DOCKER_QDRANT=true
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

**Characteristics:**
- Runs Qdrant in separate container
- Data persists in Docker volume
- Health checks and automatic restarts
- Easy to deploy and manage
- Isolated environment

**When to Use:**
- Production deployments
- Team development environments
- When you need containerization
- CI/CD pipelines

### 3. Hosted Mode

**Use Case:** Simplest setup, managed service, no infrastructure management

**Configuration:**
```bash
OPENAI_API_KEY=sk-your-key-here
MEM0_MODE=hosted
MEM0_API_KEY=your-mem0-key-here
```

**Characteristics:**
- No Qdrant setup required
- Mem0 Platform handles all storage
- Cloud-based memory management
- Automatic scaling and backups
- Minimal local setup

**When to Use:**
- Quick prototyping
- When you prefer managed services
- Don't want to manage Qdrant
- Cloud-first architecture

## Mode Comparison

| Feature | Local Self-Hosted | Docker Self-Hosted | Hosted |
|---------|-------------------|-------------------|---------|
| **Setup Complexity** | Low | Medium | Lowest |
| **External Services** | None | Docker | Mem0 Platform |
| **Data Location** | Local disk | Docker volume | Mem0 Cloud |
| **Scalability** | Limited | High | Very High |
| **Cost** | Free* | Free* | Paid** |
| **Offline Support** | Yes | Yes | No |
| **Backup Required** | Manual | Manual | Automatic |
| **Best For** | Development | Production | Simplicity |

*Only OpenAI API costs
**Mem0 Platform pricing applies

## Advanced Qdrant Configuration

### Language Configuration

Set the target language for tutoring:

```bash
TUTOR_LANGUAGE=Spanish
```

**Supported Languages:**
Any language supported by GPT-4, including:
- Spanish (`Spanish`)
- French (`French`)
- German (`German`)
- Italian (`Italian`)
- Portuguese (`Portuguese`)
- Japanese (`Japanese`)
- Chinese (`Chinese`)
- Korean (`Korean`)
- Russian (`Russian`)
- Arabic (`Arabic`)
- Hindi (`Hindi`)
- And many more!

**Tips:**
- Use the English name of the language
- Capitalize the first letter
- The tutor will automatically adapt its teaching style
- The banner will display the appropriate flag emoji

### Collection Settings

The collection name identifies the vector database collection:

```bash
QDRANT_COLLECTION_NAME=language_tutor_session
```

**Best Practices:**
- Use descriptive names: `{app}_{language}_{purpose}`
- Separate collections for different languages or user types
- Avoid spaces in collection names
- Keep names lowercase with underscores

**Examples:**
- `spanish_tutor_beginners`
- `french_conversation_practice`
- `japanese_writing_skills`
- `german_grammar_advanced`

### Storage Configuration

**Local Mode:**
```bash
QDRANT_PATH=.qdrant_data
```

- Relative paths are relative to application directory
- Absolute paths are supported: `/var/data/qdrant`
- Ensure write permissions on the directory
- Directory is created automatically if it doesn't exist

**Docker Mode:**
```bash
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

- `qdrant` is the Docker Compose service name
- Port 6333 is Qdrant's REST API
- Port 6334 is gRPC (not used by default)

### Multiple Collections

To run multiple isolated tutors:

**Option 1: Different Languages**
```bash
# Spanish tutor
USER_ID=student_001
TUTOR_LANGUAGE=Spanish
QDRANT_COLLECTION_NAME=spanish_tutor

# French tutor
USER_ID=student_001
TUTOR_LANGUAGE=French
QDRANT_COLLECTION_NAME=french_tutor
```

**Option 2: Different Collection Names**
```bash
# Student 1
USER_ID=student_001
QDRANT_COLLECTION_NAME=tutor_student_001

# Student 2
USER_ID=student_002
QDRANT_COLLECTION_NAME=tutor_student_002
```

**Option 3: Same Collection, Different Users**
```bash
# Student 1
USER_ID=student_001
TUTOR_LANGUAGE=Spanish
QDRANT_COLLECTION_NAME=language_tutor

# Student 2
USER_ID=student_002
TUTOR_LANGUAGE=French
QDRANT_COLLECTION_NAME=language_tutor
```

Option 3 is most efficient for large numbers of users learning different languages.

### Qdrant Performance Tuning

For advanced users, you can pass additional Qdrant configuration through environment variables or by modifying `tutor.py`.

**Memory Management:**
- Qdrant uses memory-mapped files
- Ensure sufficient disk space (vectors are ~1KB each)
- Monitor with: `curl http://localhost:6333/collections/spanish_tutor_session`

**Optimization Tips:**
- Use SSD storage for better performance
- Allocate adequate RAM (recommend 512MB minimum)
- For large datasets (>100K vectors), consider Qdrant Cloud

## Memory Management

### How Memory Works

MemoryTutor uses the Mem0 library to automatically extract and store facts from conversations:

1. **User sends message** → Stored as potential memory
2. **Mem0 extracts facts** → AI identifies key information
3. **Facts stored as vectors** → Semantic search enabled
4. **Next conversation** → Relevant facts retrieved
5. **Personalized response** → Based on stored context

### Memory Commands

**List all memories:**
```
/memories
```
Shows all facts stored about the user.

**Search memories:**
```
/search Barcelona
```
Find memories containing specific keywords.

**Manually add a memory:**
```
/add I prefer Latin American Spanish
```
Explicitly store a fact without chatting.

**Delete a memory:**
```
/forget [number]
```
Removes a specific fact by its number.

**Clear all memories:**
```
/clear
```
Deletes all memories (asks for confirmation).

**View statistics:**
```
/stats
```
Shows memory count, user ID, language, and storage mode.

**Export memories:**
```
/export
```
Saves all memories to a timestamped JSON file.

**Import memories:**
```
/import memories_user_20260102.json
```
Loads memories from a previously exported file.

**Help:**
```
/help
```
Shows all available commands.

### Memory Best Practices

**For Students:**
- Start by telling the tutor about yourself
- Mention your learning goals and target language
- Share your current language level
- Mention specific interests (travel, business, culture, etc.)
- Update preferences as needed

**For Developers:**
- Use distinct `USER_ID` values per student
- Consider collection naming strategy
- Monitor memory storage growth
- Implement memory cleanup for inactive users

### Memory Privacy

**Self-Hosted Mode:**
- All data stored locally or in your infrastructure
- You have complete control
- No data sent to third parties (except OpenAI for chat)

**Hosted Mode:**
- Data stored on Mem0 Platform
- Subject to Mem0's privacy policy
- Encrypted in transit and at rest
- Consider for non-sensitive use cases

## OpenAI Configuration

### API Key

Get your API key from: https://platform.openai.com/api-keys

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Security:**
- Never commit API keys to version control
- Use `.env` file (gitignored)
- Rotate keys regularly
- Monitor usage on OpenAI dashboard

### Model Configuration

Currently uses `gpt-4o` model (hardcoded in `tutor.py`).

To change the model, edit `tutor.py`:
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo", etc.
    messages=[...]
)
```

**Model Recommendations:**
- `gpt-4o`: Best quality, higher cost
- `gpt-4o-mini`: Good balance of quality and cost
- `gpt-3.5-turbo`: Fastest, lowest cost

### Rate Limits

OpenAI enforces rate limits based on your account tier:

- **Free tier**: Low limits, may need retries
- **Pay-as-you-go**: Higher limits
- **Enterprise**: Custom limits

**Handling Rate Limits:**
Add retry logic or implement exponential backoff in production deployments.

### Cost Optimization

**Tips to reduce costs:**
1. Use cheaper models (gpt-4o-mini or gpt-3.5-turbo)
2. Limit context sent to API (current implementation already optimized)
3. Use memory search to send only relevant facts
4. Monitor usage via OpenAI dashboard
5. Set spending limits in OpenAI account

**Current Implementation:**
MemoryTutor is already optimized:
- Only sends relevant memories (via semantic search)
- Doesn't send full conversation history
- Minimal system prompt

## User Management

### Single User

Default configuration for one student:

```bash
USER_ID=default_student
```

### Multiple Users

**Option 1: Environment Variables**

Create separate `.env` files:
```bash
# .env.student1
USER_ID=student_001
QDRANT_COLLECTION_NAME=tutor_session

# .env.student2
USER_ID=student_002
QDRANT_COLLECTION_NAME=tutor_session
```

Run with specific config:
```bash
python tutor.py --env .env.student1
```

**Option 2: Runtime Selection**

Modify `tutor.py` to prompt for USER_ID at startup.

**Option 3: Separate Instances**

Use Docker Compose to run multiple isolated instances with different USER_IDs.

## Validation and Debugging

### Configuration Validation

MemoryTutor validates configuration on startup:

```python
def validate_config():
    # Checks required variables
    # Shows helpful error messages
    # Exits if configuration invalid
```

**Common Validation Errors:**
- Missing `OPENAI_API_KEY`
- Missing `MEM0_API_KEY` in hosted mode
- Invalid `MEM0_MODE` value

### Debug Mode

To debug configuration issues:

1. **Check environment variables:**
   ```bash
   source .env
   env | grep -E 'OPENAI|MEM0|QDRANT|USER'
   ```

2. **Test Qdrant connection:**
   ```bash
   curl http://localhost:6333/healthz
   ```

3. **Verify OpenAI API key:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

4. **Check Docker services:**
   ```bash
   docker-compose ps
   docker-compose logs
   ```

## Configuration Examples

### Example 1: Local Development (Spanish)

`.env` file:
```bash
OPENAI_API_KEY=sk-proj-abc123
MEM0_MODE=self-hosted
USE_DOCKER_QDRANT=false
USER_ID=test_user
TUTOR_LANGUAGE=Spanish
```

**Usage:**
```bash
python tutor.py
```

### Example 2: Docker Production (Japanese)

`.env` file:
```bash
OPENAI_API_KEY=sk-proj-abc123
MEM0_MODE=self-hosted
USE_DOCKER_QDRANT=true
QDRANT_HOST=qdrant
USER_ID=production_user
TUTOR_LANGUAGE=Japanese
```

**Usage:**
```bash
docker-compose up -d
docker attach memorytutor-app
```

### Example 3: Hosted Mem0 (French)

`.env` file:
```bash
OPENAI_API_KEY=sk-proj-abc123
MEM0_MODE=hosted
MEM0_API_KEY=m0-xxx-yyy
USER_ID=cloud_user
TUTOR_LANGUAGE=French
```

**Usage:**
```bash
python tutor.py
# No Qdrant needed!
```

## Troubleshooting Configuration

### Issue: "OPENAI_API_KEY not set"

**Solution:**
1. Check `.env` file exists
2. Verify syntax: `OPENAI_API_KEY=sk-...` (no spaces around =)
3. Ensure `.env` is in same directory as `tutor.py`
4. Check file permissions: `chmod 600 .env`

### Issue: "Failed to initialize memory system"

**Solution:**
1. Verify `MEM0_MODE` is correct
2. Check Qdrant is running (if self-hosted)
3. Verify `MEM0_API_KEY` if using hosted mode
4. Check network connectivity

### Issue: Qdrant connection refused

**Solution:**
1. Ensure Qdrant is running: `docker-compose ps`
2. Check port not in use: `lsof -i :6333`
3. Verify `QDRANT_HOST` and `QDRANT_PORT`
4. Check Docker network: `docker network ls`

## Best Practices

1. **Never commit `.env` to git** - Use `.env.example` as template
2. **Use descriptive USER_IDs** - Makes debugging easier
3. **Separate environments** - Different configs for dev/staging/prod
4. **Monitor API usage** - Set up alerts for unexpected costs
5. **Regular backups** - Especially for self-hosted Qdrant data
6. **Document changes** - Keep notes on custom configurations
7. **Test configuration changes** - In development before production
8. **Use secrets management** - For production deployments

## Further Reading

- [Deployment Guide](deployment.md) - Production deployment strategies
- [Mem0 Documentation](https://docs.mem0.ai/) - Mem0 Platform details
- [Qdrant Documentation](https://qdrant.tech/documentation/) - Advanced Qdrant features
- [OpenAI API Docs](https://platform.openai.com/docs/) - OpenAI API reference
