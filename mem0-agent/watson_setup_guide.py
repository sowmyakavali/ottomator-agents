#!/usr/bin/env python3
"""
Configuration guide for Watson AI integration
"""

def main():
    print("🔧 Watson AI Configuration Guide")
    print("=" * 50)
    print()
    
    print("1. GET WATSON AI CREDENTIALS:")
    print("   • Go to https://dataplatform.cloud.ibm.com/wx/home?context=wx")
    print("   • Sign up or log in to IBM Cloud")
    print("   • Create a new Watson Studio project or select existing one")
    print("   • Copy your Project ID from the project settings")
    print("   • Go to IBM Cloud Identity and Access Management")
    print("   • Create an API key or use existing one")
    print()
    
    print("2. SET UP ENVIRONMENT VARIABLES:")
    print("   Copy .env.example to .env and fill in:")
    print("   • WATSONX_API_KEY=your_ibm_cloud_api_key")
    print("   • WATSONX_PROJECT_ID=your_watson_studio_project_id")
    print("   • WATSONX_URL=https://us-south.ml.cloud.ibm.com (or your region)")
    print("   • MODEL_CHOICE=ibm/granite-13b-chat-v2 (or preferred model)")
    print()
    
    print("3. AVAILABLE REGIONS:")
    print("   • us-south: https://us-south.ml.cloud.ibm.com")
    print("   • eu-de: https://eu-de.ml.cloud.ibm.com")
    print("   • jp-tok: https://jp-tok.ml.cloud.ibm.com")
    print()
    
    print("4. POPULAR MODELS:")
    print("   • ibm/granite-13b-chat-v2 (recommended)")
    print("   • meta-llama/llama-3-8b-instruct")
    print("   • meta-llama/llama-3-70b-instruct")
    print("   • mistralai/mixtral-8x7b-instruct-v01")
    print()
    
    print("5. TESTING YOUR SETUP:")
    print("   • Run: python demo_watson_integration.py")
    print("   • Run: python test_watson_integration.py")
    print("   • Run: python iterations/v1-basic-mem0.py")
    print()
    
    print("6. TROUBLESHOOTING:")
    print("   • 401 Error: Check your API key")
    print("   • 403 Error: Check project permissions")
    print("   • Model not found: Check model name and availability")
    print("   • Timeout: Check network connection and region")
    print()
    
    print("For more help, see README.md or IBM Watson AI documentation.")

if __name__ == "__main__":
    main()