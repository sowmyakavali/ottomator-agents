#!/usr/bin/env python3
"""
Example usage of the watsonx OnToCast Agent

This script demonstrates how to use the watsonx OnToCast agent in various ways:
1. Standalone usage
2. API server usage
3. Testing different scenarios
"""

import asyncio
import os
import json
from typing import Dict, List

# Mock environment setup for demonstration
def setup_demo_environment():
    """Set up demo environment variables if not already configured."""
    demo_config = {
        "WATSONX_URL": "https://us-south.ml.cloud.ibm.com",
        "WATSONX_PROJECT_ID": "demo-project-id",
        "WATSONX_API_KEY": "demo-api-key",
        "WATSONX_MODEL": "meta-llama/llama-3-1-70b-instruct",
        "API_BEARER_TOKEN": "demo-bearer-token"
    }
    
    for key, value in demo_config.items():
        if not os.getenv(key):
            os.environ[key] = value

async def demo_standalone_agent():
    """Demonstrate standalone agent usage."""
    print("🔧 Demo: Standalone Agent Usage")
    print("=" * 50)
    
    try:
        # This would normally require real credentials
        from studio_integration_version.watsonx_ontocast_agent import WatsonxOnToCastAgent
        
        agent = WatsonxOnToCastAgent()
        
        # Example conversations
        test_queries = [
            "What is IBM watsonx.ai?",
            "How can I use foundation models for business applications?",
            "What are the benefits of using IBM's Granite models?",
            "Can you help me understand the difference between various AI models?"
        ]
        
        session_id = "demo_session_123"
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            
            # This would work with real credentials
            # response = await agent.generate_response(query, session_id)
            # print(f"🤖 Response: {response}")
            
            # Demo response
            print(f"🤖 Response: [Demo] This would be a response from watsonx.ai about: {query}")
            
    except Exception as e:
        print(f"❌ Demo error (expected without real credentials): {str(e)}")
        print("💡 This demo shows the structure - use real credentials for actual responses")

async def demo_api_server():
    """Demonstrate API server usage."""
    print("\n🌐 Demo: API Server Usage")
    print("=" * 50)
    
    # Example API request data
    test_requests = [
        {
            "query": "Hello, introduce yourself",
            "user_id": "demo_user_1",
            "request_id": "req_001",
            "session_id": "session_001"
        },
        {
            "query": "What can you help me with?", 
            "user_id": "demo_user_1",
            "request_id": "req_002", 
            "session_id": "session_001"
        }
    ]
    
    print("Example API requests that would be sent to the server:")
    for i, request in enumerate(test_requests, 1):
        print(f"\n📤 Request {i}:")
        print(json.dumps(request, indent=2))
        
        # Example curl command
        print(f"\n🔧 Equivalent curl command:")
        curl_cmd = f"""curl -X POST http://localhost:8001/watsonx-ontocast-agent \\
  -H "Authorization: Bearer your-token-here" \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(request)}'"""
        print(curl_cmd)

def demo_configuration():
    """Demonstrate configuration options."""
    print("\n⚙️  Demo: Configuration Options")
    print("=" * 50)
    
    print("Supported watsonx.ai models:")
    models = [
        "meta-llama/llama-3-1-70b-instruct - Best for complex reasoning",
        "meta-llama/llama-3-1-8b-instruct - Balanced performance and speed", 
        "ibm/granite-3-8b-instruct - IBM's enterprise-optimized model",
        "ibm/granite-3-2b-instruct - Lightweight IBM model",
        "mistralai/mixtral-8x7b-instruct-v01 - Excellent for multilingual tasks"
    ]
    
    for model in models:
        print(f"  • {model}")
    
    print("\nEnvironment variables to configure:")
    env_vars = [
        ("WATSONX_API_KEY", "Your IBM watsonx.ai API key"),
        ("WATSONX_PROJECT_ID", "Your watsonx.ai project ID"),
        ("WATSONX_URL", "watsonx.ai endpoint URL (default: us-south)"),
        ("WATSONX_MODEL", "Foundation model to use"),
        ("SUPABASE_URL", "Supabase project URL (optional)"),
        ("SUPABASE_SERVICE_KEY", "Supabase service key (optional)"),
        ("DATABASE_URL", "PostgreSQL connection string (optional)"),
        ("API_BEARER_TOKEN", "Authentication token for API")
    ]
    
    for var, description in env_vars:
        print(f"  • {var}: {description}")

