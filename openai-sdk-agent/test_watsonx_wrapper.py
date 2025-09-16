#!/usr/bin/env python3
"""
Test script for Watson X.AI agents implementation
This script tests the wrapper functionality without making actual API calls
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Set up mock environment variables for testing
os.environ['WATSONX_API_KEY'] = 'test_api_key'
os.environ['WATSONX_PROJECT_ID'] = 'test_project_id'
os.environ['WATSONX_URL'] = 'https://us-south.ml.cloud.ibm.com'
os.environ['WATSONX_MODEL'] = 'ibm/granite-13b-chat-v2'

try:
    from watson_agents import Agent, Runner
    from pydantic import BaseModel, Field
    from typing import List
    
    print("✓ Successfully imported Watson X.AI agents wrapper")
    
    # Test basic agent creation
    try:
        agent = Agent(
            name="Test Agent",
            instructions="You are a test assistant",
            model="ibm/granite-13b-chat-v2"
        )
        print("✓ Successfully created basic Watson X.AI agent")
    except Exception as e:
        print(f"✗ Failed to create basic agent: {e}")
        sys.exit(1)
    
    # Test structured output model
    class TestModel(BaseModel):
        message: str
        count: int
        items: List[str] = Field(description="List of items")
    
    try:
        structured_agent = Agent(
            name="Structured Agent",
            instructions="Return structured JSON output",
            model="ibm/granite-13b-chat-v2",
            output_type=TestModel
        )
        print("✓ Successfully created structured output Watson X.AI agent")
    except Exception as e:
        print(f"✗ Failed to create structured agent: {e}")
        sys.exit(1)
    
    # Test tool function creation
    from watson_agents import function_tool
    
    @function_tool
    def test_tool(input_text: str) -> str:
        """A test tool function"""
        return f"Processed: {input_text}"
    
    try:
        tool_agent = Agent(
            name="Tool Agent",
            instructions="Use tools to help users",
            model="ibm/granite-13b-chat-v2"
        )
        tool_agent.add_tool(test_tool)
        print("✓ Successfully created tool-enabled Watson X.AI agent")
    except Exception as e:
        print(f"✗ Failed to create tool agent: {e}")
        sys.exit(1)
    
    print("\n🎉 All Watson X.AI wrapper tests passed!")
    print("\nTo use the Watson X.AI agents:")
    print("1. Set up your .env file with Watson X.AI credentials")
    print("2. Run: python v1_basic_agent_watsonx.py")
    print("3. Or any other Watson X.AI agent example")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements_watsonx.txt")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)