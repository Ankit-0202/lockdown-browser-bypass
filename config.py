#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
APP_NAME = "Helium"
EXAM_URL = ""  # Add your exam URL here
WAIT_TIME = 15  # seconds to wait before first activation
PAGE_LOAD_TIMEOUT = 30  # seconds to wait for page load
SERVER_PORT = 5000
SERVER_HOST = "127.0.0.1"

# Process monitoring settings
MONITOR_INTERVAL = 5  # seconds between process checks
LOCKDOWN_PROCESS_NAMES = ["lockdown", "respondus", "itslearning"]

# API settings
API_VERSION = "1.0"
MAX_CONVERSATION_LENGTH = 1000
REQUEST_TIMEOUT = 30  # seconds

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4" if available
OPENAI_MAX_TOKENS = 1000
OPENAI_TEMPERATURE = 0.7

# Security settings
ALLOWED_ORIGINS = ["http://127.0.0.1:5000"]  # Only allow localhost

# Communication security
USE_UNIX_SOCKET = True  # Use Unix domain socket instead of TCP
SOCKET_PATH = "/tmp/ai_agent.sock"  # Unix socket path
ENCRYPTION_KEY = os.urandom(32)  # Random encryption key
USE_MEMORY_QUEUE = True  # Use in-memory queue for communication

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
