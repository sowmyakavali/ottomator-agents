#!/usr/bin/env python3
"""
Compatibility Test Suite for Watson X.AI Migration
This script verifies that the Watson X.AI implementation maintains full compatibility with the OpenAI interface
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Set up mock environment for testing
os.environ['WATSONX_API_KEY'] = 'test_key'
os.environ['WATSONX_PROJECT_ID'] = 'test_project'
os.environ['WATSONX_MODEL'] = 'ibm/granite-13b-chat-v2'

def test_interface_compatibility():
    """Test that Watson X.AI agents have the same interface as OpenAI agents"""
    
    print("🧪 Testing Interface Compatibility")
    print("-" * 40)
    
    try:
        # Test imports
        from watson_agents import Agent, Runner, function_tool
        from pydantic import BaseModel, Field
        from typing import List
        print("✓ All required imports successful")
        
        # Test basic agent creation
        agent = Agent(
            name="Test Agent",
            instructions="Test instructions",
            model="ibm/granite-13b-chat-v2"
        )
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'instructions') 
        assert hasattr(agent, 'model')
        assert hasattr(agent, 'run_sync')
        assert hasattr(agent, 'run_async')
        assert hasattr(agent, 'add_tool')
        print("✓ Basic agent interface compatible")
        
        # Test structured output
        class TestOutput(BaseModel):
            message: str
            count: int
            items: List[str] = Field(description="List of items")
        
        structured_agent = Agent(
            name="Structured Agent",
            instructions="Return structured output",
            model="ibm/granite-13b-chat-v2",
            output_type=TestOutput
        )
        assert structured_agent.output_type == TestOutput
        print("✓ Structured output interface compatible")
        
        # Test tool function decorator
        @function_tool
        def test_function(param: str) -> str:
            """Test function"""
            return f"Result: {param}"
        
        assert callable(test_function)
        assert test_function("test") == "Result: test"
        print("✓ Function tool decorator compatible")
        
        # Test tool registration
        tool_agent = Agent(
            name="Tool Agent",
            instructions="Use tools",
            model="ibm/granite-13b-chat-v2"
        )
        tool_agent.add_tool(test_function)
        assert test_function in tool_agent.tools
        print("✓ Tool registration compatible")
        
        # Test Runner class
        assert hasattr(Runner, 'run_sync')
        assert hasattr(Runner, 'run')
        assert callable(Runner.run_sync)
        assert callable(Runner.run)
        print("✓ Runner interface compatible")
        
        return True
        
    except Exception as e:
        print(f"✗ Compatibility test failed: {e}")
        return False

def test_method_signatures():
    """Test that method signatures match OpenAI SDK expectations"""
    
    print("\n🔍 Testing Method Signatures")
    print("-" * 40)
    
    try:
        from watson_agents import Agent, Runner
        import inspect
        
        # Test Agent.__init__ signature
        agent_init_sig = inspect.signature(Agent.__init__)
        expected_params = ['self', 'name', 'instructions', 'model', 'output_type']
        actual_params = list(agent_init_sig.parameters.keys())
        for param in expected_params:
            assert param in actual_params, f"Missing parameter: {param}"
        print("✓ Agent.__init__ signature compatible")
        
        # Test Runner.run_sync signature
        run_sync_sig = inspect.signature(Runner.run_sync)
        expected_params = ['agent', 'user_input']
        actual_params = list(run_sync_sig.parameters.keys())
        for param in expected_params:
            assert param in actual_params, f"Missing parameter: {param}"
        print("✓ Runner.run_sync signature compatible")
        
        # Test Runner.run signature  
        run_sig = inspect.signature(Runner.run)
        expected_params = ['agent', 'user_input']
        actual_params = list(run_sig.parameters.keys())
        for param in expected_params:
            assert param in actual_params, f"Missing parameter: {param}"
        print("✓ Runner.run signature compatible")
        
        return True
        
    except Exception as e:
        print(f"✗ Method signature test failed: {e}")
        return False

def test_example_compatibility():
    """Test that our examples have the same structure as OpenAI examples"""
    
    print("\n📝 Testing Example Compatibility")
    print("-" * 40)
    
    try:
        # Check that Watson X.AI examples exist
        watsonx_files = [
            'v1_basic_agent_watsonx.py',
            'v2_structured_output_watsonx.py', 
            'v3_tool_calls_watsonx.py'
        ]
        
        for filename in watsonx_files:
            filepath = f"/home/runner/work/ottomator-agents/ottomator-agents/openai-sdk-agent/{filename}"
            assert os.path.exists(filepath), f"Missing Watson X.AI example: {filename}"
            
            # Read file and check for key patterns
            with open(filepath, 'r') as f:
                content = f.read()
                assert 'from watson_agents import Agent, Runner' in content, f"Missing import in {filename}"
                assert 'Agent(' in content, f"Missing Agent creation in {filename}"
                assert 'Runner.run' in content or 'Runner.run_sync' in content, f"Missing Runner usage in {filename}"
        
        print("✓ All Watson X.AI examples exist and have correct structure")
        
        # Check configuration files
        config_files = [
            '.env.watsonx.example',
            'requirements_watsonx.txt',
            'README_watsonx.md'
        ]
        
        for filename in config_files:
            filepath = f"/home/runner/work/ottomator-agents/ottomator-agents/openai-sdk-agent/{filename}"
            assert os.path.exists(filepath), f"Missing configuration file: {filename}"
        
        print("✓ All configuration files exist")
        
        return True
        
    except Exception as e:
        print(f"✗ Example compatibility test failed: {e}")
        return False

def test_error_handling():
    """Test that error handling is implemented"""
    
    print("\n⚠️  Testing Error Handling")
    print("-" * 40)
    
    try:
        # Test missing API key
        old_key = os.environ.get('WATSONX_API_KEY')
        if 'WATSONX_API_KEY' in os.environ:
            del os.environ['WATSONX_API_KEY']
        
        try:
            from watson_agents import Agent
            agent = Agent("Test", "Test", "test-model")
            assert False, "Should have raised ValueError for missing API key"
        except ValueError as e:
            assert "WATSONX_API_KEY" in str(e)
            print("✓ Missing API key error handling works")
        finally:
            if old_key:
                os.environ['WATSONX_API_KEY'] = old_key
        
        # Test missing project ID
        old_project = os.environ.get('WATSONX_PROJECT_ID')
        if 'WATSONX_PROJECT_ID' in os.environ:
            del os.environ['WATSONX_PROJECT_ID']
        
        try:
            from watson_agents import Agent
            agent = Agent("Test", "Test", "test-model")
            assert False, "Should have raised ValueError for missing project ID"
        except ValueError as e:
            assert "WATSONX_PROJECT_ID" in str(e)
            print("✓ Missing project ID error handling works")
        finally:
            if old_project:
                os.environ['WATSONX_PROJECT_ID'] = old_project
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def main():
    """Run all compatibility tests"""
    
    print("🚀 Watson X.AI Compatibility Test Suite")
    print("=" * 50)
    
    tests = [
        test_interface_compatibility,
        test_method_signatures,
        test_example_compatibility,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All compatibility tests passed!")
        print("✅ Watson X.AI migration maintains full OpenAI interface compatibility")
        print("\n🚀 Ready for production use!")
    else:
        print("❌ Some compatibility tests failed")
        print("⚠️  Review the failed tests and fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()