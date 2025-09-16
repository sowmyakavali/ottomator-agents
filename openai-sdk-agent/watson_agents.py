"""
Watson X.AI Agent Implementation
A drop-in replacement for OpenAI Agents SDK using IBM Watson Machine Learning
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Type, Union, Callable
from dataclasses import dataclass
from pydantic import BaseModel
from ibm_watson_machine_learning import APIClient


@dataclass
class AgentConfig:
    """Configuration for Watson X.AI Agent"""
    name: str
    instructions: str
    model: str
    output_type: Optional[Type[BaseModel]] = None
    tools: Optional[List[Callable]] = None


class WatsonAgent:
    """Watson X.AI Agent that mimics OpenAI Agents SDK interface"""
    
    def __init__(self, name: str, instructions: str, model: str, output_type: Optional[Type[BaseModel]] = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.output_type = output_type
        self.tools = []
        
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
    
    def add_tool(self, tool_func: Callable):
        """Add a tool function to the agent"""
        self.tools.append(tool_func)
    
    def _format_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Format messages for Watson X.AI"""
        return [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": user_input}
        ]
    
    def _get_generation_params(self):
        """Get generation parameters for Watson X.AI"""
        return {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "top_p": 1.0
        }
    
    def _call_watsonx(self, messages: List[Dict[str, str]]) -> str:
        """Make a call to Watson X.AI"""
        try:
            # Convert messages to a single prompt (Watson X.AI format)
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
            
        except Exception as e:
            raise Exception(f"Watson X.AI API call failed: {str(e)}")
    
    def _parse_structured_output(self, response_text: str):
        """Parse structured output if output_type is specified"""
        if not self.output_type:
            return response_text
            
        try:
            # Try to extract JSON from the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                json_data = json.loads(json_str)
                return self.output_type(**json_data)
            else:
                # If no JSON found, try to create structured output from text
                # This is a simplified approach - you might need more sophisticated parsing
                print(f"Warning: Could not extract JSON from response. Returning raw text.")
                return response_text
                
        except Exception as e:
            print(f"Warning: Could not parse structured output: {e}")
            return response_text
    
    def run_sync(self, user_input: str):
        """Synchronous execution of the agent"""
        messages = self._format_messages(user_input)
        
        # If we have tools, we might need to handle tool calls
        # For now, we'll implement a simple approach
        if self.tools:
            # Add tool descriptions to the system message
            tool_descriptions = []
            for tool in self.tools:
                tool_descriptions.append(f"- {tool.__name__}: {tool.__doc__}")
            
            enhanced_instructions = self.instructions + "\n\nAvailable tools:\n" + "\n".join(tool_descriptions)
            enhanced_instructions += "\n\nIf you need to use a tool, respond with TOOL_CALL: tool_name(arguments)"
            
            messages[0]["content"] = enhanced_instructions
        
        response_text = self._call_watsonx(messages)
        
        # Handle tool calls if needed
        if self.tools and "TOOL_CALL:" in response_text:
            response_text = self._handle_tool_calls(response_text, user_input)
        
        # Parse structured output if needed
        final_output = self._parse_structured_output(response_text)
        
        return AgentResult(final_output=final_output, raw_response=response_text)
    
    async def run_async(self, user_input: str):
        """Asynchronous execution of the agent"""
        # For now, just wrap the sync call
        # In a real implementation, you'd want to use async Watson X.AI calls
        return self.run_sync(user_input)
    
    def _handle_tool_calls(self, response_text: str, original_input: str) -> str:
        """Handle tool calls in the response"""
        # Simple tool call handling - find TOOL_CALL: lines and execute them
        lines = response_text.split('\n')
        tool_results = []
        
        for line in lines:
            if line.strip().startswith("TOOL_CALL:"):
                tool_call = line.strip().replace("TOOL_CALL:", "").strip()
                
                # Parse tool call (simplified)
                for tool in self.tools:
                    if tool.__name__ in tool_call:
                        try:
                            # Very simplified argument parsing
                            # In a real implementation, you'd want more robust parsing
                            import re
                            args_match = re.search(r'\((.*?)\)', tool_call)
                            if args_match:
                                args_str = args_match.group(1)
                                # Parse arguments (simplified - assumes string arguments)
                                args = [arg.strip().strip('"').strip("'") for arg in args_str.split(',') if arg.strip()]
                                result = tool(*args)
                                tool_results.append(f"Tool {tool.__name__} result: {result}")
                        except Exception as e:
                            tool_results.append(f"Tool {tool.__name__} error: {str(e)}")
        
        if tool_results:
            # Make another call with tool results
            enhanced_input = f"{original_input}\n\nTool results:\n" + "\n".join(tool_results)
            enhanced_input += "\n\nPlease provide your final response incorporating the tool results."
            
            messages = self._format_messages(enhanced_input)
            return self._call_watsonx(messages)
        
        return response_text


@dataclass 
class AgentResult:
    """Result from agent execution"""
    final_output: Any
    raw_response: str


class WatsonRunner:
    """Runner class that mimics OpenAI Agents SDK Runner"""
    
    @staticmethod
    def run_sync(agent: WatsonAgent, user_input: str) -> AgentResult:
        """Run agent synchronously"""
        return agent.run_sync(user_input)
    
    @staticmethod
    async def run(agent: WatsonAgent, user_input: str) -> AgentResult:
        """Run agent asynchronously"""
        return await agent.run_async(user_input)


def function_tool(func: Callable) -> Callable:
    """Decorator to mark a function as a tool (compatibility with OpenAI SDK)"""
    # For Watson X.AI, we'll just return the function as-is
    # The agent will handle tool registration
    return func


# Alias classes to match OpenAI SDK interface
Agent = WatsonAgent
Runner = WatsonRunner