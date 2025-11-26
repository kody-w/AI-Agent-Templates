#!/usr/bin/env python3
"""
M365 Copilot Navigation Recorder
Records your clicks and actions to get to the chat interface,
then saves them for automatic replay.
"""

import time
import json
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NavigationRecorder:
    def __init__(self):
        self.driver = None
        self.actions = []
        self.recording = False
        self.start_url = "https://m365.cloud.microsoft/chat"
        self.recording_file = Path(__file__).parent / "navigation_recording.json"

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

    def record_action(self, action_type: str, data: dict):
        """Record an action"""
        action = {
            "type": action_type,
            "timestamp": time.time(),
            "url": self.driver.current_url,
            "data": data
        }
        self.actions.append(action)
        logger.info(f"📝 Recorded: {action_type} - {data}")

    def start_recording(self):
        """Start the recording session"""
        logger.info("\n" + "="*70)
        logger.info("🎬 M365 COPILOT NAVIGATION RECORDER")
        logger.info("="*70)
        logger.info("This tool will record your actions to reach the chat interface.")
        logger.info("")
        logger.info("Instructions:")
        logger.info("  1. Browser will open to M365 Copilot")
        logger.info("  2. Complete any sign-in steps")
        logger.info("  3. Click through any popups/dialogs")
        logger.info("  4. Navigate to the chat interface")
        logger.info("  5. STOP when you see the message input field")
        logger.info("")
        logger.info("Recording will track:")
        logger.info("  • URL navigations")
        logger.info("  • Button clicks (you'll mark them)")
        logger.info("  • Wait times")
        logger.info("  • Page transitions")
        logger.info("")
        logger.info("="*70)

        self._setup_browser()

        # Record initial navigation
        logger.info(f"\n📍 Navigating to {self.start_url}")
        self.driver.get(self.start_url)
        self.record_action("navigate", {"url": self.start_url})

        logger.info("\n✅ Browser is ready. Now recording your actions...")
        logger.info("="*70)

        self.recording = True
        self._interactive_recording()

    def _interactive_recording(self):
        """Interactive recording mode with manual action logging"""
        logger.info("\n🎯 INTERACTIVE RECORDING MODE")
        logger.info("="*70)
        logger.info("Commands:")
        logger.info("  w [seconds] - Wait for [seconds] (e.g., 'w 3' waits 3 seconds)")
        logger.info("  c [selector] - Record a click on element with CSS selector")
        logger.info("  t [text] - Record typing text")
        logger.info("  n [url] - Record navigation to URL")
        logger.info("  m - Mark current page/state (useful for checkpoints)")
        logger.info("  s - Show recorded actions so far")
        logger.info("  d - Done recording (save and exit)")
        logger.info("  h - Show this help again")
        logger.info("")
        logger.info("💡 TIP: Just interact with the browser normally, then use")
        logger.info("   these commands to describe what you did!")
        logger.info("="*70)

        step = 1

        while self.recording:
            try:
                logger.info(f"\n[Step {step}] Current URL: {self.driver.current_url[:80]}...")

                cmd = input("\nCommand (h for help): ").strip()

                if not cmd:
                    continue

                parts = cmd.split(maxsplit=1)
                action = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None

                if action == 'h':
                    logger.info("\nCommands:")
                    logger.info("  w [seconds] - Wait")
                    logger.info("  c [selector] - Click element")
                    logger.info("  t [text] - Type text")
                    logger.info("  n [url] - Navigate to URL")
                    logger.info("  m - Mark checkpoint")
                    logger.info("  s - Show actions")
                    logger.info("  d - Done (save)")

                elif action == 'w':
                    seconds = float(arg) if arg else 2.0
                    logger.info(f"⏳ Waiting {seconds} seconds...")
                    time.sleep(seconds)
                    self.record_action("wait", {"seconds": seconds})

                elif action == 'c':
                    if not arg:
                        logger.error("❌ Please provide CSS selector: c [selector]")
                        continue
                    logger.info(f"🖱️  Recording click on: {arg}")
                    self.record_action("click", {"selector": arg, "method": "css"})

                elif action == 't':
                    if not arg:
                        logger.error("❌ Please provide text: t [text]")
                        continue
                    logger.info(f"⌨️  Recording text input: {arg}")
                    self.record_action("type", {"text": arg})

                elif action == 'n':
                    if not arg:
                        logger.error("❌ Please provide URL: n [url]")
                        continue
                    logger.info(f"🔗 Recording navigation to: {arg}")
                    current_url = self.driver.current_url
                    self.record_action("navigate", {"url": arg, "from": current_url})

                elif action == 'm':
                    logger.info("📌 Marking checkpoint...")
                    self.record_action("checkpoint", {
                        "url": self.driver.current_url,
                        "title": self.driver.title,
                        "note": arg if arg else f"Checkpoint {step}"
                    })

                elif action == 's':
                    logger.info(f"\n📋 Recorded Actions ({len(self.actions)} total):")
                    logger.info("="*70)
                    for i, act in enumerate(self.actions, 1):
                        logger.info(f"{i}. {act['type']}: {act['data']}")
                    logger.info("="*70)

                elif action == 'd':
                    logger.info("\n✅ Finishing recording...")
                    self._finish_recording()
                    break

                else:
                    logger.warning(f"⚠️  Unknown command: {cmd}")
                    logger.info("Type 'h' for help")
                    continue

                step += 1

            except KeyboardInterrupt:
                logger.info("\n⚠️  Recording interrupted")
                if input("\nSave recording? (y/n): ").lower() == 'y':
                    self._finish_recording()
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")

    def _finish_recording(self):
        """Finalize and save the recording"""
        if not self.actions:
            logger.warning("⚠️  No actions recorded!")
            return

        # Add final checkpoint
        self.record_action("final_checkpoint", {
            "url": self.driver.current_url,
            "title": self.driver.title,
            "total_actions": len(self.actions)
        })

        # Save to file
        recording_data = {
            "version": "1.0",
            "recorded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "start_url": self.start_url,
            "final_url": self.driver.current_url,
            "total_actions": len(self.actions),
            "actions": self.actions
        }

        with open(self.recording_file, 'w') as f:
            json.dump(recording_data, f, indent=2)

        logger.info(f"\n✅ Recording saved to: {self.recording_file}")
        logger.info(f"📊 Total actions: {len(self.actions)}")
        logger.info("")
        logger.info("="*70)
        logger.info("🎉 Recording Complete!")
        logger.info("="*70)
        logger.info("Next steps:")
        logger.info("  1. Review the recording: cat navigation_recording.json")
        logger.info("  2. Test playback: python playback_navigation.py")
        logger.info("  3. Use in automation: python m365_copilot_automation.py")
        logger.info("="*70)

        self.recording = False

        # Keep browser open
        logger.info("\n💡 Browser will stay open for your review")
        logger.info("   Close it manually when done\n")

    def run(self):
        """Main entry point"""
        try:
            self.start_recording()
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver and not self.recording:
                logger.info("\n🧹 Keeping browser open for review...")

if __name__ == "__main__":
    recorder = NavigationRecorder()
    recorder.run()
