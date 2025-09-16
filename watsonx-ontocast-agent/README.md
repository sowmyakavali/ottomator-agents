# watsonx OnToCast Agent

Author: [AI Assistant](https://ottomator.ai)

This is a Python FastAPI agent that integrates with IBM watsonx.ai LLM models for the Live Agent Studio platform. It demonstrates how to use watsonx foundation models for AI-powered conversational agents.

## Overview

This agent provides:
- Integration with IBM watsonx.ai foundation models
- Natural language processing using watsonx LLMs
- Conversation history management
- Secure authentication
- Database storage for chat sessions
- Support for multiple watsonx model types

## Prerequisites

- Python 3.11 or higher
- IBM watsonx.ai account and API credentials
- PostgreSQL database or Supabase account
- Basic understanding of FastAPI and async Python

## Supported watsonx Models

This agent supports various IBM watsonx foundation models including:
- `meta-llama/llama-3-1-70b-instruct`
- `meta-llama/llama-3-1-8b-instruct`
- `ibm/granite-3-8b-instruct`
- `ibm/granite-3-2b-instruct`
- `mistralai/mixtral-8x7b-instruct-v01`

## Setup

1. **Clone Repository**
   ```bash
   cd ottomator-agents/watsonx-ontocast-agent
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   
   Required environment variables in `.env` file:
   ```plaintext
   # watsonx.ai Configuration
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_PROJECT_ID=your-project-id
   WATSONX_API_KEY=your-api-key
   WATSONX_MODEL=meta-llama/llama-3-1-70b-instruct
   
   # Database Configuration (choose one)
   # For Supabase:
   SUPABASE_URL=your-project-url
   SUPABASE_SERVICE_KEY=your-service-key
   
   # For PostgreSQL:
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   
   # Authentication
   API_BEARER_TOKEN=your-token-here
   ```

3. **Create Database Tables**
   ```sql
   CREATE EXTENSION IF NOT EXISTS pgcrypto;
   
   CREATE TABLE messages (
       id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
       session_id TEXT NOT NULL,
       message JSONB NOT NULL
   );
   
   CREATE INDEX idx_messages_session_id ON messages(session_id);
   CREATE INDEX idx_messages_created_at ON messages(created_at);
   ```

## Quick Start

### Option 1: Automated Setup (Recommended)

Run the interactive setup script:
```bash
python setup.py
```

This will guide you through:
- Configuring watsonx.ai credentials
- Setting up database connections
- Creating configuration files
- Testing the connection

### Option 2: Manual Setup

1. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Database** (optional, for conversation history)
   ```sql
   -- Run this in your PostgreSQL/Supabase database
   CREATE EXTENSION IF NOT EXISTS pgcrypto;
   CREATE TABLE messages (
       id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
       session_id TEXT NOT NULL,
       message JSONB NOT NULL
   );
   ```

## Running the Agent

### Standalone Agent
```bash
python studio-integration-version/watsonx_ontocast_agent.py
```

### API Server
```bash
uvicorn watsonx_ontocast_agent:app --host 0.0.0.0 --port 8001
```

### Docker Deployment

1. Build the agent:
```bash
docker build -t watsonx-ontocast-agent .
```

2. Run the container:
```bash
docker run -d --name watsonx-ontocast-agent -p 8001:8001 --env-file .env watsonx-ontocast-agent
```

## Example Usage & Testing

### Interactive Demo
```bash
python example.py
```

This will show you:
- How to use the standalone agent
- API request examples
- Configuration options
- Deployment methods
- Testing scenarios

### API Testing
```bash
curl -X POST http://localhost:8001/api/watsonx-ontocast-agent \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is IBM watsonx.ai?",
    "user_id": "test-user",
    "request_id": "test-request-1",
    "session_id": "test-session-1"
  }'
```

### Health Check
```bash
curl http://localhost:8001/api/health
```

### Available Models
```bash
curl http://localhost:8001/api/models
```

## watsonx.ai Configuration

### Getting watsonx Credentials

1. Sign up for IBM watsonx.ai at https://dataplatform.cloud.ibm.com/
2. Create a new project
3. Go to "Manage" > "Access (IAM)" > "API keys" to create an API key
4. Find your project ID in the project settings

### Model Selection

You can change the model by updating the `WATSONX_MODEL` environment variable to any supported foundation model. Popular choices include:

- **Llama 3.1 70B**: Best for complex reasoning and large context
- **Llama 3.1 8B**: Good balance of performance and speed
- **Granite 3 8B**: IBM's own model, optimized for enterprise use
- **Mixtral 8x7B**: Excellent for multilingual tasks

## Features

- **Multi-model Support**: Easy switching between different watsonx models
- **Conversation Management**: Persistent chat history across sessions
- **Error Handling**: Robust error handling for API failures
- **Authentication**: Secure bearer token authentication
- **Scalable**: Built with async FastAPI for high performance
- **Dockerized**: Ready for containerized deployment
- **Live Agent Studio Ready**: Optimized for the Live Agent Studio platform
- **Flexible Database**: Supports both Supabase and PostgreSQL
- **Easy Setup**: Interactive configuration script included

## File Structure

```
watsonx-ontocast-agent/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                      # Environment variables template
├── Dockerfile                        # Docker configuration
├── .dockerignore                     # Docker ignore file
├── setup.py                         # Interactive setup script
├── example.py                       # Usage examples and demos
├── watsonx_ontocast_agent.py        # Main agent (PostgreSQL version)
├── watsonx_ontocast_agent_supabase.py # Supabase version
└── studio-integration-version/      # Live Agent Studio compatible version
    ├── requirements.txt
    ├── watsonx_ontocast_agent.py     # Standalone agent class
    └── watsonx_ontocast_agent_endpoint.py # Studio API endpoint
```

## Contributing

This agent is part of the oTTomator agents collection. For contributions or issues, please refer to the main repository guidelines.

## License

This project is licensed under the same terms as the main ottomator-agents repository.