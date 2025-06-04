#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[-]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

check_python() {
    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Get Python version using python3 command
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    
    # Compare version numbers
    REQUIRED_VERSION="3.7"
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        print_error "Python 3.7 or higher is required (found $PYTHON_VERSION)"
        exit 1
    fi
    print_status "Python version $PYTHON_VERSION detected"
}

# Function to check and create virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Installing/updating dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Function to check for Helium browser
check_helium() {
    if [ ! -d "Helium.app" ]; then
        print_warning "Helium browser not found in current directory"
        print_status "Please place Helium.app in the current directory"
        exit 1
    fi
    print_status "Helium browser found"
}

# Function to check OpenAI API key
check_api_key() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        print_status "Creating .env file from template..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_error "Please edit .env file and add your OpenAI API key"
            exit 1
        else
            print_error ".env.example not found"
            exit 1
        fi
    fi
    
    # Check if API key is set
    if ! grep -q "OPENAI_API_KEY=" .env || grep -q "OPENAI_API_KEY=your_api_key_here" .env; then
        print_error "OpenAI API key not set in .env file"
        print_status "Please add your OpenAI API key to the .env file"
        exit 1
    fi
    
    print_status "OpenAI API key found"
}

# Function to clean up on exit
cleanup() {
    print_status "Cleaning up..."
    if [ -f "/tmp/ai_agent.sock" ]; then
        rm -f "/tmp/ai_agent.sock"
    fi
    deactivate 2>/dev/null
    print_status "Cleanup complete"
}

# Set up trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    print_status "Starting setup..."
    
    # Check Python
    check_python
    
    # Setup virtual environment
    setup_venv
    
    # Check for Helium
    check_helium
    
    # Check API key
    check_api_key
    
    # Start the AI agent in the background
    print_status "Starting AI agent..."
    python3 ai_agent.py &
    AI_AGENT_PID=$!
    
    # Wait for the agent to start
    sleep 2
    
    # Start the LockDown Browser bypass
    print_status "Starting LockDown Browser bypass..."
    python3 lockdown-bypass.py &
    BYPASS_PID=$!
    
    # Run the test script
    print_status "Running tests..."
    python3 test_agent.py
    
    # Wait for user input to exit
    print_status "System is running. Press Ctrl+C to exit."
    wait $AI_AGENT_PID $BYPASS_PID
}

# Run the main function
main 