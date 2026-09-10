"""Development task runner for the Summarisation API."""
import subprocess
import sys
import os


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'=' * 60}")
    print(f"{description}")
    print("=" * 60)
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def install_dependencies():
    """Install project dependencies."""
    return run_command(
        "pip install -r requirements.txt",
        "Installing dependencies..."
    )


def run_api():
    """Start the API server."""
    return run_command(
        "python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000",
        "Starting API server..."
    )


def run_tests():
    """Run the test suite."""
    return run_command(
        "pytest tests/ -v",
        "Running tests..."
    )


def run_test_client():
    """Run the quick test client."""
    return run_command(
        "python test_client.py",
        "Running quick tests..."
    )


def main():
    """Main task runner."""
    if len(sys.argv) < 2:
        print("\nAvailable commands:")
        print("  python tasks.py install   - Install dependencies")
        print("  python tasks.py dev       - Start API in development mode")
        print("  python tasks.py test      - Run test suite")
        print("  python tasks.py quicktest - Run quick API tests")
        print("\nUsage: python tasks.py [command]")
        return 1
    
    command = sys.argv[1]
    
    if command == "install":
        return 0 if install_dependencies() else 1
    elif command == "dev":
        return 0 if run_api() else 1
    elif command == "test":
        return 0 if run_tests() else 1
    elif command == "quicktest":
        return 0 if run_test_client() else 1
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
