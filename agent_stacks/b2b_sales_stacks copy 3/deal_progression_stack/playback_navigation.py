#!/usr/bin/env python3
"""
M365 Copilot Navigation Playback
Replays recorded navigation actions to get to the chat interface.
"""

import time
import json
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NavigationPlayback:
    def __init__(self, recording_file=None):
        self.driver = None
        self.recording_file = recording_file or Path(__file__).parent / "navigation_recording.json"
        self.recording_data = None

    def _setup_browser(self):
        """Initialize Edge with default profile"""
        logger.info("🚀 Opening Edge browser with your default profile...")
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        logger.info("✅ Browser ready")

    def load_recording(self):
        """Load the recorded actions"""
        if not self.recording_file.exists():
            logger.error(f"❌ Recording file not found: {self.recording_file}")
            logger.error("   Run 'python record_navigation.py' first to create a recording")
            return False

        try:
            with open(self.recording_file, 'r') as f:
                self.recording_data = json.load(f)

            logger.info("✅ Recording loaded successfully")
            logger.info(f"   Recorded: {self.recording_data.get('recorded_at')}")
            logger.info(f"   Actions: {self.recording_data.get('total_actions')}")
            logger.info(f"   Start URL: {self.recording_data.get('start_url')}")
            logger.info(f"   Final URL: {self.recording_data.get('final_url')}")
            return True

        except Exception as e:
            logger.error(f"❌ Error loading recording: {e}")
            return False

    def playback(self):
        """Playback the recorded actions"""
        if not self.recording_data:
            logger.error("❌ No recording data loaded")
            return False

        actions = self.recording_data.get('actions', [])
        if not actions:
            logger.error("❌ No actions to playback")
            return False

        logger.info(f"\n{'='*70}")
        logger.info("▶️  PLAYING BACK NAVIGATION")
        logger.info(f"{'='*70}")
        logger.info(f"Will execute {len(actions)} recorded actions")
        logger.info(f"{'='*70}\n")

        success_count = 0
        failed_count = 0

        for i, action in enumerate(actions, 1):
            action_type = action.get('type')
            data = action.get('data', {})

            logger.info(f"\n[{i}/{len(actions)}] {action_type}: {data}")

            try:
                if action_type == 'navigate':
                    url = data.get('url')
                    logger.info(f"🔗 Navigating to: {url}")
                    self.driver.get(url)
                    time.sleep(2)  # Wait for page load
                    success_count += 1

                elif action_type == 'wait':
                    seconds = data.get('seconds', 2)
                    logger.info(f"⏳ Waiting {seconds} seconds...")
                    time.sleep(seconds)
                    success_count += 1

                elif action_type == 'click':
                    selector = data.get('selector')
                    method = data.get('method', 'css')

                    logger.info(f"🖱️  Clicking element: {selector}")

                    if method == 'css':
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    else:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )

                    element.click()
                    time.sleep(1)
                    success_count += 1

                elif action_type == 'type':
                    text = data.get('text')
                    logger.info(f"⌨️  Typing text: {text}")

                    # Assume active element or find input field
                    try:
                        # Try to find an input field that's visible
                        inputs = self.driver.find_elements(By.CSS_SELECTOR,
                            "input[type='text'], input[type='email'], input[type='password'], textarea")

                        for inp in inputs:
                            if inp.is_displayed() and inp.is_enabled():
                                inp.send_keys(text)
                                time.sleep(0.5)
                                break
                    except:
                        # Fallback: use active element
                        self.driver.switch_to.active_element.send_keys(text)

                    success_count += 1

                elif action_type == 'checkpoint':
                    note = data.get('note', 'Checkpoint')
                    logger.info(f"📌 Checkpoint: {note}")
                    logger.info(f"   Current URL: {self.driver.current_url}")
                    success_count += 1

                elif action_type == 'final_checkpoint':
                    logger.info(f"🏁 Final checkpoint reached")
                    logger.info(f"   URL: {self.driver.current_url}")
                    logger.info(f"   Title: {self.driver.title}")
                    success_count += 1

                else:
                    logger.warning(f"⚠️  Unknown action type: {action_type}")

            except Exception as e:
                logger.error(f"❌ Action failed: {e}")
                failed_count += 1

                # Ask if should continue
                if failed_count > 3:
                    logger.error("❌ Too many failures, stopping playback")
                    return False

                retry = input("\nContinue playback? (y/n): ").strip().lower()
                if retry != 'y':
                    logger.info("⚠️  Playback cancelled by user")
                    return False

        # Summary
        logger.info(f"\n{'='*70}")
        logger.info("📊 PLAYBACK SUMMARY")
        logger.info(f"{'='*70}")
        logger.info(f"✅ Successful: {success_count}/{len(actions)}")
        logger.info(f"❌ Failed: {failed_count}/{len(actions)}")
        logger.info(f"🔗 Final URL: {self.driver.current_url}")
        logger.info(f"{'='*70}\n")

        return failed_count == 0

    def run(self, keep_open=True):
        """Main entry point"""
        try:
            logger.info("╔═══════════════════════════════════════════════════════════════════╗")
            logger.info("║   M365 Copilot Navigation Playback                               ║")
            logger.info("╚═══════════════════════════════════════════════════════════════════╝\n")

            if not self.load_recording():
                return False

            self._setup_browser()

            success = self.playback()

            if success:
                logger.info("✅ Playback completed successfully!")
                logger.info("   Chat interface should be ready")

                if keep_open:
                    logger.info("\n💡 Browser will stay open for you to verify")
                    logger.info("   Close it manually when done\n")
                    input("Press ENTER to close...")

                return True
            else:
                logger.error("❌ Playback completed with errors")
                logger.info("\n💡 Browser will stay open for troubleshooting")
                input("Press ENTER to close...")
                return False

        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if not keep_open and self.driver:
                self.driver.quit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Playback M365 Copilot navigation recording')
    parser.add_argument('--recording', '-r', type=str,
                       help='Path to recording file (default: navigation_recording.json)')
    parser.add_argument('--no-wait', action='store_true',
                       help='Close browser automatically after playback')

    args = parser.parse_args()

    playback = NavigationPlayback(recording_file=args.recording)
    playback.run(keep_open=not args.no_wait)
