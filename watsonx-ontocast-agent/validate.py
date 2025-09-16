#!/usr/bin/env python3
"""
Validation Script for watsonx OnToCast Agent

This script validates the agent setup and configuration without requiring
actual watsonx.ai credentials.
"""

import os
import sys
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def print_result(test_name, passed, details=None):
    """Print test result with status."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test_name}")
    if details and not passed:
        print(f"   Details: {details}")

def validate_file_structure():
    """Validate that all required files exist."""
    print_header("File Structure Validation")
    
    required_files = [
        "README.md",
        "requirements.txt", 
        ".env.example",
        "Dockerfile",
        ".dockerignore",
        "setup.py",
        "example.py",
        "watsonx_ontocast_agent.py",
        "watsonx_ontocast_agent_supabase.py",
        "studio-integration-version/requirements.txt",
        "studio-integration-version/watsonx_ontocast_agent.py",
        "studio-integration-version/watsonx_ontocast_agent_endpoint.py",
        "INTEGRATION_GUIDE.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        print_result(f"File exists: {file_path}", exists)
        if not exists:
            all_exist = False
    
    return all_exist

def validate_python_syntax():
    """Validate Python syntax of all Python files."""
    print_header("Python Syntax Validation")
    
    python_files = [
        "setup.py",
        "example.py", 
        "watsonx_ontocast_agent.py",
        "watsonx_ontocast_agent_supabase.py",
        "studio-integration-version/watsonx_ontocast_agent.py",
        "studio-integration-version/watsonx_ontocast_agent_endpoint.py"
    ]
    
    all_valid = True
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print_result(f"Syntax valid: {file_path}", True)
        except SyntaxError as e:
            print_result(f"Syntax valid: {file_path}", False, str(e))
            all_valid = False
        except FileNotFoundError:
            print_result(f"Syntax valid: {file_path}", False, "File not found")
            all_valid = False
    
    return all_valid

def validate_env_example():
    """Validate .env.example file format."""
    print_header("Environment Configuration Validation")
    
    required_vars = [
        "WATSONX_URL",
        "WATSONX_PROJECT_ID", 
        "WATSONX_API_KEY",
        "WATSONX_MODEL",
        "API_BEARER_TOKEN"
    ]
    
    try:
        with open('.env.example', 'r') as f:
            content = f.read()
        
        all_vars_present = True
        for var in required_vars:
            if var in content:
                print_result(f"Environment variable: {var}", True)
            else:
                print_result(f"Environment variable: {var}", False)
                all_vars_present = False
        
        return all_vars_present
        
    except FileNotFoundError:
        print_result("Environment template file", False, ".env.example not found")
        return False

def validate_requirements():
    """Validate requirements.txt files."""
    print_header("Dependencies Validation")
    
    requirements_files = [
        "requirements.txt",
        "studio-integration-version/requirements.txt"
    ]
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "python-dotenv",
        "ibm-watsonx-ai",
        "supabase"
    ]
    
    all_valid = True
    for req_file in requirements_files:
        try:
            with open(req_file, 'r') as f:
                content = f.read().lower()
            
            file_valid = True
            for package in required_packages:
                if package.replace('-', '_') in content or package in content:
                    print_result(f"{req_file} contains {package}", True)
                else:
                    print_result(f"{req_file} contains {package}", False)
                    file_valid = False
            
            if not file_valid:
                all_valid = False
                
        except FileNotFoundError:
            print_result(f"Requirements file: {req_file}", False, "File not found")
            all_valid = False
    
    return all_valid

def validate_docker_config():
    """Validate Docker configuration."""
    print_header("Docker Configuration Validation")
    
    try:
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
        
        checks = [
            ("FROM ottomator/base-python:latest" in dockerfile_content, "Uses base image"),
            ("COPY . ." in dockerfile_content, "Copies application code"),
            ("EXPOSE" in dockerfile_content, "Exposes port"),
            ("CMD" in dockerfile_content or "ENTRYPOINT" in dockerfile_content, "Has run command")
        ]
        
        all_valid = True
        for check, description in checks:
            print_result(f"Dockerfile {description}", check)
            if not check:
                all_valid = False
        
        return all_valid
        
    except FileNotFoundError:
        print_result("Dockerfile exists", False, "Dockerfile not found")
        return False

def validate_documentation():
    """Validate documentation completeness."""
    print_header("Documentation Validation")
    
    try:
        with open('README.md', 'r') as f:
            readme_content = f.read()
        
        required_sections = [
            ("# watsonx OnToCast Agent", "Has main title"),
            ("## Overview", "Has overview section"),
            ("## Prerequisites", "Has prerequisites"),
            ("## Quick Start", "Has quick start guide"),
            ("## Example Usage", "Has usage examples"),
            ("watsonx.ai", "Mentions watsonx.ai"),
            ("IBM", "Mentions IBM")
        ]
        
        all_sections = True
        for section, description in required_sections:
            if section in readme_content:
                print_result(f"README {description}", True)
            else:
                print_result(f"README {description}", False)
                all_sections = False
        
        # Check integration guide
        try:
            with open('INTEGRATION_GUIDE.md', 'r') as f:
                guide_content = f.read()
            print_result("Integration guide exists", True)
            
            if "@growgraph/ontocast" in guide_content:
                print_result("Integration guide mentions @growgraph/ontocast", True)
            else:
                print_result("Integration guide mentions @growgraph/ontocast", False)
                all_sections = False
                
        except FileNotFoundError:
            print_result("Integration guide exists", False)
            all_sections = False
        
        return all_sections
        
    except FileNotFoundError:
        print_result("README.md exists", False, "README.md not found")
        return False

def run_example_script():
    """Test that the example script runs without errors."""
    print_header("Example Script Validation")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'example.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print_result("Example script runs successfully", True)
            return True
        else:
            print_result("Example script runs successfully", False, result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_result("Example script runs successfully", False, "Script timed out")
        return False
    except Exception as e:
        print_result("Example script runs successfully", False, str(e))
        return False

def main():
    """Main validation function."""
    print("🤖 watsonx OnToCast Agent - Validation Script")
    print("=" * 60)
    print("This script validates the agent setup and configuration.")
    
    # Change to the agent directory
    agent_dir = Path(__file__).parent
    os.chdir(agent_dir)
    
    # Run all validations
    validations = [
        ("File Structure", validate_file_structure),
        ("Python Syntax", validate_python_syntax), 
        ("Environment Config", validate_env_example),
        ("Dependencies", validate_requirements),
        ("Docker Config", validate_docker_config),
        ("Documentation", validate_documentation),
        ("Example Script", run_example_script)
    ]
    
    results = []
    for name, validation_func in validations:
        try:
            result = validation_func()
            results.append((name, result))
        except Exception as e:
            print_result(f"Validation: {name}", False, str(e))
            results.append((name, False))
    
    # Summary
    print_header("Validation Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n📊 Overall Result: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 All validations passed! The watsonx OnToCast agent is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Set up your watsonx.ai credentials")
        print("2. Run: python setup.py")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Start the agent: uvicorn watsonx_ontocast_agent:app --port 8001")
    else:
        print(f"\n⚠️  {total - passed} validations failed. Please review and fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())