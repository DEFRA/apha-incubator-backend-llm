"""
Quick test script to verify the API is working correctly.
Run this after starting the API server.
"""
import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_test(name):
    """Print test header."""
    print(f"\n{BOLD}Testing: {name}{RESET}")
    print("-" * 60)


def print_success(message):
    """Print success message."""
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    """Print error message."""
    print(f"{RED}✗ {message}{RESET}")


def print_info(message):
    """Print info message."""
    print(f"{YELLOW}ℹ {message}{RESET}")


def test_health():
    """Test health check endpoint."""
    print_test("Health Check Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success("Health check returned 200")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Health check returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Could not connect to API at {API_BASE_URL}")
        print_info("Make sure the API is running: python -m uvicorn src.main:app --reload")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False


def test_config():
    """Test config endpoint."""
    print_test("Configuration Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/config")
        if response.status_code == 200:
            data = response.json()
            print_success("Config endpoint returned 200")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Config endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Config test failed: {str(e)}")
        return False


def test_summarise_valid():
    """Test summarisation with valid input."""
    print_test("Summarisation with Valid Input")
    
    payload = {
        "text": "Artificial intelligence has become increasingly important in modern society. AI systems can process vast amounts of data to identify patterns and make predictions. Machine learning, a subset of AI, enables computers to learn from data without being explicitly programmed. Natural language processing allows computers to understand and generate human language. These technologies are revolutionizing healthcare by improving diagnostics, finance through fraud detection, and education with personalized learning systems.",
        "max_length": 75
    }
    
    try:
        print(f"Sending request with text length: {len(payload['text'])} characters")
        response = requests.post(f"{API_BASE_URL}/summarise", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Summarisation request returned 200")
            print(f"\n{BOLD}Original Text:{RESET}")
            print(data['original_text'][:200] + "...")
            print(f"\n{BOLD}Summary:{RESET}")
            print(data['summary'])
            print(f"\n{BOLD}Tokens Used:{RESET}")
            print(f"  Input: {data['input_tokens']}")
            print(f"  Output: {data['output_tokens']}")
            print(f"  Model: {data['model']}")
            return True
        else:
            print_error(f"Summarisation returned {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Summarisation test failed: {str(e)}")
        return False


def test_summarise_missing_text():
    """Test summarisation with missing text."""
    print_test("Validation: Missing Text")
    
    payload = {"max_length": 50}
    
    try:
        response = requests.post(f"{API_BASE_URL}/summarise", json=payload)
        
        if response.status_code == 422:  # Validation error
            print_success("Missing text field properly rejected (422)")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Validation test failed: {str(e)}")
        return False


def test_summarise_invalid_max_length():
    """Test summarisation with invalid max_length."""
    print_test("Validation: Invalid Max Length")
    
    payload = {
        "text": "Test text",
        "max_length": 10  # Too small, minimum is 50
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/summarise", json=payload)
        
        if response.status_code == 422:  # Validation error
            print_success("Invalid max_length properly rejected (422)")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Validation test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print(f"\n{BOLD}{'=' * 60}")
    print("Text Summarisation API - Quick Test Suite")
    print("=" * 60 + f"{RESET}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Configuration", test_config),
        ("Validation - Missing Text", test_summarise_missing_text),
        ("Validation - Invalid Max Length", test_summarise_invalid_max_length),
        ("Summarisation", test_summarise_valid),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Test interrupted by user{RESET}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{BOLD}{'=' * 60}")
    print("Test Summary")
    print("=" * 60 + f"{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{BOLD}Result: {passed}/{total} tests passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}All tests passed! API is working correctly.{RESET}\n")
        return 0
    else:
        print(f"{RED}Some tests failed. Please check the output above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
