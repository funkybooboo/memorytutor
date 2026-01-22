import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

load_dotenv()

# EXPERIENTIAL LAYER: Memory Configuration
# We use an explicit collection name and path to ensure persistence. 
# In a real product, naming your collection prevents data "leaks" 
# between different AI agents running on the same machine.
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": ".qdrant_data",
            "collection_name": "spanish_tutor_session",
            "on_disk": True,
        }
    }
}

client = OpenAI()
memory = Memory.from_config(config)
USER_ID = "beau_student_01"

# A helper to map simple user-friendly numbers to complex database UUIDs
memory_map = {}

def handle_chat():
    global memory
    global memory_map
    
    print("\n" + "="*45)
    print("🇪🇸  PERSONALIZED AI SPANISH TUTOR")
    print("Status: Memory Persistent | Storage: Local Disk")
    print("Commands: /memories, /forget [num], exit")
    print("="*45 + "\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input: continue
            if user_input.lower() in ['exit', 'quit']: break

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
                    full_id = memory_map.get(num)
                    if full_id:
                        memory.delete(full_id)
                        print(f"\n🗑️  Pruned memory {num}.\n")
                    else:
                        print("\n⚠️  Invalid index.\n")
                except (IndexError, ValueError):
                    print("\n⚠️  Use: /forget [number]\n")
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
                            "content": f"You are a Spanish Tutor. Personalize based on this context:\n{context}"
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
                print(f"⚠️  Error: {e}")

    finally:
        # Professional cleanup to prevent Qdrant race conditions
        del memory 
        os._exit(0)

if __name__ == "__main__":
    handle_chat()