#!/usr/bin/env python3

import sys
import time
import psutil
import logging
import threading
from datetime import datetime
import openai
from config import *
from encryption import SecureCommunication

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Configure OpenAI
if not OPENAI_API_KEY:
    logger.error("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY


class AIAgent:
    def __init__(self):
        self.is_active = False
        self.last_interaction = time.time()
        self.conversation_history = []
        self.start_time = None
        self.process_monitor = None
        self.secure_comm = SecureCommunication()
        self._setup_stealth()

    def _setup_stealth(self):
        """Setup stealth measures"""
        # Use secure communication headers
        self.headers = self.secure_comm.generate_stealth_headers()

        # Configure OpenAI to use our secure headers
        openai.api_requestor.APIRequestor._default_headers = self.headers

    def start(self):
        """Start the AI agent service"""
        self.is_active = True
        self.start_time = datetime.now()
        logger.info("AI Agent started - monitoring for interactions")

    def stop(self):
        """Stop the AI agent service"""
        self.is_active = False
        logger.info("AI Agent stopped")

    def process_query(self, query):
        """Process a query and return a response"""
        self.last_interaction = time.time()

        # Encrypt the query before adding to history
        encrypted_query = self.secure_comm.encrypt_message(query)

        # Add to conversation history
        self.conversation_history.append(
            {
                "role": "user",
                "content": encrypted_query,
                "timestamp": datetime.now().isoformat(),
            }
        )

        try:
            # Process the query using OpenAI API with stealth measures
            response = self._generate_response(query)

            # Encrypt the response
            encrypted_response = self.secure_comm.encrypt_message(response)

            # Add response to history
            self.conversation_history.append(
                {
                    "role": "assistant",
                    "content": encrypted_response,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Trim conversation history if needed
            if len(self.conversation_history) > MAX_CONVERSATION_LENGTH:
                self.conversation_history = self.conversation_history[
                    -MAX_CONVERSATION_LENGTH:
                ]

            return response
        except Exception as e:
            logger.error(f"Error processing query with OpenAI: {str(e)}")
            return f"Error: {str(e)}"

    def _generate_response(self, query):
        """Generate a response using OpenAI API with stealth measures"""
        try:
            # Prepare messages for the API
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ]

            # Add conversation history (decrypting each message)
            for msg in self.conversation_history[-10:]:  # Last 10 messages for context
                decrypted_content = self.secure_comm.decrypt_message(msg["content"])
                messages.append({"role": msg["role"], "content": decrypted_content})

            # Make API call with stealth measures
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=OPENAI_TEMPERATURE,
                request_timeout=REQUEST_TIMEOUT,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    def get_status(self):
        """Get the current status of the agent"""
        return {
            "active": self.is_active,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "last_interaction": datetime.fromtimestamp(
                self.last_interaction
            ).isoformat(),
            "conversation_length": len(self.conversation_history),
            "uptime": (
                (datetime.now() - self.start_time).total_seconds()
                if self.start_time
                else 0
            ),
            "model": OPENAI_MODEL,
        }


# Initialize the AI agent
agent = AIAgent()


def monitor_lockdown_browser():
    """Monitor LockDown Browser process"""
    while True:
        try:
            for proc in psutil.process_iter(["name", "pid"]):
                try:
                    name = proc.info["name"].lower()
                    if any(
                        lockdown_name in name
                        for lockdown_name in LOCKDOWN_PROCESS_NAMES
                    ):
                        logger.info(
                            f"LockDown Browser detected: {proc.info['name']} (PID: {proc.info['pid']})"
                        )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            logger.error(f"Error in process monitoring: {str(e)}")

        time.sleep(MONITOR_INTERVAL)


def main():
    try:
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_lockdown_browser, daemon=True)
        monitor_thread.start()

        # Start the AI agent
        agent.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        agent.stop()


if __name__ == "__main__":
    main()
