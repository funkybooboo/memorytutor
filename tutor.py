import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

load_dotenv()

def validate_config():
    """Validate required environment variables are set."""
    mem0_mode = os.getenv("MEM0_MODE", "self-hosted")

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set in environment.")
        print("Please set it in your .env file or environment variables.")
        sys.exit(1)

    if mem0_mode == "hosted":
        if not os.getenv("MEM0_API_KEY"):
            print("ERROR: MEM0_API_KEY required for hosted mode.")
            print("Either set MEM0_API_KEY or change MEM0_MODE to 'self-hosted'.")
            sys.exit(1)

    return mem0_mode

def get_qdrant_config():
    """Returns Qdrant config based on whether running in Docker or locally."""
    use_docker = os.getenv("USE_DOCKER_QDRANT", "false").lower() == "true"

    if use_docker:
        return {
            "host": os.getenv("QDRANT_HOST", "qdrant"),
            "port": int(os.getenv("QDRANT_PORT", "6333")),
            "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "language_tutor_session"),
        }
    else:
        return {
            "path": os.getenv("QDRANT_PATH", ".qdrant_data"),
            "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "language_tutor_session"),
            "on_disk": True,
        }

def init_memory():
    """Initialize memory client based on MEM0_MODE."""
    mem0_mode = os.getenv("MEM0_MODE", "self-hosted")

    try:
        if mem0_mode == "hosted":
            from mem0 import MemoryClient
            return MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
        else:
            # EXPERIENTIAL LAYER: Memory Configuration
            # We use an explicit collection name and path to ensure persistence.
            # In a real product, naming your collection prevents data "leaks"
            # between different AI agents running on the same machine.
            config = {
                "vector_store": {
                    "provider": "qdrant",
                    "config": get_qdrant_config()
                }
            }
            return Memory.from_config(config)
    except Exception as e:
        print(f"\nERROR: Failed to initialize memory system: {e}")
        if mem0_mode == "self-hosted":
            print("Make sure Qdrant is accessible (check QDRANT_HOST and QDRANT_PORT).")
        sys.exit(1)

# Initialize configuration
mem0_mode = validate_config()
client = OpenAI()
memory = init_memory()
USER_ID = os.getenv("USER_ID", "default_student")
TUTOR_LANGUAGE = os.getenv("TUTOR_LANGUAGE", "Spanish")

# A helper to map simple user-friendly numbers to complex database UUIDs
memory_map = {}

def get_language_flag(language):
    """Return an appropriate flag emoji for the language."""
    flags = {
        "spanish": "🇪🇸",
        "french": "🇫🇷",
        "german": "🇩🇪",
        "italian": "🇮🇹",
        "portuguese": "🇵🇹",
        "chinese": "🇨🇳",
        "japanese": "🇯🇵",
        "korean": "🇰🇷",
        "russian": "🇷🇺",
        "arabic": "🇸🇦",
        "hindi": "🇮🇳",
        "english": "🇬🇧",
    }
    return flags.get(language.lower(), "🌍")

def check_first_run():
    """Check if this is the user's first run and display welcome message."""
    try:
        res = memory.get_all(user_id=USER_ID)
        all_memories = res.get('results', []) if isinstance(res, dict) else res
        return len(all_memories) == 0
    except:
        return True