def demo_deployment_options():
    """Demonstrate deployment options."""
    print("\n🚀 Demo: Deployment Options")
    print("=" * 50)
    
    print("1. 🐳 Docker Deployment:")
    docker_commands = [
        "# Build the image",
        "docker build -t watsonx-ontocast-agent .",
        "",
        "# Run with environment file",
        "docker run -d --name watsonx-agent -p 8001:8001 --env-file .env watsonx-ontocast-agent",
        "",
        "# Run with environment variables",
        "docker run -d --name watsonx-agent -p 8001:8001 \\",
        "  -e WATSONX_API_KEY=your-key \\",
        "  -e WATSONX_PROJECT_ID=your-project \\",
        "  watsonx-ontocast-agent"
    ]
    
    for cmd in docker_commands:
        print(f"  {cmd}")
    
    print("\n2. 🖥️  Local Development:")
    local_commands = [
        "# Install dependencies",
        "pip install -r requirements.txt",
        "",
        "# Run the API server",
        "uvicorn watsonx_ontocast_agent:app --host 0.0.0.0 --port 8001",
        "",
        "# Run the standalone agent",
        "python studio-integration-version/watsonx_ontocast_agent.py"
    ]
    
    for cmd in local_commands:
        print(f"  {cmd}")
    
    print("\n3. 🌟 Live Agent Studio Integration:")
    studio_steps = [
        "1. Upload the studio-integration-version files to the platform",
        "2. Configure environment variables in the studio",
        "3. Set the endpoint to: watsonx-ontocast-agent",
        "4. Test the agent through the studio interface"
    ]
    
    for step in studio_steps:
        print(f"  {step}")

def demo_testing_scenarios():
    """Demonstrate testing scenarios."""
    print("\n🧪 Demo: Testing Scenarios")
    print("=" * 50)
    
    test_scenarios = [
        {
            "name": "Basic Conversation",
            "queries": [
                "Hello, who are you?",
                "What can you help me with?",
                "How do you use watsonx.ai?"
            ]
        },
        {
            "name": "Technical Questions",
            "queries": [
                "Explain foundation models",
                "What's the difference between Llama and Granite models?",
                "How do I choose the right AI model for my use case?"
            ]
        },
        {
            "name": "Creative Tasks",
            "queries": [
                "Write a short story about AI",
                "Help me brainstorm ideas for a tech startup",
                "Create a marketing slogan for a new app"
            ]
        },
        {
            "name": "Problem Solving",
            "queries": [
                "I need to analyze customer feedback data",
                "How can I improve my website's user experience?",
                "What's the best approach for machine learning project planning?"
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📋 {scenario['name']}:")
        for i, query in enumerate(scenario['queries'], 1):
            print(f"  {i}. {query}")

async def main():
    """Main demo function."""
    print("🤖 watsonx OnToCast Agent - Demo & Examples")
    print("=" * 60)
    print("This script demonstrates the features and usage of the watsonx OnToCast agent.")
    print("Note: Real watsonx.ai credentials are required for actual functionality.\n")
    
    setup_demo_environment()
    
    # Run all demos
    await demo_standalone_agent()
    await demo_api_server()
    demo_configuration()
    demo_deployment_options()
    demo_testing_scenarios()
    
    print("\n🎯 Summary")
    print("=" * 50)
    print("The watsonx OnToCast agent provides:")
    print("✅ Integration with IBM watsonx.ai foundation models")
    print("✅ Multiple deployment options (Docker, local, cloud)")
    print("✅ Conversation history management")
    print("✅ RESTful API interface")
    print("✅ Live Agent Studio compatibility")
    print("✅ Flexible model selection")
    print("✅ Comprehensive error handling")
    
    print("\n🚀 Next Steps:")
    print("1. Set up your watsonx.ai credentials")
    print("2. Run the setup script: python setup.py")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start the agent: uvicorn watsonx_ontocast_agent:app --port 8001")
    print("5. Test with: curl -X POST http://localhost:8001/watsonx-ontocast-agent")

if __name__ == "__main__":
    asyncio.run(main())