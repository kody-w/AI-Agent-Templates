#!/usr/bin/env python3
"""
Deal Progression Agent Stack - Demo Automation
Fully automated demo playback using Selenium with intelligent monitoring and controls.
"""

import time
import logging
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DealProgressionDemoAutomation:
    def __init__(self, demo_file_path=None):
        self.driver = None
        self.demo_file_path = demo_file_path or self._find_demo_file()
        self.demo_state = {
            'is_playing': False,
            'is_paused': False,
            'current_step': 0,
            'total_steps': 0,
            'messages_count': 0
        }

    def _find_demo_file(self):
        """Automatically find the demo HTML file"""
        # Get the directory of this script
        script_dir = Path(__file__).parent
        demo_path = script_dir / 'demos' / 'deal_progression_demo.html'

        if demo_path.exists():
            return str(demo_path.absolute())

        # Try alternative locations
        alternatives = [
            script_dir / 'deal_progression_demo.html',
            script_dir.parent / 'demos' / 'deal_progression_demo.html',
        ]

        for alt in alternatives:
            if alt.exists():
                return str(alt.absolute())

        raise FileNotFoundError("Could not find deal_progression_demo.html")

    def _setup_browser(self):
        """Initialize Chrome browser with proper configuration"""
        try:
            logger.info("Initializing Chrome browser...")
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Optionally run headless (comment out for visible browser)
            # options.add_argument("--headless")

            self.driver = webdriver.Chrome(options=options)
            logger.info("✅ Chrome browser initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error initializing browser: {e}")
            logger.info("💡 Make sure ChromeDriver is installed: brew install chromedriver")
            return False

    def load_demo(self):
        """Load the demo HTML file"""
        try:
            logger.info(f"📂 Loading demo file: {self.demo_file_path}")

            # Convert to file:// URL
            file_url = f"file://{self.demo_file_path}"
            self.driver.get(file_url)

            # Wait for page to load
            time.sleep(2)

            # Verify we're on the right page
            title = self.driver.title
            logger.info(f"✅ Demo loaded successfully")
            logger.info(f"   📄 Title: {title}")
            logger.info(f"   🔗 URL: {file_url}")

            return True

        except Exception as e:
            logger.error(f"❌ Error loading demo: {e}")
            return False

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"⚠️ Element not found: {value}")
            return None

    def get_demo_controls(self):
        """Get all demo control buttons"""
        try:
            controls = {
                'start': self.driver.find_element(By.ID, 'startBtn'),
                'pause': self.driver.find_element(By.ID, 'pauseBtn'),
                'reset': self.driver.find_element(By.ID, 'resetBtn'),
                'skip': self.driver.find_element(By.ID, 'skipBtn')
            }
            logger.info("✅ Found all demo control buttons")
            return controls
        except NoSuchElementException as e:
            logger.error(f"❌ Could not find demo controls: {e}")
            return None

    def get_status(self):
        """Get current demo status from the page"""
        try:
            status_text = self.driver.find_element(By.ID, 'statusText').text
            status_dot = self.driver.find_element(By.ID, 'statusDot')
            status_class = status_dot.get_attribute('class')

            return {
                'text': status_text,
                'class': status_class,
                'is_processing': 'processing' in status_class
            }
        except Exception as e:
            logger.warning(f"⚠️ Could not get status: {e}")
            return None

    def count_messages(self):
        """Count the number of messages currently displayed"""
        try:
            messages = self.driver.find_elements(By.CLASS_NAME, 'message')
            return len(messages)
        except Exception as e:
            logger.warning(f"⚠️ Could not count messages: {e}")
            return 0

    def is_typing_indicator_visible(self):
        """Check if typing indicator is visible"""
        try:
            typing = self.driver.find_element(By.ID, 'typingIndicator')
            return typing.is_displayed()
        except NoSuchElementException:
            return False

    def start_demo(self):
        """Start the demo playback"""
        try:
            logger.info("\n🎬 Starting demo playback...")

            controls = self.get_demo_controls()
            if not controls:
                return False

            # Click start button
            start_btn = controls['start']
            if start_btn.is_enabled():
                start_btn.click()
                logger.info("✅ Demo started")
                self.demo_state['is_playing'] = True
                return True
            else:
                logger.warning("⚠️ Start button is disabled")
                return False

        except Exception as e:
            logger.error(f"❌ Error starting demo: {e}")
            return False

    def pause_demo(self):
        """Pause the demo playback"""
        try:
            logger.info("⏸️ Pausing demo...")

            controls = self.get_demo_controls()
            if not controls:
                return False

            pause_btn = controls['pause']
            if pause_btn.is_enabled():
                pause_btn.click()
                logger.info("✅ Demo paused")
                self.demo_state['is_paused'] = True
                return True
            else:
                logger.warning("⚠️ Pause button is disabled")
                return False

        except Exception as e:
            logger.error(f"❌ Error pausing demo: {e}")
            return False

    def reset_demo(self):
        """Reset the demo to the beginning"""
        try:
            logger.info("🔄 Resetting demo...")

            controls = self.get_demo_controls()
            if not controls:
                return False

            reset_btn = controls['reset']
            reset_btn.click()
            logger.info("✅ Demo reset")
            self.demo_state['is_playing'] = False
            self.demo_state['is_paused'] = False
            self.demo_state['current_step'] = 0
            return True

        except Exception as e:
            logger.error(f"❌ Error resetting demo: {e}")
            return False

    def skip_to_next(self):
        """Skip to next message in demo"""
        try:
            logger.info("⏭️ Skipping to next message...")

            controls = self.get_demo_controls()
            if not controls:
                return False

            skip_btn = controls['skip']
            if skip_btn.is_enabled():
                skip_btn.click()
                logger.info("✅ Skipped to next message")
                return True
            else:
                logger.warning("⚠️ Skip button is disabled")
                return False

        except Exception as e:
            logger.error(f"❌ Error skipping: {e}")
            return False

    def monitor_demo_progress(self, check_interval=2, timeout=300):
        """
        Monitor demo progress and provide real-time updates

        Args:
            check_interval: Seconds between status checks
            timeout: Maximum seconds to wait for demo completion
        """
        logger.info("\n📊 Monitoring demo progress...")
        logger.info("=" * 70)

        start_time = time.time()
        last_message_count = 0

        while time.time() - start_time < timeout:
            try:
                # Get current status
                status = self.get_status()
                message_count = self.count_messages()
                is_typing = self.is_typing_indicator_visible()

                # Check for new messages
                if message_count > last_message_count:
                    new_messages = message_count - last_message_count
                    logger.info(f"📝 New message(s): {new_messages} (Total: {message_count})")
                    last_message_count = message_count

                # Check typing indicator
                if is_typing:
                    logger.info("⌨️  Agent is typing...")

                # Check status
                if status:
                    if status['text'] == 'Demo Complete':
                        logger.info("\n🎉 Demo completed successfully!")
                        logger.info(f"📊 Total messages displayed: {message_count}")
                        logger.info(f"⏱️  Total time: {time.time() - start_time:.1f} seconds")
                        return True
                    elif status['text'] == 'Paused':
                        logger.info("⏸️ Demo is paused")
                    elif status['is_processing']:
                        logger.info(f"🔄 Status: {status['text']}")

                time.sleep(check_interval)

            except Exception as e:
                logger.warning(f"⚠️ Error monitoring progress: {e}")
                time.sleep(check_interval)

        logger.warning(f"⏰ Monitoring timeout after {timeout} seconds")
        return False

    def capture_demo_content(self):
        """Capture and display demo content (messages and agent cards)"""
        try:
            logger.info("\n📸 Capturing demo content...")
            logger.info("=" * 70)

            messages = self.driver.find_elements(By.CLASS_NAME, 'message')

            for i, message in enumerate(messages, 1):
                try:
                    # Get message header
                    author = message.find_element(By.CLASS_NAME, 'message-author').text
                    content_elem = message.find_element(By.CLASS_NAME, 'message-content')
                    content = content_elem.text[:200]  # First 200 chars

                    logger.info(f"\n--- Message {i} ---")
                    logger.info(f"From: {author}")
                    logger.info(f"Content: {content}...")

                    # Check for agent card
                    try:
                        agent_card = message.find_element(By.CLASS_NAME, 'agent-card')
                        card_title = agent_card.find_element(By.CLASS_NAME, 'agent-card-title').text
                        logger.info(f"📊 Agent Card: {card_title}")
                    except NoSuchElementException:
                        pass

                except Exception as e:
                    logger.warning(f"⚠️ Error capturing message {i}: {e}")

            return True

        except Exception as e:
            logger.error(f"❌ Error capturing content: {e}")
            return False

    def run_full_demo(self, monitor=True, capture_content=False):
        """
        Run the complete demo with optional monitoring and content capture

        Args:
            monitor: Whether to monitor demo progress in real-time
            capture_content: Whether to capture and display demo content at the end
        """
        try:
            logger.info("\n" + "=" * 70)
            logger.info("Deal Progression Agent Stack - Demo Automation")
            logger.info("=" * 70)
            logger.info("This automation will:")
            logger.info("1. Load the demo HTML file in Chrome")
            logger.info("2. Start the demo playback automatically")
            logger.info("3. Monitor progress with real-time updates")
            logger.info("4. Capture and display demo content")
            logger.info("5. Complete the entire demo flow")
            logger.info("=" * 70)

            # Setup browser
            if not self._setup_browser():
                return False

            # Load demo
            if not self.load_demo():
                return False

            logger.info("\n⏳ Waiting 3 seconds for demo to fully load...")
            time.sleep(3)

            # Start demo
            if not self.start_demo():
                return False

            # Monitor progress
            if monitor:
                logger.info("\n🔍 Starting real-time monitoring...")
                logger.info("💡 Watch the browser window to see the demo in action!")
                self.monitor_demo_progress()
            else:
                # Just wait for a fixed time
                logger.info("\n⏳ Demo is playing... waiting 120 seconds...")
                time.sleep(120)

            # Capture content
            if capture_content:
                self.capture_demo_content()

            logger.info("\n✅ Demo automation completed successfully!")
            logger.info("🌐 Browser will remain open for manual inspection")

            return True

        except KeyboardInterrupt:
            logger.info("\n⚠️ Demo interrupted by user")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False

    def interactive_mode(self):
        """Run in interactive mode with manual control"""
        try:
            logger.info("\n" + "=" * 70)
            logger.info("Deal Progression Demo - Interactive Mode")
            logger.info("=" * 70)

            # Setup and load
            if not self._setup_browser():
                return False
            if not self.load_demo():
                return False

            logger.info("\n⏳ Demo loaded. Waiting 3 seconds...")
            time.sleep(3)

            while True:
                logger.info("\n" + "-" * 70)
                logger.info("Demo Controls:")
                logger.info("  1 - Start/Resume Demo")
                logger.info("  2 - Pause Demo")
                logger.info("  3 - Skip to Next Message")
                logger.info("  4 - Reset Demo")
                logger.info("  5 - Show Current Status")
                logger.info("  6 - Capture Demo Content")
                logger.info("  0 - Exit")
                logger.info("-" * 70)

                choice = input("\nEnter your choice: ").strip()

                if choice == '1':
                    self.start_demo()
                elif choice == '2':
                    self.pause_demo()
                elif choice == '3':
                    self.skip_to_next()
                elif choice == '4':
                    self.reset_demo()
                elif choice == '5':
                    status = self.get_status()
                    message_count = self.count_messages()
                    logger.info(f"\n📊 Current Status:")
                    logger.info(f"   Status: {status['text'] if status else 'Unknown'}")
                    logger.info(f"   Messages: {message_count}")
                elif choice == '6':
                    self.capture_demo_content()
                elif choice == '0':
                    logger.info("👋 Exiting interactive mode...")
                    break
                else:
                    logger.warning("⚠️ Invalid choice. Please try again.")

            return True

        except KeyboardInterrupt:
            logger.info("\n⚠️ Interactive mode interrupted")
            return False
        except Exception as e:
            logger.error(f"❌ Error in interactive mode: {e}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            logger.info("\n🧹 Cleaning up...")
            # Don't quit to keep browser open for inspection
            # self.driver.quit()
            logger.info("✅ Browser will remain open for inspection")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Deal Progression Demo Automation')
    parser.add_argument('--mode', choices=['auto', 'interactive'], default='auto',
                       help='Automation mode: auto (full automation) or interactive (manual control)')
    parser.add_argument('--demo-file', type=str, help='Path to demo HTML file')
    parser.add_argument('--no-monitor', action='store_true', help='Disable real-time monitoring')
    parser.add_argument('--capture', action='store_true', help='Capture demo content at the end')

    args = parser.parse_args()

    try:
        automation = DealProgressionDemoAutomation(demo_file_path=args.demo_file)

        if args.mode == 'auto':
            success = automation.run_full_demo(
                monitor=not args.no_monitor,
                capture_content=args.capture
            )
        else:
            success = automation.interactive_mode()

        if success:
            logger.info("\n🎉 Automation completed successfully!")
        else:
            logger.warning("\n⚠️ Automation completed with some issues")

    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
