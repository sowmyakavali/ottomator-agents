# Integration Guide: @growgraph/ontocast with watsonx

This guide explains how to integrate the watsonx OnToCast agent with the @growgraph/ontocast project.

## Overview

The `@growgraph/ontocast` project can now be executed using IBM watsonx.ai LLM models through this custom agent implementation. This integration provides:

- **Enterprise-grade AI**: IBM watsonx.ai foundation models
- **Multiple Model Options**: Llama, Granite, Mixtral models
- **Scalable Deployment**: Docker and cloud-ready
- **Conversation Memory**: Persistent chat history
- **Live Agent Studio Compatible**: Ready for production

## Quick Start

### 1. Set Up watsonx.ai Credentials

First, get your IBM watsonx.ai credentials:

1. Visit [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/)
2. Create a project or use existing one
3. Go to **Manage** > **Access (IAM)** > **API keys** to create an API key
4. Note your project ID from project settings

### 2. Configure the Agent

Run the interactive setup:

```bash
cd watsonx-ontocast-agent
python setup.py
```

Or manually create `.env` file:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Install and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent
uvicorn watsonx_ontocast_agent:app --host 0.0.0.0 --port 8001
```

### 4. Test the Integration

```bash
curl -X POST http://localhost:8001/api/watsonx-ontocast-agent \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello from @growgraph/ontocast! How can you help?",
    "user_id": "growgraph_user",
    "request_id": "ontocast_001",
    "session_id": "growgraph_session"
  }'
```

## Integration Patterns

### Pattern 1: Direct API Integration

Your `@growgraph/ontocast` application can directly call the watsonx agent:

```javascript
// Example JavaScript integration
const response = await fetch('http://localhost:8001/api/watsonx-ontocast-agent', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: userInput,
    user_id: userId,
    request_id: generateRequestId(),
    session_id: sessionId
  })
});
```

### Pattern 2: Docker Compose Integration

```yaml
# docker-compose.yml
version: '3.8'
services:
  watsonx-agent:
    build: ./watsonx-ontocast-agent
    ports:
      - "8001:8001"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - API_BEARER_TOKEN=${API_BEARER_TOKEN}
    
  your-ontocast-app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - watsonx-agent
    environment:
      - WATSONX_AGENT_URL=http://watsonx-agent:8001
```

### Pattern 3: Live Agent Studio Integration

1. Upload the `studio-integration-version` files to Live Agent Studio
2. Configure environment variables in the studio
3. Set the endpoint to: `watsonx-ontocast-agent`
4. Your @growgraph/ontocast can now use the studio's API

## Model Selection Guide

Choose the right watsonx model for your @growgraph/ontocast use case:

### For General Purpose Chatbots
- **Recommended**: `meta-llama/llama-3-1-8b-instruct`
- **Reason**: Good balance of performance and speed

### For Complex Reasoning Tasks
- **Recommended**: `meta-llama/llama-3-1-70b-instruct`
- **Reason**: Best reasoning capabilities, larger context

### For Enterprise Applications
- **Recommended**: `ibm/granite-3-8b-instruct`
- **Reason**: IBM's enterprise-optimized model with better compliance

### For Lightweight Applications
- **Recommended**: `ibm/granite-3-2b-instruct`
- **Reason**: Fastest response times, minimal resource usage

### For Multilingual Support
- **Recommended**: `mistralai/mixtral-8x7b-instruct-v01`
- **Reason**: Excellent multilingual capabilities

## Environment Configuration

### Required Variables
```bash
WATSONX_API_KEY=your-api-key-here
WATSONX_PROJECT_ID=your-project-id
WATSONX_MODEL=meta-llama/llama-3-1-70b-instruct
API_BEARER_TOKEN=your-secure-token
```

### Optional Database Variables (for conversation history)
```bash
# Option 1: Supabase
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key

# Option 2: PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## Deployment Options

### Development
```bash
uvicorn watsonx_ontocast_agent:app --reload --port 8001
```

### Production
```bash
# Docker
docker build -t ontocast-watsonx .
docker run -d -p 8001:8001 --env-file .env ontocast-watsonx

# Or with gunicorn for better performance
gunicorn -w 4 -k uvicorn.workers.UvicornWorker watsonx_ontocast_agent:app --bind 0.0.0.0:8001
```

### Cloud Deployment (Example: AWS)
```bash
# Build and push to ECR
aws ecr create-repository --repository-name ontocast-watsonx
docker tag ontocast-watsonx:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ontocast-watsonx:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ontocast-watsonx:latest

# Deploy with ECS or EKS
```

## Monitoring and Debugging

### Health Check
```bash
curl http://localhost:8001/api/health
```

### Check Available Models
```bash
curl http://localhost:8001/api/models
```

### Debug Mode
Set `LOG_LEVEL=DEBUG` in your environment for detailed logging.

## Performance Optimization

### For High Traffic
1. Use multiple worker processes: `gunicorn -w 8`
2. Implement caching for frequent queries
3. Use connection pooling for database

### For Low Latency
1. Choose smaller models (Granite 3 2B)
2. Reduce `MAX_NEW_TOKENS` parameter
3. Use local database instead of remote

### For Cost Optimization
1. Implement request batching
2. Cache frequent responses
3. Use smaller models when appropriate

## Security Considerations

### API Security
- Always use HTTPS in production
- Rotate bearer tokens regularly
- Implement rate limiting

### Credential Management
- Never commit credentials to version control
- Use environment variables or secrets management
- Rotate API keys periodically

### Network Security
- Use VPCs for cloud deployments
- Implement firewall rules
- Monitor API usage

## Troubleshooting

### Common Issues

**Issue**: "Failed to initialize watsonx model"
**Solution**: Check your API key and project ID

**Issue**: "Connection timeout"
**Solution**: Verify watsonx.ai URL and network connectivity

**Issue**: "Database connection failed"
**Solution**: Check database credentials and ensure tables exist

**Issue**: "Authentication failed"
**Solution**: Verify bearer token matches environment variable

### Support

For issues specific to this integration:
1. Check the logs in the container/process
2. Verify environment variables are set correctly
3. Test individual components (watsonx connection, database connection)
4. Review the example scripts for correct usage patterns

## Migration from Other LLMs

If you're migrating from OpenAI or other providers:

1. **API Format**: The request/response format is similar to OpenAI
2. **Model Names**: Use watsonx model identifiers instead
3. **Authentication**: Use IBM API keys instead of OpenAI keys
4. **Parameters**: Some model parameters may differ

## Contributing

To extend this integration:
1. Fork the repository
2. Add new features to the agent
3. Update documentation
4. Submit a pull request

This integration provides a complete bridge between @growgraph/ontocast and IBM watsonx.ai, enabling enterprise-grade AI capabilities with minimal code changes.