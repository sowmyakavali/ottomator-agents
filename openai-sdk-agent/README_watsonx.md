# Watson X.AI Agents SDK Demo

This repository contains examples of using Watson X.AI (IBM Watson Machine Learning) to build intelligent travel planning agents with progressively advanced capabilities, as an alternative to OpenAI.

## Project Structure

### Watson X.AI Versions
- `v1_basic_agent_watsonx.py` - A simple agent example that generates a haiku about recursion
- `v2_structured_output_watsonx.py` - Travel agent with structured output using Pydantic models
- `v3_tool_calls_watsonx.py` - Travel agent with tool calls for weather forecasting
- `watson_agents.py` - Watson X.AI wrapper that provides OpenAI SDK-compatible interface

### Original OpenAI Versions (for comparison)
- `v1_basic_agent.py` - Original OpenAI version
- `v2_structured_output.py` - Original OpenAI version
- `v3_tool_calls.py` - Original OpenAI version
- (Additional OpenAI versions: v4_handoffs.py, v5_guardrails_and_context.py, v6_streamlit_agent.py)

## Watson X.AI Setup

### 1. Install Dependencies

```bash
pip install -r requirements_watsonx.txt
```

### 2. Watson X.AI Credentials Setup

1. **Get Watson X.AI Access**: Sign up for IBM Cloud and access Watson Machine Learning
2. **Create a Project**: Create a new project in Watson Studio
3. **Get API Key**: Generate an API key from IBM Cloud IAM
4. **Get Project ID**: Find your project ID in Watson Studio

### 3. Environment Configuration

Create a `.env` file with your Watson X.AI credentials:

```bash
cp .env.watsonx.example .env
```

Then edit `.env` with your actual credentials:

```
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-chat-v2
```

## Running the Watson X.AI Examples

### Basic Agent (Watson X.AI v1)

Run the basic Watson X.AI agent example:

```bash
python v1_basic_agent_watsonx.py
```

This will execute a simple agent that generates a haiku about recursion using Watson X.AI.

### Structured Output Agent (Watson X.AI v2)

Run the structured output travel agent example:

```bash
python v2_structured_output_watsonx.py
```

This demonstrates using Pydantic models to create structured travel plans with destinations, activities, and budget information using Watson X.AI.

### Tool Calls Agent (Watson X.AI v3)

Run the tool calls travel agent example:

```bash
python v3_tool_calls_watsonx.py
```

This version adds a weather forecasting tool to provide weather information for travel destinations using Watson X.AI.

## Watson X.AI Environment Variables

The following environment variables can be configured in your `.env` file:

- `WATSONX_API_KEY` (required): Your Watson X.AI API key from IBM Cloud
- `WATSONX_PROJECT_ID` (required): Your Watson Studio project ID
- `WATSONX_URL` (optional): The Watson X.AI service URL (default: US South)
- `WATSONX_MODEL` (optional): The Watson X.AI model to use (default: ibm/granite-13b-chat-v2)

## Available Watson X.AI Models

Watson X.AI provides access to various foundation models:

### IBM Granite Models
- `ibm/granite-13b-chat-v2` - IBM's enterprise-focused chat model
- `ibm/granite-20b-multilingual` - Multilingual model

### Meta Llama Models  
- `meta-llama/llama-2-70b-chat` - Large Llama 2 chat model
- `meta-llama/llama-2-13b-chat` - Medium Llama 2 chat model

### Other Models
- Check Watson X.AI documentation for the latest available models

## Key Differences from OpenAI

### 1. Authentication
- **OpenAI**: Uses `OPENAI_API_KEY`
- **Watson X.AI**: Uses `WATSONX_API_KEY` + `WATSONX_PROJECT_ID`

### 2. Model Names
- **OpenAI**: `gpt-4o-mini`, `gpt-4`, etc.
- **Watson X.AI**: `ibm/granite-13b-chat-v2`, `meta-llama/llama-2-70b-chat`, etc.

### 3. API Structure
- **OpenAI**: Direct chat completions API
- **Watson X.AI**: Foundation models API with project-based access

### 4. Tool Calling
- **OpenAI**: Native function calling support
- **Watson X.AI**: Custom implementation using prompt engineering

## Features Demonstrated

1. **Basic Agent Configuration (v1)**
   - Instructions and model settings
   - Simple agent execution with Watson X.AI

2. **Structured Output (v2)**
   - Using Pydantic models for structured responses
   - JSON parsing from Watson X.AI responses
   - Travel planning with organized information

3. **Tool Calls (v3)**
   - Custom tools for retrieving external data
   - Weather forecasting integration
   - Tool result incorporation

## Migration Guide

To migrate from OpenAI to Watson X.AI:

1. **Replace imports**: Change `from agents import Agent, Runner` to `from watson_agents import Agent, Runner`
2. **Update model names**: Change OpenAI model names to Watson X.AI model IDs
3. **Update environment variables**: Replace OpenAI credentials with Watson X.AI credentials
4. **Test structured outputs**: Watson X.AI may require more explicit JSON formatting instructions

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your `WATSONX_API_KEY` and `WATSONX_PROJECT_ID`
2. **Model Not Found**: Check that the model ID is correct and available in your region
3. **Structured Output Issues**: Watson X.AI models may need more explicit JSON format instructions
4. **Tool Calling**: The current implementation uses prompt engineering; for complex tools, you may need to enhance the tool calling logic

## Notes

- This is a demonstration project and uses simulated data for weather, flights, and hotels
- The Watson X.AI wrapper (`watson_agents.py`) provides OpenAI SDK compatibility but may not support all advanced features
- For production use, consider implementing more robust error handling and tool calling mechanisms
- Watson X.AI responses may vary from OpenAI due to different model characteristics

## Support

For Watson X.AI specific issues:
- [IBM Watson Machine Learning Documentation](https://cloud.ibm.com/apidocs/machine-learning)
- [Watson Studio Documentation](https://dataplatform.cloud.ibm.com/docs/)

For general agent implementation questions:
- Review the original OpenAI implementations for comparison
- Check the `watson_agents.py` wrapper for implementation details