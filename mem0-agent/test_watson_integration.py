#!/usr/bin/env python3
"""
Simple test to verify Watson AI integration structure
This test verifies the code structure without requiring actual Watson AI credentials
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required imports are correctly structured"""
    print("Testing import structure...")
    
    # Test v1 basic implementation
    v1_path = Path(__file__).parent / "iterations" / "v1-basic-mem0.py"
    with open(v1_path, 'r') as f:
        v1_content = f.read()
    
    # Check for Watson AI imports
    assert "from ibm_watsonx_ai import APIClient" in v1_content
    assert "from ibm_watsonx_ai.foundation_models import Model" in v1_content
    assert "from openai import OpenAI" not in v1_content
    print("✓ v1-basic-mem0.py: Watson AI imports correct")
    
    # Test v2 supabase implementation
    v2_path = Path(__file__).parent / "iterations" / "v2-supabase-mem0.py"
    with open(v2_path, 'r') as f:
        v2_content = f.read()
    
    assert "from ibm_watsonx_ai import APIClient" in v2_content
    assert "from openai import OpenAI" not in v2_content
    print("✓ v2-supabase-mem0.py: Watson AI imports correct")
    
    # Test v3 streamlit implementation
    v3_path = Path(__file__).parent / "iterations" / "v3-streamlit-supabase-mem0.py"
    with open(v3_path, 'r') as f:
        v3_content = f.read()
    
    assert "from ibm_watsonx_ai import APIClient" in v3_content
    assert "from openai import OpenAI" not in v3_content
    print("✓ v3-streamlit-supabase-mem0.py: Watson AI imports correct")

def test_environment_variables():
    """Test that environment variable names are correctly updated"""
    print("\nTesting environment variables...")
    
    env_path = Path(__file__).parent / ".env.example"
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Check for Watson AI variables
    assert "WATSONX_API_KEY=" in env_content
    assert "WATSONX_PROJECT_ID=" in env_content  
    assert "WATSONX_URL=" in env_content
    # Note: OPENAI_API_KEY may be present for hybrid approach
    print("✓ .env.example: Watson AI variables correct")
    
    # Test studio integration env
    studio_env_path = Path(__file__).parent / "studio-integration-version" / ".env.example"
    with open(studio_env_path, 'r') as f:
        studio_env_content = f.read()
    
    assert "WATSONX_API_KEY=" in studio_env_content
    assert "WATSONX_PROJECT_ID=" in studio_env_content
    print("✓ studio-integration-version/.env.example: Watson AI variables correct")

def test_mem0_configuration():
    """Test that Mem0 configurations use IBM provider"""
    print("\nTesting Mem0 configurations...")
    
    v1_path = Path(__file__).parent / "iterations" / "v1-basic-mem0.py"
    with open(v1_path, 'r') as f:
        v1_content = f.read()
    
    assert '"provider": "ibm"' in v1_content
    assert '"provider": "openai"' not in v1_content
    print("✓ v1: Mem0 config uses IBM provider")
    
    v2_path = Path(__file__).parent / "iterations" / "v2-supabase-mem0.py"
    with open(v2_path, 'r') as f:
        v2_content = f.read()
    
    assert '"provider": "ibm"' in v2_content
    assert '"provider": "openai"' not in v2_content
    print("✓ v2: Mem0 config uses IBM provider")

def test_requirements():
    """Test that requirements.txt is updated"""
    print("\nTesting requirements...")
    
    req_path = Path(__file__).parent / "requirements.txt"
    with open(req_path, 'r') as f:
        req_content = f.read()
    
    assert "ibm-watsonx-ai==1.3.38" in req_content
    # OpenAI may still be present for hybrid approach
    print("✓ requirements.txt: Watson AI dependency correct")
    
    studio_req_path = Path(__file__).parent / "studio-integration-version" / "requirements.txt"
    with open(studio_req_path, 'r') as f:
        studio_req_content = f.read()
    
    assert "ibm-watsonx-ai==1.3.38" in studio_req_content
    print("✓ studio-integration-version/requirements.txt: Watson AI dependency correct")

def test_model_configuration():
    """Test that model configurations use Watson AI models"""
    print("\nTesting model configurations...")
    
    v1_path = Path(__file__).parent / "iterations" / "v1-basic-mem0.py"
    with open(v1_path, 'r') as f:
        v1_content = f.read()
    
    assert "ibm/granite-13b-chat-v2" in v1_content
    print("✓ v1: Uses Watson AI model")
    
    # Check hybrid version
    hybrid_path = Path(__file__).parent / "iterations" / "v1-hybrid-mem0.py"
    with open(hybrid_path, 'r') as f:
        hybrid_content = f.read()
    
    assert "ibm/granite-13b-chat-v2" in hybrid_content
    print("✓ v1-hybrid: Uses Watson AI model")
    
    env_path = Path(__file__).parent / ".env.example"
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    assert "MODEL_CHOICE=ibm/granite-13b-chat-v2" in env_content
    print("✓ .env.example: Default model is Watson AI")

def main():
    """Run all tests"""
    print("Running Watson AI integration tests...\n")
    
    try:
        test_imports()
        test_environment_variables() 
        test_mem0_configuration()
        test_requirements()
        test_model_configuration()
        
        print("\n🎉 All tests passed! Watson AI integration is correctly implemented.")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())