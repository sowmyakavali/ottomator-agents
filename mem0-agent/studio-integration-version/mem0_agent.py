from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import logfire
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
import json

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart, UserPromptPart, TextPart

load_dotenv()
llm = os.getenv('LLM_MODEL', 'ibm/granite-13b-chat-v2')

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')

# Watson AI configuration
credentials = {
    "url": os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
    "apikey": os.environ['WATSONX_API_KEY']
}

watsonx_client = APIClient(credentials)
project_id = os.environ['WATSONX_PROJECT_ID']

# Custom Watson AI model adapter for Pydantic AI
class WatsonXModel:
    def __init__(self, model_id: str, project_id: str, credentials: dict):
        self.model_id = model_id
        self.project_id = project_id
        self.credentials = credentials
        self.model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 512,
                "temperature": 0.7
            }
        )
    
    async def request(self, messages: list[ModelRequest]) -> ModelResponse:
        # Convert Pydantic AI messages to a single prompt for Watson AI
        prompt_parts = []
        for msg in messages:
            for part in msg.parts:
                if isinstance(part, SystemPromptPart):
                    prompt_parts.append(f"System: {part.content}")
                elif isinstance(part, UserPromptPart):
                    prompt_parts.append(f"User: {part.content}")
                elif isinstance(part, TextPart):
                    prompt_parts.append(f"Assistant: {part.content}")
        
        full_prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.model.generate_text, full_prompt
            )
            content = response['results'][0]['generated_text'].strip()
            
            return ModelResponse(
                parts=[TextPart(content=content)]
            )
        except Exception as e:
            raise ModelRetry(f"Watson AI request failed: {e}")

watsonx_model = WatsonXModel(llm, project_id, credentials)


@dataclass
class Mem0Deps:
    memories: str


mem0_agent = Agent(
    watsonx_model,
    system_prompt=f'You are a helpful AI. Answer the question based on query and memories. The current date is: {datetime.now().strftime("%Y-%m-%d")}',
    deps_type=Mem0Deps,
    retries=2
)

@mem0_agent.system_prompt  
def add_memories(ctx: RunContext[str]) -> str:
    return f"\nUser Memories:\n{ctx.deps.memories}"

async def main():
    deps = Mem0Deps(memories="")
    
    result = await mem0_agent.run(
        'Greetings!', deps=deps
    )
    
    print('Response:', result.data)


if __name__ == '__main__':
    asyncio.run(main())