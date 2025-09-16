# Mem0 Agent - Memory-Powered AI Assistant with Watson AI

This project demonstrates how to build an AI assistant with memory capabilities using the Mem0 library, IBM Watson AI, and Supabase for authentication and vector storage.

The Live Agent Studio integration verison referenced below also shows how to integrate Mem0 with a Pydantic AI agent.

## Features

- **🧠 Long-term Memory**: The AI remembers past conversations and preferences
- **🔒 Secure Authentication**: User data is protected with Supabase authentication
- **💬 Personalized Responses**: Get responses tailored to your history and context
- **🌐 Streamlit Interface**: Easy-to-use web interface for chatting with the AI
- **🤖 Watson AI Integration**: Powered by IBM Watson AI models for reliable responses

## Project Structure

This repository contains multiple implementations of the Mem0 agent:

1. **Basic Watson AI Implementation** (`iterations/v1-basic-mem0.py`): Pure Watson AI implementation (requires Mem0 IBM provider support)
2. **Hybrid Implementation** (`iterations/v1-hybrid-mem0.py`): Uses OpenAI for memory embeddings and Watson AI for text generation (recommended)
3. **Supabase Integration** (`iterations/v2-supabase-mem0.py`): Enhanced implementation with Supabase vector storage
4. **Streamlit Web Interface** (`iterations/v3-streamlit-supabase-mem0.py`): Web application with Supabase authentication
5. **Live Agent Studio Integration** (`studio-integration-version/`): Code for integrating with Live Agent Studio

**Note**: If you encounter issues with Mem0's IBM provider support, use the hybrid implementation (`v1-hybrid-mem0.py`) which is more reliable.

The `studio-integration-version` folder contains the code used to integrate this agent into the Live Agent Studio, including:
- API endpoint setup
- Database integration
- Authentication handling
- Message history management

## Prerequisites

- Python 3.11+
- IBM Watson AI API key and project ID
- Supabase account and project

## Setup Instructions

1. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Copy the `.env.example` file to `.env` and fill in your API keys:
   
   **For Pure Watson AI approach:**
   - `WATSONX_API_KEY`: Your IBM Watson AI API key
   - `WATSONX_PROJECT_ID`: Your Watson AI project ID  
   - `WATSONX_URL`: Your Watson AI service URL (defaults to https://us-south.ml.cloud.ibm.com)
   - `MODEL_CHOICE`: The Watson AI model to use (defaults to ibm/granite-13b-chat-v2)
   
   **For Hybrid approach (recommended):**
   - All Watson AI variables above, plus:
   - `OPENAI_API_KEY`: Your OpenAI API key (for memory embeddings)
   
   **For Supabase versions:**
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase service role key

4. **Run the application**:
   ```bash
   # For hybrid approach (recommended)
   python iterations/v1-hybrid-mem0.py
   
   # For pure Watson AI (if Mem0 supports IBM provider)
   python iterations/v1-basic-mem0.py
   
   # For Streamlit interface
   streamlit run iterations/v3-streamlit-supabase-mem0.py
   ```

## Watson AI Setup

1. Create an IBM Watson AI account at [IBM Cloud](https://cloud.ibm.com/)
2. Create a Watson Studio project and get your project ID
3. Get your API key from IBM Cloud Identity and Access Management (IAM)
4. Choose your service region (default is us-south)

## Supabase Setup

1. Create a Supabase account and project at [supabase.com](https://supabase.com)
2. Get your Database URL from: Project Settings > Database
3. Get your API keys from: Project Settings > API

## How It Works

The application uses:
- **Mem0**: For memory management and retrieval
- **IBM Watson AI**: For generating AI responses
- **Supabase**: For authentication and vector storage
- **Streamlit**: For the web interface

When a user sends a message, the system:
1. Retrieves relevant memories based on the query
2. Includes these memories in the prompt to Watson AI
3. Stores the conversation as a new memory
4. Displays the response to the user

## Studio Integration

The `studio-integration-version` folder contains everything needed to deploy this agent to the Live Agent Studio:

- `mem0_agent.py`: Core agent implementation
- `mem0_agent_endpoint.py`: FastAPI endpoint for the agent
- `Dockerfile`: Container configuration for deployment
- `.env.example`: Template for required environment variables

## Troubleshooting

1. **Authentication Issues**:
   - Verify your Supabase credentials are correctly set in the `.env` file
   - Check if your Supabase project has Email Auth enabled

2. **Database Connection Issues**:
   - Verify your DATABASE_URL is correctly formatted
   - Make sure you aren't using special characters in your database password. See the note in `.env.example`.

3. **Watson AI Issues**:
   - Verify your WATSONX_API_KEY is correctly set in the `.env` file
   - Check if your WATSONX_PROJECT_ID is valid
   - Ensure your Watson AI service region (WATSONX_URL) is correct
   - Make sure your Watson AI account has access to the model you're trying to use
