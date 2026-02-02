# MemoryTutor Command Reference

Quick reference for all available commands in MemoryTutor.

## Memory Management Commands

### View & Search

| Command | Description | Example |
|---------|-------------|---------|
| `/memories` | List all stored memories | `/memories` |
| `/search [query]` | Search for specific memories | `/search Barcelona` |
| `/stats` | View memory statistics | `/stats` |

### Modify

| Command | Description | Example |
|---------|-------------|---------|
| `/add [text]` | Manually add a fact | `/add I prefer formal Spanish` |
| `/forget [num]` | Delete a specific memory | `/forget 3` |
| `/clear` | Delete ALL memories | `/clear` |

## Data Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/export` | Export memories to JSON file | `/export` |
| `/import [file]` | Import memories from JSON file | `/import memories_user_20260102.json` |

## General Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all commands | `/help` |
| `exit` or `quit` | Exit the tutor | `exit` |

---

## Detailed Usage

### `/memories` - List All Memories
Lists every fact the tutor knows about you, numbered for easy reference.

**Output:**
```
🧠 KNOWLEDGE BASE:
1. User is learning Spanish for moving to Barcelona
2. User prefers conversational over formal Spanish
3. User is interested in food-related vocabulary
```

### `/search [query]` - Search Memories
Search through your memories using keywords.

**Examples:**
```
/search Barcelona        # Find memories mentioning Barcelona
/search food             # Find food-related memories
/search beginner level   # Find memories about your level
```

**Output:**
```
🔍 Searching for: 'Barcelona'...

📋 SEARCH RESULTS (2 found):
1. User is learning Spanish for moving to Barcelona
2. User wants to focus on Barcelona dialect
```

### `/add [text]` - Manually Add Memory
Explicitly add a fact without having to work it into conversation.

**Examples:**
```
/add I'm allergic to seafood
/add I prefer Latin American Spanish over Spain Spanish
/add My level is intermediate B1
/add I work in the medical field
```

### `/forget [num]` - Delete Specific Memory
Delete a memory by its number (from `/memories` list).

**Usage:**
1. Run `/memories` to see the list
2. Note the number of the memory to delete
3. Run `/forget [number]`

**Example:**
```
You: /memories

🧠 KNOWLEDGE BASE:
1. User is learning Spanish
2. User has incorrect fact here    <-- Want to delete this
3. User prefers morning study

You: /forget 2

✓ Pruned memory 2.
```

### `/clear` - Delete All Memories
Deletes ALL memories (asks for confirmation first).

**Usage:**
```
You: /clear

⚠️  WARNING: This will delete ALL 15 memories!
Type 'yes' to confirm: yes

✓ Cleared all memories (15 deleted).
```

**Use cases:**
- Starting fresh with a clean slate
- Switching to a different learning focus
- Testing the system

### `/stats` - View Statistics
See information about your memory storage.

**Output:**
```
📊 MEMORY STATISTICS:
  Total memories: 12
  User ID: default_student
  Language: Spanish
  Storage mode: self-hosted
  Collection: language_tutor_session
```

### `/export` - Export Memories
Saves all your memories to a JSON file with a timestamp.

**Usage:**
```
You: /export

✓ Exported 12 memories to: memories_default_student_20260102_143022.json
```

**File format:**
```json
{
  "user_id": "default_student",
  "language": "Spanish",
  "export_date": "2026-01-02T14:30:22",
  "total_memories": 12,
  "memories": [
    {
      "text": "User is learning Spanish for travel",
      "id": "mem-uuid-123"
    },
    ...
  ]
}
```

**Use cases:**
- Backup before `/clear`
- Share progress with a teacher
- Move between devices
- Migrate to different storage modes

### `/import [file]` - Import Memories
Load memories from a previously exported file.

**Usage:**
```
You: /import memories_default_student_20260102_143022.json

📥 Found 12 memories in memories_default_student_20260102_143022.json
Import these memories? (yes/no): yes

✓ Imported 12 memories.
```

**Notes:**
- Imported memories are added to existing ones (not replaced)
- If you want to replace, use `/clear` first
- Files must be in JSON format from `/export`

---

## Common Workflows

### Workflow 1: Regular Usage
```
1. Start tutor
2. Chat naturally
3. Use /memories occasionally to review
4. Use /forget to remove mistakes
5. Use /export weekly for backups
```

### Workflow 2: Managing Memories
```
1. /stats                     # Check memory count
2. /memories                  # Review all memories
3. /search [topic]            # Find specific ones
4. /forget [num]              # Remove incorrect ones
5. /add [new fact]            # Add explicit preferences
```

### Workflow 3: Starting Fresh
```
1. /export                    # Backup current memories
2. /clear                     # Delete everything
3. Start new conversations
4. /import [file] if needed   # Restore if you change your mind
```

### Workflow 4: Switching Devices
```
On Device A:
1. /export                    # Creates JSON file

On Device B:
1. Copy JSON file over
2. /import [filename]         # Load memories
3. Continue learning
```

### Workflow 5: Experimenting
```
1. /add I want to learn slang             # Add preference
2. Chat to test
3. /search slang                          # See what was stored
4. /forget [num] if not working well      # Remove if needed
```

---

## Tips & Tricks

### Efficient Memory Management
- Use `/search` instead of scrolling through `/memories`
- Add explicit preferences with `/add` to guide the tutor
- Export regularly to avoid losing progress
- Use `/stats` to see your progress over time

### Searching Effectively
```
/search travel        # Find all travel-related memories
/search beginner      # Find memories about your level
/search prefer        # Find your preferences
/search food          # Find topic-specific memories
```

### When to Use `/add` vs. Chatting
**Use `/add` when:**
- You want to store a fact without conversation
- You're setting explicit preferences
- You're correcting the tutor's understanding

**Use natural chat when:**
- You're practicing the language
- You're having a conversation
- Facts emerge naturally

### Managing Memory Clutter
If you have too many memories:
1. `/stats` - Check count
2. `/memories` - Review all
3. `/forget [num]` - Remove duplicates or old ones
4. Or `/clear` and start fresh with `/import` of curated backup

---

## Keyboard Shortcuts

While there are no built-in shortcuts, you can use these shell techniques:

**Up Arrow** - Recall previous command
**Ctrl+C** - Cancel current input (doesn't exit)
**Ctrl+D** or `exit` - Exit the tutor

---

## Error Messages

| Message | Meaning | Solution |
|---------|---------|----------|
| `⚠️ Invalid index` | Memory number doesn't exist | Run `/memories` first to see valid numbers |
| `⚠️ Usage: /search [query]` | No search term provided | Include a search term: `/search travel` |
| `⚠️ File not found` | Import file doesn't exist | Check filename and path |
| `⚠️ No memories to export` | You have no memories yet | Chat first to create some memories |

---

## Quick Reference Card

```
📖 MEMORY COMMANDS
  /memories          List all
  /search [query]    Search
  /stats             Statistics
  /add [text]        Add manually
  /forget [num]      Delete one
  /clear             Delete all

💾 DATA COMMANDS
  /export            Save to file
  /import [file]     Load from file

⚙️ GENERAL
  /help              Show help
  exit               Quit
```

---

**Print this reference and keep it handy!** 📋
