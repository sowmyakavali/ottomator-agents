# OpenAI to Watson X.AI Migration Comparison

This document shows the exact changes needed to migrate from OpenAI to Watson X.AI.

## 1. Import Changes

### Before (OpenAI):
```python
from agents import Agent, Runner
```

### After (Watson X.AI):
```python
from watson_agents import Agent, Runner
```

## 2. Environment Variables

### Before (OpenAI):
```bash
OPENAI_API_KEY=your_openai_api_key
MODEL_CHOICE=gpt-4o-mini
```

### After (Watson X.AI):
```bash
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-chat-v2
```

## 3. Model Names

### Before (OpenAI):
```python
model = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
```

### After (Watson X.AI):
```python
model = os.getenv('WATSONX_MODEL', 'ibm/granite-13b-chat-v2')
```

## 4. Agent Creation (No Changes Needed!)

### OpenAI and Watson X.AI (Identical):
```python
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant",
    model=model
)
```

## 5. Running Agents (No Changes Needed!)

### OpenAI and Watson X.AI (Identical):
```python
# Synchronous
result = Runner.run_sync(agent, "Your query here")

# Asynchronous  
result = await Runner.run(agent, "Your query here")
```

## 6. Structured Output (No Changes Needed!)

### OpenAI and Watson X.AI (Identical):
```python
class TravelPlan(BaseModel):
    destination: str
    duration_days: int
    budget: float
    activities: List[str]
    notes: str

agent = Agent(
    name="Travel Planner",
    instructions="...",
    model=model,
    output_type=TravelPlan  # Same interface!
)
```

## 7. Tool Functions (No Changes Needed!)

### OpenAI and Watson X.AI (Identical):
```python
@function_tool
def get_weather_forecast(city: str, date: str) -> str:
    """Get weather forecast for a city"""
    return f"Weather in {city}: sunny"

agent.add_tool(get_weather_forecast)  # Same interface!
```

## 8. Dependencies

### Before (OpenAI):
```
openai==1.66.3
openai-agents==0.0.4
```

### After (Watson X.AI):
```
ibm-watson-machine-learning==1.0.368
```

## Key Benefits of This Migration

1. **Zero Code Changes**: Your existing agent logic remains exactly the same
2. **Drop-in Replacement**: Just change the import and environment variables
3. **Enterprise Grade**: Watson X.AI provides enterprise security and compliance
4. **Model Variety**: Access to IBM Granite, Meta Llama, and other foundation models
5. **No Vendor Lock-in**: Easy to switch back or to other providers

## File Structure Comparison

### Original OpenAI Project:
```
openai-sdk-agent/
├── v1_basic_agent.py
├── v2_structured_output.py  
├── v3_tool_calls.py
├── requirements.txt
├── .env.example
└── README.md
```

### With Watson X.AI Migration:
```
openai-sdk-agent/
├── v1_basic_agent.py                    # Original OpenAI versions
├── v2_structured_output.py
├── v3_tool_calls.py
├── v1_basic_agent_watsonx.py           # Watson X.AI versions
├── v2_structured_output_watsonx.py
├── v3_tool_calls_watsonx.py
├── watson_agents.py                     # Watson X.AI wrapper
├── requirements.txt                     # Original requirements
├── requirements_watsonx.txt             # Watson X.AI requirements
├── .env.example                         # Original env config
├── .env.watsonx.example                # Watson X.AI env config
├── README.md                           # Original README
├── README_watsonx.md                   # Watson X.AI README
└── migration_demo.py                   # Migration demo
```

## Complete Migration Example

Here's a complete before/after example:

### Before (OpenAI - v2_structured_output.py):
```python
from agents import Agent, Runner
from dotenv import load_dotenv
import os

load_dotenv()
model = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')

travel_agent = Agent(
    name="Travel Planner",
    instructions="You are a travel planning assistant...",
    model=model,
    output_type=TravelPlan
)

result = await Runner.run(travel_agent, query)
```

### After (Watson X.AI - v2_structured_output_watsonx.py):
```python
from watson_agents import Agent, Runner  # Only change!
from dotenv import load_dotenv
import os

load_dotenv()
model = os.getenv('WATSONX_MODEL', 'ibm/granite-13b-chat-v2')  # Only change!

travel_agent = Agent(
    name="Travel Planner", 
    instructions="You are a travel planning assistant...",
    model=model,
    output_type=TravelPlan
)

result = await Runner.run(travel_agent, query)  # Same code!
```

## Getting Started with Watson X.AI

1. **Get Access**: Sign up for IBM Cloud and Watson Machine Learning
2. **Create Project**: Set up a Watson Studio project  
3. **Get Credentials**: Generate API key and note project ID
4. **Install Dependencies**: `pip install -r requirements_watsonx.txt`
5. **Configure Environment**: Copy `.env.watsonx.example` to `.env` and fill in credentials
6. **Run Migrated Agents**: `python v1_basic_agent_watsonx.py`

That's it! Your OpenAI agents now run on Watson X.AI with minimal changes required.