def handle_chat():
    global memory
    global memory_map

    # Display banner with current configuration
    mode_display = "Hosted" if mem0_mode == "hosted" else "Self-Hosted"
    storage_display = "Mem0 Platform" if mem0_mode == "hosted" else (
        "Qdrant (Docker)" if os.getenv("USE_DOCKER_QDRANT", "false").lower() == "true" else "Qdrant (Local)"
    )

    flag = get_language_flag(TUTOR_LANGUAGE)

    print("\n" + "="*60)
    print(f"{flag}  PERSONALIZED AI {TUTOR_LANGUAGE.upper()} TUTOR")
    print(f"Status: Memory Persistent | Mode: {mode_display} | Storage: {storage_display}")
    print(f"User: {USER_ID}")
    print("Commands: /help for full list | exit to quit")
    print("="*60 + "\n")

    # Show first-run welcome message
    if check_first_run():
        print("👋 Welcome! This appears to be your first session.")
        print(f"I'm your personal {TUTOR_LANGUAGE} tutor with persistent memory.")
        print()
        print("💡 Quick Tips:")
        print(f"  • Start by telling me about yourself and your {TUTOR_LANGUAGE} learning goals")
        print("  • I'll remember everything across sessions")
        print("  • Use /help to see all commands")
        print("  • Use /memories to see what I know about you")
        print()
        print("Let's begin! Tell me about yourself...")
        print()

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input: continue
            if user_input.lower() in ['exit', 'quit']: break

            # HELP COMMAND
            if user_input == '/help':
                print("\n📖 AVAILABLE COMMANDS:")
                print("\n  Memory Management:")
                print("    /memories           - List all stored memories about you")
                print("    /search [query]     - Search for specific memories")
                print("    /forget [num]       - Delete a specific memory by number")
                print("    /clear              - Delete ALL memories (with confirmation)")
                print("    /add [text]         - Manually add a fact to memory")
                print("    /stats              - View memory statistics")
                print("\n  Data Management:")
                print("    /export             - Export memories to JSON file")
                print("    /import [file]      - Import memories from JSON file")
                print("\n  General:")
                print("    /help               - Show this help message")
                print("    exit or quit        - Exit the tutor")
                print("\n💡 TIPS:")
                print(f"  • Just chat naturally to practice {TUTOR_LANGUAGE}")
                print("  • The tutor remembers facts about you across sessions")
                print("  • Use /memories to see what the tutor knows about you")
                print("  • Use /search to find specific memories")
                print("-" * 60 + "\n")
                continue

            # STATS COMMAND
            if user_input == '/stats':
                try:
                    res = memory.get_all(user_id=USER_ID)
                    all_memories = res.get('results', []) if isinstance(res, dict) else res

                    print("\n📊 MEMORY STATISTICS:")
                    print(f"  Total memories: {len(all_memories)}")
                    print(f"  User ID: {USER_ID}")
                    print(f"  Language: {TUTOR_LANGUAGE}")
                    print(f"  Storage mode: {mem0_mode}")
                    if mem0_mode == "self-hosted":
                        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "language_tutor_session")
                        print(f"  Collection: {collection_name}")
                    print("-" * 50 + "\n")
                except Exception as e:
                    print(f"\n⚠️  Error retrieving stats: {e}\n")
                continue

            # SEARCH COMMAND
            if user_input.startswith('/search '):
                try:
                    query = user_input[8:].strip()
                    if not query:
                        print("\n⚠️  Usage: /search [query]\n")
                        continue

                    print(f"\n🔍 Searching for: '{query}'...")
                    search_results = memory.search(query, user_id=USER_ID)
                    actual_results = search_results.get('results', []) if isinstance(search_results, dict) else search_results

                    if not actual_results:
                        print("No matching memories found.\n")
                    else:
                        print(f"\n📋 SEARCH RESULTS ({len(actual_results)} found):")
                        for i, m in enumerate(actual_results, 1):
                            mem_text = m['memory'] if isinstance(m, dict) else m
                            print(f"{i}. {mem_text}")
                        print("-" * 50 + "\n")
                except Exception as e:
                    print(f"\n⚠️  Error searching: {e}\n")
                continue

            # ADD COMMAND
            if user_input.startswith('/add '):
                try:
                    fact = user_input[5:].strip()
                    if not fact:
                        print("\n⚠️  Usage: /add [fact to remember]\n")
                        continue

                    memory.add(fact, user_id=USER_ID)
                    print(f"\n✓ Added to memory: '{fact}'\n")
                except Exception as e:
                    print(f"\n⚠️  Error adding memory: {e}\n")
                continue

            # CLEAR COMMAND
            if user_input == '/clear':
                try:
                    res = memory.get_all(user_id=USER_ID)
                    all_memories = res.get('results', []) if isinstance(res, dict) else res

                    if not all_memories:
                        print("\n⚠️  No memories to clear.\n")
                        continue

                    print(f"\n⚠️  WARNING: This will delete ALL {len(all_memories)} memories!")
                    confirm = input("Type 'yes' to confirm: ").strip().lower()

                    if confirm == 'yes':
                        # Delete all memories
                        for m in all_memories:
                            mem_id = m.get('id') if isinstance(m, dict) else None
                            if mem_id:
                                memory.delete(mem_id)
                        print(f"\n✓ Cleared all memories ({len(all_memories)} deleted).\n")
                        memory_map = {}
                    else:
                        print("\n✓ Cancelled. No memories deleted.\n")
                except Exception as e:
                    print(f"\n⚠️  Error clearing memories: {e}\n")
                continue

            # EXPORT COMMAND
            if user_input == '/export':
                try:
                    import json
                    from datetime import datetime

                    res = memory.get_all(user_id=USER_ID)
                    all_memories = res.get('results', []) if isinstance(res, dict) else res

                    if not all_memories:
                        print("\n⚠️  No memories to export.\n")
                        continue

                    # Create export data
                    export_data = {
                        "user_id": USER_ID,
                        "language": TUTOR_LANGUAGE,
                        "export_date": datetime.now().isoformat(),
                        "total_memories": len(all_memories),
                        "memories": [
                            {
                                "text": m['memory'] if isinstance(m, dict) else str(m),
                                "id": m.get('id') if isinstance(m, dict) else None
                            }
                            for m in all_memories
                        ]
                    }

                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"memories_{USER_ID}_{timestamp}.json"

                    with open(filename, 'w') as f:
                        json.dump(export_data, f, indent=2)

                    print(f"\n✓ Exported {len(all_memories)} memories to: {filename}\n")
                except Exception as e:
                    print(f"\n⚠️  Error exporting memories: {e}\n")
                continue

            # IMPORT COMMAND
            if user_input.startswith('/import '):
                try:
                    import json

                    filename = user_input[8:].strip()
                    if not filename:
                        print("\n⚠️  Usage: /import [filename]\n")
                        continue

                    with open(filename, 'r') as f:
                        import_data = json.load(f)

                    memories_to_import = import_data.get('memories', [])

                    if not memories_to_import:
                        print("\n⚠️  No memories found in file.\n")
                        continue

                    print(f"\n📥 Found {len(memories_to_import)} memories in {filename}")
                    confirm = input("Import these memories? (yes/no): ").strip().lower()

                    if confirm == 'yes':
                        imported = 0
                        for mem in memories_to_import:
                            try:
                                memory.add(mem['text'], user_id=USER_ID)
                                imported += 1
                            except:
                                pass
                        print(f"\n✓ Imported {imported} memories.\n")
                    else:
                        print("\n✓ Import cancelled.\n")
                except FileNotFoundError:
                    print(f"\n⚠️  File not found: {filename}\n")
                except Exception as e:
                    print(f"\n⚠️  Error importing memories: {e}\n")
                continue

            # MEMORY OPERATION: LISTING (get_all)
            if user_input == '/memories':
                res = memory.get_all(user_id=USER_ID)
                all_memories = res.get('results', []) if isinstance(res, dict) else res
                
                print("\n🧠 KNOWLEDGE BASE:")
                if not all_memories:
                    print("(Empty)")
                else:
                    memory_map = {} 
                    for i, m in enumerate(all_memories, 1):
                        mem_text = m['memory'] if isinstance(m, dict) else m
                        mem_id = m.get('id') if isinstance(m, dict) else None
                        memory_map[str(i)] = mem_id
                        print(f"{i}. {mem_text}")
                print("-" * 25 + "\n")
                continue

            # MEMORY OPERATION: DELETING (delete)
            if user_input.startswith('/forget '):
                try:
                    num = user_input.split(' ')[1]

                    # Auto-fetch memories if map is empty
                    if not memory_map:
                        res = memory.get_all(user_id=USER_ID)
                        all_memories = res.get('results', []) if isinstance(res, dict) else res
                        memory_map = {}
                        for i, m in enumerate(all_memories, 1):
                            mem_id = m.get('id') if isinstance(m, dict) else None
                            memory_map[str(i)] = mem_id

                    full_id = memory_map.get(num)
                    if full_id:
                        memory.delete(full_id)
                        print(f"\n🗑️  Pruned memory {num}.\n")
                        # Clear map so it refreshes next time
                        memory_map = {}
                    else:
                        print(f"\n⚠️  Invalid index: {num}")
                        print("Run /memories first to see available memories.\n")
                except (IndexError, ValueError):
                    print("\n⚠️  Use: /forget [number]\n")
                except Exception as e:
                    print(f"\n⚠️  Error deleting memory: {e}\n")
                continue

            try:
                # MEMORY OPERATION: SEARCHING (search)
                # We pull facts relevant to the CURRENT question only.
                # This keeps the context window clean and cheap.
                search_results = memory.search(user_input, user_id=USER_ID)
                actual_results = search_results.get('results', []) if isinstance(search_results, dict) else search_results
                context = "\n".join([m['memory'] if isinstance(m, dict) else m for m in actual_results])

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a {TUTOR_LANGUAGE} language tutor. Help the user learn {TUTOR_LANGUAGE}. Personalize your teaching based on this context about the user:\n{context}"
                        },
                        {"role": "user", "content": user_input}
                    ]
                )

                reply = response.choices[0].message.content
                print(f"\nAI: {reply}\n")

                # MEMORY OPERATION: ADDING (add)
                # Mem0 automatically extracts the core "facts" from the conversation.
                memory.add(user_input, user_id=USER_ID)

            except Exception as e:
                error_msg = str(e)
                if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                    print(f"\n⚠️  Authentication Error: Invalid API key.")
                    print("Please check your OPENAI_API_KEY in .env file.\n")
                elif "connection" in error_msg.lower() or "refused" in error_msg.lower():
                    print(f"\n⚠️  Connection Error: Could not connect to service.")
                    if mem0_mode == "self-hosted":
                        print("Make sure Qdrant is running and accessible.\n")
                    else:
                        print("Check your internet connection and Mem0 service status.\n")
                else:
                    print(f"\n⚠️  Error: {error_msg}\n")

    finally:
        # Professional cleanup to prevent Qdrant race conditions
        if 'memory' in globals():
            del memory
        sys.exit(0)

if __name__ == "__main__":
    handle_chat()