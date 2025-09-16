# Universal OpenAI to Watson X.AI Migration Pattern

This document provides a universal pattern for migrating any OpenAI-based project to Watson X.AI.

## 🎯 Migration Strategy

The key insight is that Watson X.AI migration doesn't require rewriting your entire application. Instead, we create compatibility wrappers that maintain the same interface while using Watson X.AI as the backend.

## 📋 Step-by-Step Migration Process

### 1. Identify OpenAI Dependencies

Look for these patterns in your codebase:

```python
# Direct OpenAI imports
from openai import OpenAI
import openai

# OpenAI Agents SDK
from agents import Agent, Runner

# Pydantic AI with OpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
```

### 2. Environment Variable Migration

| OpenAI | Watson X.AI | Notes |
|--------|-------------|-------|
| `OPENAI_API_KEY` | `WATSONX_API_KEY` | Your IBM Cloud API key |
| `OPENAI_ORG_ID` | `WATSONX_PROJECT_ID` | Watson Studio project ID |
| `MODEL_CHOICE=gpt-4o-mini` | `WATSONX_MODEL=ibm/granite-13b-chat-v2` | Model selection |
| N/A | `WATSONX_URL=https://us-south.ml.cloud.ibm.com` | Regional endpoint |

### 3. Dependency Migration

Replace in `requirements.txt`:

```diff
- openai==1.66.3
- openai-agents==0.0.4
+ ibm-watson-machine-learning==1.0.368
```

Keep these if already present:
```
pydantic==2.10.6
python-dotenv==1.0.1
```

### 4. Code Migration Patterns

#### Pattern A: Direct OpenAI Client Replacement

**Before:**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**After:**
```python
from ibm_watson_machine_learning import APIClient

client = APIClient({
    "url": os.getenv("WATSONX_URL"),
    "apikey": os.getenv("WATSONX_API_KEY")
})
client.set.default_project(os.getenv("WATSONX_PROJECT_ID"))

response_text = client.foundation_models.generate_text(
    model_id=os.getenv("WATSONX_MODEL", "ibm/granite-13b-chat-v2"),
    prompt="User: Hello\nAssistant: ",
    params={"max_new_tokens": 1000, "temperature": 0.7}
)
```

#### Pattern B: OpenAI Agents SDK Replacement

**Before:**
```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are helpful",
    model="gpt-4o-mini"
)

result = Runner.run_sync(agent, "Hello")
```

**After:**
```python
from watson_agents import Agent, Runner  # Use our wrapper

agent = Agent(
    name="Assistant", 
    instructions="You are helpful",
    model="ibm/granite-13b-chat-v2"
)

result = Runner.run_sync(agent, "Hello")  # Same interface!
```

#### Pattern C: Complex Integration (like mem0)

For projects that integrate OpenAI with other services:

1. **Create compatibility layer**: Build a wrapper that mimics OpenAI's interface
2. **Maintain existing integrations**: Don't modify the third-party library integration
3. **Swap the backend**: Replace OpenAI calls with Watson X.AI calls

## 🔧 Migration Tools Provided

### Core Watson X.AI Wrapper
- `watson_agents.py` - Drop-in replacement for OpenAI Agents SDK
- Maintains identical interface
- Handles authentication, model calls, and response formatting

### Example Migrations
- `v1_basic_agent_watsonx.py` - Basic agent migration
- `v2_structured_output_watsonx.py` - Structured output migration  
- `v3_tool_calls_watsonx.py` - Tool calling migration
- `mem0_agent_watsonx_example.py` - Complex integration migration

### Configuration Templates
- `.env.watsonx.example` - Environment variable template
- `requirements_watsonx.txt` - Dependency requirements
- `README_watsonx.md` - Complete setup documentation

## 🏗️ Architecture Comparison

### OpenAI Architecture
```
Your Code → OpenAI SDK → OpenAI API → GPT Models
```

