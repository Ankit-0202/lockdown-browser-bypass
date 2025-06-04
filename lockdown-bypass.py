#!/usr/bin/env python3

import os
import time
import json
import psutil
import logging
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from ai_agent import AIAgent

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class LockDownBypass:
    def __init__(self):
        self.driver = None
        self.ai_agent = AIAgent()  # Initialize AI agent
        self.is_running = False
        self.start_time = None
        self._setup_stealth()

    def _setup_stealth(self):
        """Setup stealth measures"""
        # Create a custom Chrome profile directory
        self.profile_dir = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Google",
            "Chrome",
            "Default",
        )
        os.makedirs(self.profile_dir, exist_ok=True)

        # Create a preferences file that looks like a normal browser
        preferences = {
            "profile": {
                "default_content_setting_values": {"notifications": 2},
                "password_manager_enabled": False,
            },
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }

        with open(os.path.join(self.profile_dir, "Preferences"), "w") as f:
            json.dump(preferences, f)

    def start(self):
        """Start the LockDown Browser bypass"""
        try:
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--user-data-dir={self.profile_dir}")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Start Chrome with Helium
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.chrome = {
                        runtime: {}
                    };
                """
                },
            )

            # Start the AI agent
            self.ai_agent.start()

            # Navigate to the exam URL
            self.driver.get(EXAM_URL)

            # Wait for the page to load
            WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            self.is_running = True
            self.start_time = datetime.now()
            logger.info("LockDown Browser bypass started successfully")

            # Start monitoring thread
            self.monitor_thread = threading.Thread(
                target=self._monitor_browser, daemon=True
            )
            self.monitor_thread.start()

            # Start question capture thread
            self.capture_thread = threading.Thread(
                target=self._capture_questions, daemon=True
            )
            self.capture_thread.start()

        except Exception as e:
            logger.error(f"Error starting LockDown Browser bypass: {str(e)}")
            self.stop()
            raise

    def stop(self):
        """Stop the LockDown Browser bypass"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        if self.ai_agent:
            self.ai_agent.stop()
        self.is_running = False
        logger.info("LockDown Browser bypass stopped")

    def _monitor_browser(self):
        """Monitor browser state"""
        while self.is_running:
            try:
                # Check if browser is still responsive
                self.driver.current_url

                # Check for LockDown Browser process
                for proc in psutil.process_iter(["name", "pid"]):
                    try:
                        name = proc.info["name"].lower()
                        if any(
                            lockdown_name in name
                            for lockdown_name in LOCKDOWN_PROCESS_NAMES
                        ):
                            logger.warning(
                                f"LockDown Browser detected: {proc.info['name']} (PID: {proc.info['pid']})"
                            )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

            except Exception as e:
                logger.error(f"Browser monitoring error: {str(e)}")
                self.stop()
                break

            time.sleep(MONITOR_INTERVAL)

    def _capture_questions(self):
        """Capture questions from the exam page"""
        while self.is_running:
            try:
                # Look for question elements (this will need to be customized based on the exam platform)
                question_elements = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".question-text, .question-content, [data-question]",
                )

                for element in question_elements:
                    try:
                        # Get the question text
                        question_text = element.text.strip()
                        if not question_text:
                            continue

                        # Process the question with AI agent
                        response = self.ai_agent.process_query(question_text)

                        # Display response in a stealthy way
                        self._display_response(response)

                    except Exception as e:
                        logger.error(f"Error processing question: {str(e)}")

            except Exception as e:
                logger.error(f"Error in question capture: {str(e)}")

            time.sleep(1)  # Check for new questions every second

    def _display_response(self, response):
        """Display AI response in a stealthy way"""
        try:
            # Create a temporary overlay that looks like a system notification
            script = """
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: system-ui;
                font-size: 14px;
                z-index: 9999;
                max-width: 300px;
                opacity: 0;
                transition: opacity 0.3s;
            `;
            overlay.textContent = arguments[0];
            document.body.appendChild(overlay);
            
            // Fade in
            setTimeout(() => overlay.style.opacity = '1', 100);
            
            // Remove after 5 seconds
            setTimeout(() => {
                overlay.style.opacity = '0';
                setTimeout(() => overlay.remove(), 300);
            }, 5000);
            """

            self.driver.execute_script(script, response)

        except Exception as e:
            logger.error(f"Error displaying response: {str(e)}")

    def get_status(self):
        """Get the current status of the bypass"""
        return {
            "running": self.is_running,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime": (
                (datetime.now() - self.start_time).total_seconds()
                if self.start_time
                else 0
            ),
            "current_url": self.driver.current_url if self.driver else None,
            "ai_agent_status": self.ai_agent.get_status() if self.ai_agent else None,
        }


def main():
    try:
        # Start the bypass
        bypass = LockDownBypass()
        bypass.start()

        # Keep the main thread alive
        while bypass.is_running:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        if "bypass" in locals():
            bypass.stop()


if __name__ == "__main__":
    main()
