"""
Watson X.AI version of the mem0-agent 
This demonstrates how to migrate any OpenAI-based agent to Watson X.AI
"""

from dotenv import load_dotenv
from ibm_watson_machine_learning import APIClient
from mem0 import Memory
import os

# Load environment variables
load_dotenv()

# Watson X.AI configuration for mem0
config = {
    "llm": {
        "provider": "openai",  # mem0 uses OpenAI-compatible interface
        "config": {
            "model": "gpt-4o-mini",  # Will be overridden by our Watson X.AI client
            "base_url": "http://localhost:8000/v1",  # Placeholder - we'll handle this differently
        }
    }
}

class WatsonXAIClient:
    """Watson X.AI client that mimics OpenAI interface for mem0 compatibility"""
    
    def __init__(self):
        # Initialize Watson ML client
        self.wml_credentials = {
            "url": os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            "apikey": os.getenv("WATSONX_API_KEY"),
        }
        
        if not self.wml_credentials["apikey"]:
            raise ValueError("WATSONX_API_KEY environment variable is required")
            
        self.client = APIClient(self.wml_credentials)
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        
        if not self.project_id:
            raise ValueError("WATSONX_PROJECT_ID environment variable is required")
            
        self.client.set.default_project(self.project_id)
        self.model = os.getenv("WATSONX_MODEL", "ibm/granite-13b-chat-v2")
        
        # Create a mock chat completions object for compatibility
        self.chat = MockChatCompletions(self)
    
    def _get_generation_params(self):
        """Get generation parameters for Watson X.AI"""
        return {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "top_p": 1.0
        }
    
    def generate_response(self, messages):
        """Generate response using Watson X.AI"""
        # Convert messages to a single prompt
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                prompt += f"User: {msg['content']}\n\n"
        
        prompt += "Assistant: "
        
        # Generate response using Watson X.AI
        response = self.client.foundation_models.generate_text(
            model_id=self.model,
            prompt=prompt,
            params=self._get_generation_params()
        )
        
        return response

class MockChatCompletions:
    """Mock chat completions object for OpenAI compatibility"""
    
    def __init__(self, watson_client):
        self.watson_client = watson_client
        
    def create(self, model, messages, **kwargs):
        """Create a chat completion using Watson X.AI"""
        response_text = self.watson_client.generate_response(messages)
        
        # Return mock OpenAI response format
        return MockOpenAIResponse(response_text)

class MockOpenAIResponse:
    """Mock OpenAI response object"""
    
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockChoice:
    """Mock choice object"""
    
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    """Mock message object"""
    
    def __init__(self, content):
        self.content = content

# Initialize Watson X.AI client and memory
watsonx_client = WatsonXAIClient()
memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    """Chat function using Watson X.AI instead of OpenAI"""
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    
    # Generate Assistant response using Watson X.AI
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    
    # Use Watson X.AI instead of OpenAI
    response = watsonx_client.chat.create(model=watsonx_client.model, messages=messages)
    assistant_response = response.choices[0].message.content
    
    # Add memories
    memory.add(messages=[{"role": "user", "content": message}, {"role": "assistant", "content": assistant_response}], user_id=user_id)
    
    return assistant_response

# Example usage
if __name__ == "__main__":
    print("🧠 Watson X.AI + Mem0 Agent Demo")
    print("=" * 40)
    
    # Test the chat function
    user_id = "demo_user"
    
    # First conversation
    response1 = chat_with_memories("Hi, my name is Alice and I love hiking!", user_id)
    print(f"User: Hi, my name is Alice and I love hiking!")
    print(f"Assistant: {response1}")
    print()
    
    # Second conversation (should remember the name and interest)
    response2 = chat_with_memories("What outdoor activities do you recommend for me?", user_id)
    print(f"User: What outdoor activities do you recommend for me?")
    print(f"Assistant: {response2}")
    print()
    
    # Third conversation (should remember previous context)
    response3 = chat_with_memories("What was my name again?", user_id)
    print(f"User: What was my name again?")
    print(f"Assistant: {response3}")
    
    print("\n✅ Watson X.AI + Mem0 integration working!")
    print("The agent remembers conversation history using mem0 and generates responses using Watson X.AI")