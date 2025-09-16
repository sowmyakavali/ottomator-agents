"""
watsonx OnToCast Agent - Standalone Version

This is a standalone implementation of the watsonx OnToCast agent that can be run
independently or integrated into other applications.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# IBM watsonx.ai imports
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials

# Supabase imports
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class WatsonxOnToCastAgent:
    """Standalone watsonx OnToCast agent implementation."""
    
    def __init__(self):
        """Initialize the agent with watsonx and Supabase connections."""
        self.model = None
        self.supabase = None
        self._initialize_watsonx()
        self._initialize_supabase()
    
    def _initialize_watsonx(self):
        """Initialize the watsonx.ai model with credentials."""
        try:
            # Get credentials from environment
            api_key = os.getenv("WATSONX_API_KEY")
            project_id = os.getenv("WATSONX_PROJECT_ID")
            url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
            model_id = os.getenv("WATSONX_MODEL", "meta-llama/llama-3-1-70b-instruct")
            
            if not api_key or not project_id:
                raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set")
            
            # Set up credentials
            credentials = Credentials(
                url=url,
                api_key=api_key
            )
            
            # Initialize model with optimized parameters
            self.model = Model(
                model_id=model_id,
                params={
                    GenParams.DECODING_METHOD: "greedy",
                    GenParams.MAX_NEW_TOKENS: 800,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_P: 0.9,
                    GenParams.TOP_K: 50,
                    GenParams.REPETITION_PENALTY: 1.1
                },
                credentials=credentials,
                project_id=project_id
            )
            
            print(f"✅ Initialized watsonx.ai with model: {model_id}")
            
        except Exception as e:
            print(f"❌ Failed to initialize watsonx model: {str(e)}")
            raise
    
    def _initialize_supabase(self):
        """Initialize Supabase client."""
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_KEY")
            
            if url and key:
                self.supabase = create_client(url, key)
                print("✅ Initialized Supabase connection")
            else:
                print("⚠️  Supabase credentials not found - conversation history will not be persisted")
        except Exception as e:
            print(f"❌ Failed to initialize Supabase: {str(e)}")
    
    async def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch the most recent conversation history for a session."""
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table("messages").select("*").eq("session_id", session_id).order("created_at", desc=True).limit(limit).execute()
            messages = result.data[::-1] if result.data else []
            return messages
        except Exception as e:
            print(f"Error fetching conversation history: {str(e)}")
            return []
    
    async def store_message(self, session_id: str, message_type: str, content: str, data: Optional[Dict] = None):
        """Store a message in the messages table."""
        if not self.supabase:
            return
        
        message_obj = {
            "type": message_type,
            "content": content
        }
        if data:
            message_obj["data"] = data

        try:
            self.supabase.table("messages").insert({
                "session_id": session_id,
                "message": message_obj
            }).execute()
        except Exception as e:
            print(f"Error storing message: {str(e)}")
    
    def _format_conversation_for_watsonx(self, messages: List[Dict], current_query: str) -> str:
        """Format conversation history for watsonx.ai model."""
        conversation_text = ""
        
        for msg in messages:
            msg_data = msg.get("message", {})
            msg_type = msg_data.get("type", "")
            msg_content = msg_data.get("content", "")
            
            if msg_type == "human":
                conversation_text += f"Human: {msg_content}\n"
            elif msg_type == "assistant":
                conversation_text += f"Assistant: {msg_content}\n"
        
        conversation_text += f"Human: {current_query}\nAssistant:"
        
        return conversation_text
    
    async def generate_response(self, query: str, session_id: str = None) -> str:
        """Generate a response using watsonx.ai."""
        try:
            # Get conversation history if session_id is provided
            conversation_history = []
            if session_id:
                conversation_history = await self.get_conversation_history(session_id)
                # Store user's query
                await self.store_message(session_id, "human", query)
            
            # Format conversation for watsonx
            conversation_text = self._format_conversation_for_watsonx(conversation_history, query)
            
            # Create system prompt
            system_prompt = """You are OnToCast, an intelligent AI assistant powered by IBM watsonx.ai. You are designed to help users with a wide variety of tasks including:

- Answering questions and providing accurate information
- Helping with research and analysis
- Assisting with creative writing and content creation
- Providing explanations and educational content
- Problem-solving and strategic thinking
- Technical assistance and coding help
- General conversation and support

Key characteristics:
- Be helpful, accurate, and engaging
- Provide clear and concise responses
- When you don't know something, say so honestly
- Use your knowledge to provide comprehensive answers
- Be friendly and professional in your tone

"""
            
            full_prompt = system_prompt + conversation_text
            
            # Generate response
            response = self.model.generate_text(prompt=full_prompt)
            
            # Clean up the response
            if isinstance(response, str):
                cleaned_response = response.strip()
            else:
                cleaned_response = str(response).strip()
            
            # Remove any potential prompt leakage
            if cleaned_response.startswith("Assistant:"):
                cleaned_response = cleaned_response[10:].strip()
            
            # Store agent's response if session_id is provided
            if session_id:
                await self.store_message(session_id, "assistant", cleaned_response)
            
            return cleaned_response
            
        except Exception as e:
            error_msg = f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"
            if session_id:
                await self.store_message(session_id, "assistant", error_msg)
            return error_msg
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current watsonx model."""
        return {
            "model_id": os.getenv("WATSONX_MODEL", "meta-llama/llama-3-1-70b-instruct"),
            "watsonx_url": os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            "project_id": os.getenv("WATSONX_PROJECT_ID", "not_set"),
            "supabase_connected": self.supabase is not None
        }

# Example usage function
async def example_usage():
    """Example of how to use the WatsonxOnToCastAgent."""
    agent = WatsonxOnToCastAgent()
    
    print("🤖 watsonx OnToCast Agent initialized!")
    print(f"📋 Model info: {agent.get_model_info()}")
    
    # Example conversation
    session_id = "example_session_123"
    
    queries = [
        "Hello! What is IBM watsonx.ai?",
        "How does it compare to other AI platforms?",
        "Can you help me understand foundation models?"
    ]
    
    for query in queries:
        print(f"\n👤 User: {query}")
        response = await agent.generate_response(query, session_id)
        print(f"🤖 OnToCast: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())