### Watson X.AI Architecture  
```
Your Code → Watson Wrapper → Watson ML SDK → Watson X.AI API → IBM/Meta Models
```

### Hybrid Architecture (Both)
```
Your Code → Abstraction Layer → [OpenAI SDK | Watson Wrapper] → [OpenAI | Watson X.AI]
```

## 🔄 Model Mapping

| OpenAI Model | Watson X.AI Equivalent | Use Case |
|--------------|------------------------|----------|
| `gpt-4o-mini` | `ibm/granite-13b-chat-v2` | General chat, fast responses |
| `gpt-4` | `meta-llama/llama-2-70b-chat` | Complex reasoning |
| `gpt-3.5-turbo` | `ibm/granite-20b-multilingual` | Multilingual tasks |
| `text-embedding-ada-002` | `ibm/slate-30m-english-rtrvr` | Text embeddings |

## 🚀 Advanced Migration Scenarios

### Scenario 1: Multi-Agent Systems

If you have multiple agents using OpenAI:

```python
# Before
agent1 = Agent(name="Researcher", model="gpt-4")
agent2 = Agent(name="Writer", model="gpt-4o-mini") 
agent3 = Agent(name="Critic", model="gpt-4")

# After - Mix and match models
agent1 = Agent(name="Researcher", model="meta-llama/llama-2-70b-chat")
agent2 = Agent(name="Writer", model="ibm/granite-13b-chat-v2")
agent3 = Agent(name="Critic", model="meta-llama/llama-2-70b-chat")
```

### Scenario 2: Streaming Responses

Watson X.AI doesn't have built-in streaming, but you can simulate it:

```python
def stream_watson_response(prompt):
    response = client.foundation_models.generate_text(
        model_id=model,
        prompt=prompt,
        params={"max_new_tokens": 1000}
    )
    
    # Simulate streaming by yielding words
    words = response.split()
    for word in words:
        yield word + " "
        time.sleep(0.05)  # Simulate streaming delay
```

### Scenario 3: Function Calling

Watson X.AI doesn't have native function calling, but our wrapper provides it:

```python
@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Use tools when needed. For tool calls, respond with: TOOL_CALL: function_name(args)",
    model="ibm/granite-13b-chat-v2"
)
agent.add_tool(get_weather)
```

## 📊 Migration Checklist

### Pre-Migration
- [ ] Inventory all OpenAI usage in your codebase
- [ ] Identify direct API calls vs SDK usage
- [ ] Note any special features used (streaming, functions, etc.)
- [ ] Set up Watson X.AI access and credentials

### Migration  
- [ ] Install Watson X.AI dependencies
- [ ] Update environment variables
- [ ] Replace imports with Watson equivalents
- [ ] Update model names
- [ ] Test basic functionality

### Post-Migration
- [ ] Performance testing with Watson X.AI models
- [ ] Cost comparison analysis  
- [ ] Update documentation
- [ ] Train team on new configuration
- [ ] Monitor for any edge cases

## 🎯 Success Metrics

Track these metrics to measure migration success:

1. **Compatibility**: % of original functionality working
2. **Performance**: Response time comparison
3. **Quality**: Response quality comparison
4. **Cost**: Cost per token/request comparison
5. **Reliability**: Error rates and uptime

## 🔮 Future Enhancements

Potential improvements to the Watson X.AI wrapper:

1. **Native Streaming**: Implement actual streaming responses
2. **Enhanced Function Calling**: More sophisticated tool calling
3. **Batch Processing**: Support for batch API requests
4. **Model Switching**: Dynamic model selection per request
5. **Caching**: Response caching for cost optimization

## 📞 Getting Help

1. **Watson X.AI Issues**: Check IBM Cloud documentation
2. **Migration Issues**: Review this guide and examples
3. **Custom Requirements**: Extend the watson_agents.py wrapper
4. **Performance Issues**: Consider different Watson X.AI models

---

This migration pattern provides a robust foundation for moving any OpenAI-based application to Watson X.AI while maintaining code compatibility and functionality.