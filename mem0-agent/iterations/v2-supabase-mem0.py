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

config = {
    "llm": {
        "provider": "ibm",
        "config": {
            "model": os.getenv('MODEL_CHOICE', 'ibm/granite-13b-chat-v2'),
            "url": os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
            "apikey": os.environ['WATSONX_API_KEY'],
            "project_id": os.environ['WATSONX_PROJECT_ID']
        }
    },
    "vector_store": {
        "provider": "supabase",
        "config": {
            "connection_string": os.environ['DATABASE_URL'],
            "collection_name": "memories"
        }
    }    
}

# Watson AI model for direct chat
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

memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    
    # Generate Assistant response using Watson AI
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
    
    response = model.generate_text(prompt=full_prompt)
    assistant_response = response['results'][0]['generated_text'].strip()

    # Create new memories from the conversation
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": message},
        {"role": "assistant", "content": assistant_response}
    ]
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()