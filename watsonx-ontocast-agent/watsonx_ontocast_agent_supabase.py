from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import sys
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

# Initialize FastAPI app
app = FastAPI()
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL and SUPABASE_SERVICE_KEY must be set"
        )
    
    return create_client(url, key)

# Request/Response Models
class AgentRequest(BaseModel):
    query: str
    user_id: str
    request_id: str
    session_id: str

class AgentResponse(BaseModel):
    success: bool

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verify the bearer token against environment variable."""
    expected_token = os.getenv("API_BEARER_TOKEN")
    if not expected_token:
        raise HTTPException(
            status_code=500,
            detail="API_BEARER_TOKEN environment variable not set"
        )
    if credentials.credentials != expected_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
    return True

def initialize_watsonx_model():
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
        
        # Initialize model
        model = Model(
            model_id=model_id,
            params={
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 1000,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 1,
                GenParams.TOP_K: 50,
                GenParams.REPETITION_PENALTY: 1.1
            },
            credentials=credentials,
            project_id=project_id
        )
        
        return model
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize watsonx model: {str(e)}"
        )

async def fetch_conversation_history(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch the most recent conversation history for a session using Supabase."""
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("messages").select("*").eq("session_id", session_id).order("created_at", desc=True).limit(limit).execute()
        
        # Convert to list and reverse to get chronological order
        messages = result.data[::-1]
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversation history: {str(e)}")

async def store_message(session_id: str, message_type: str, content: str, data: Optional[Dict] = None):
    """Store a message in the messages table using Supabase."""
    message_obj = {
        "type": message_type,
        "content": content
    }
    if data:
        message_obj["data"] = data

    try:
        supabase = get_supabase_client()
        
        supabase.table("messages").insert({
            "session_id": session_id,
            "message": message_obj
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")

def format_conversation_for_watsonx(messages: List[Dict], current_query: str) -> str:
    """Format conversation history for watsonx.ai model."""
    conversation_text = ""
    
    for msg in messages:
        msg_data = msg["message"]
        msg_type = msg_data["type"]
        msg_content = msg_data["content"]
        
        if msg_type == "human":
            conversation_text += f"Human: {msg_content}\n"
        elif msg_type == "assistant":
            conversation_text += f"Assistant: {msg_content}\n"
    
    conversation_text += f"Human: {current_query}\nAssistant:"
    
    return conversation_text

async def get_watsonx_response(conversation_text: str) -> str:
    """Get response from watsonx.ai model."""
    try:
        model = initialize_watsonx_model()
        
        # Create a comprehensive prompt that includes context about the agent
        system_prompt = """You are OnToCast, an intelligent AI assistant powered by IBM watsonx.ai. You help users with various tasks including:

- Answering questions and providing information
- Helping with analysis and problem-solving
- Assisting with creative tasks
- Providing explanations and tutorials
- General conversation and support

Please provide helpful, accurate, and engaging responses. Be concise but thorough in your explanations.

"""
        
        full_prompt = system_prompt + conversation_text
        
        # Generate response
        response = model.generate_text(prompt=full_prompt)
        
        # Clean up the response
        if isinstance(response, str):
            return response.strip()
        else:
            return str(response).strip()
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get response from watsonx: {str(e)}"
        )

@app.post("/api/watsonx-ontocast-agent", response_model=AgentResponse)
async def watsonx_ontocast_agent(
    request: AgentRequest,
    authenticated: bool = Depends(verify_token)
):
    try:
        # Fetch conversation history from Supabase
        conversation_history = await fetch_conversation_history(request.session_id)
        
        # Store user's query
        await store_message(
            session_id=request.session_id,
            message_type="human",
            content=request.query
        )

        # Format conversation for watsonx
        conversation_text = format_conversation_for_watsonx(conversation_history, request.query)
        
        # Get response from watsonx
        agent_response = await get_watsonx_response(conversation_text)

        # Store agent's response
        await store_message(
            session_id=request.session_id,
            message_type="assistant",
            content=agent_response
        )

        return AgentResponse(success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "watsonx-ontocast-agent-supabase"}

@app.get("/api/models")
async def list_supported_models():
    """List supported watsonx models."""
    return {
        "supported_models": [
            "meta-llama/llama-3-1-70b-instruct",
            "meta-llama/llama-3-1-8b-instruct",
            "ibm/granite-3-8b-instruct",
            "ibm/granite-3-2b-instruct",
            "mistralai/mixtral-8x7b-instruct-v01"
        ],
        "current_model": os.getenv("WATSONX_MODEL", "meta-llama/llama-3-1-70b-instruct")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)