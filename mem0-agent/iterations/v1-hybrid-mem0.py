from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from mem0 import Memory
import os

# Load environment variables
load_dotenv()

# Watson AI configuration
credentials = {
    "url": os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
    "apikey": os.environ['WATSONX_API_KEY']
}

watsonx_client = APIClient(credentials)
project_id = os.environ['WATSONX_PROJECT_ID']

# Hybrid approach: Use OpenAI for embeddings/memory, Watson AI for generation
config = {
    "llm": {
        "provider": "openai",  # Keep OpenAI for memory embeddings
        "config": {
            "model": "gpt-3.5-turbo"  # Cheaper model for memory management
        }
    }
}

# Watson AI model for direct chat generation
model = Model(
    model_id=os.getenv('MODEL_CHOICE', 'ibm/granite-13b-chat-v2'),
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 512,
        "temperature": 0.7
    },
    credentials=credentials,
    project_id=project_id
)

# Memory instance for embeddings and retrieval
memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories using Mem0 (with OpenAI embeddings)
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    
    # Generate Assistant response using Watson AI
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
    
    response = model.generate_text(prompt=full_prompt)
    assistant_response = response['results'][0]['generated_text'].strip()

    # Store new memories using Mem0 (this will use OpenAI for embeddings)
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": message},
        {"role": "assistant", "content": assistant_response}
    ]
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    print("Note: Using hybrid approach - OpenAI for memory, Watson AI for generation")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()