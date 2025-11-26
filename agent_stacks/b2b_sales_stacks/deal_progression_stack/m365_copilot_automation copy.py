#!/usr/bin/env python3
"""
M365 Copilot - Deal Progression Automation
Simulates the deal progression conversation from the demo with real M365 Copilot.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class M365DealProgressionAutomation:
    def __init__(self, debug_port=9222):
        self.driver = None
        self.debug_port = debug_port
        self.last_input_element = None

        # Deal Progression conversation flow from demo
        self.conversation = [
            {
                "message": "Show me all stalled deals in our pipeline and assess the overall health risks",
                "context": "Analyzing pipeline for stalled deals and risk assessment"
            },
            {
                "message": "What's the health score for the Contoso Enterprise Suite deal? I'm concerned about its progress.",
                "context": "Calculating health score for Contoso Enterprise Suite"
            },
            {
                "message": "Analyze the stakeholder engagement for this deal. Who should we be talking to?",
                "context": "Analyzing stakeholder engagement patterns"
            },
            {
                "message": "What's our win probability for this deal, and what are the main factors affecting it?",
                "context": "Calculating AI-driven win probability"
            },
            {
                "message": "Recommend the next best actions to save this deal",
                "context": "Generating recovery plan with prioritized actions"
            }
        ]

    def _get_edge_options(self):
        """Get Edge browser options with debugging enabled"""
        options = Options()
        options.add_argument(f"--remote-debugging-port={self.debug_port}")
        # Use default profile (already signed in) instead of InPrivate
        # Note: This will use your existing Edge profile with saved credentials
        # Disable automation flags to appear more natural
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        return options

    def _setup_browser(self):
        """Initialize the Edge browser"""
        try:
            logger.info("Attempting to reuse existing Edge session...")
            options = self._get_edge_options()
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.debug_port}")

            try:
                self.driver = webdriver.Edge(options=options)
                logger.info("✅ Connected to existing Edge session")
                return True
            except:
                logger.info("No existing session found, creating new session...")

        except Exception as e:
            logger.info("No existing Edge processes found")

        # Create new session with default profile (already authenticated)
        logger.info("Creating new Edge session with default profile...")
        options = self._get_edge_options()

        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        logger.info("✅ Edge browser initialized with default profile")
        logger.info("   Using existing authentication from your Edge profile")
        return True

    def _find_input_field(self):
        """Find the M365 Copilot chat input field"""
        logger.info("🔍 Detecting chat input field...")

        # If we have a cached working element, try it first
        if self.last_input_element:
            try:
                if self.last_input_element.is_displayed() and self.last_input_element.is_enabled():
                    logger.info("✅ Using cached input field")
                    return self.last_input_element
            except:
                self.last_input_element = None

        # M365 Copilot input field selectors (prioritized)
        selectors = [
            # Contenteditable elements (most common in M365 Copilot)
            "div[contenteditable='true'][role='textbox']",
            "span[contenteditable='true'][role='textbox']",
            "div[contenteditable='true']",
            "span[contenteditable='true']",

            # Role-based selectors
            "*[role='textbox'][contenteditable='true']",
            "*[role='textbox']",

            # Class-based patterns
            "div[class*='composer']",
            "div[class*='input']",
            "div[class*='textbox']",

            # Textarea fallback
            "textarea[placeholder*='Ask']",
            "textarea[placeholder*='Message']",
            "textarea",

            # Data attributes
            "*[data-testid*='composer']",
            "*[data-testid*='input']",
            "*[aria-label*='message' i]",
            "*[aria-label*='ask' i]"
        ]

        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            # Test if it can accept input
                            original_text = element.text or element.get_attribute("textContent") or ""
                            element.send_keys(".")
                            time.sleep(0.3)

                            new_text = element.text or element.get_attribute("textContent") or ""
                            if len(new_text) > len(original_text):
                                # Clear the test input
                                element.send_keys(Keys.BACKSPACE)
                                logger.info(f"✅ Found input field: <{element.tag_name}> with selector: {selector}")
                                self.last_input_element = element
                                return element
                            else:
                                # Try to clear
                                try:
                                    element.send_keys(Keys.BACKSPACE)
                                except:
                                    pass
                    except:
                        continue
            except:
                continue

        logger.error("❌ Could not find input field")
        return None

    def _send_message(self, message: str, context: str = "") -> bool:
        """Send a message to M365 Copilot"""
        logger.info(f"\n{'='*70}")
        logger.info(f"💬 Sending: {message}")
        if context:
            logger.info(f"📋 Context: {context}")
        logger.info(f"{'='*70}")

        # Find input field
        input_field = self._find_input_field()
        if not input_field:
            logger.error("❌ Could not find input field")
            return False

        try:
            # Clear any existing content
            try:
                input_field.clear()
            except:
                # For contenteditable, clear differently
                input_field.send_keys(Keys.CONTROL + "a")
                input_field.send_keys(Keys.BACKSPACE)

            time.sleep(0.5)

            # Type the message slowly to appear more natural
            for char in message:
                input_field.send_keys(char)
                time.sleep(0.02)  # 20ms delay between characters

            logger.info("✅ Message typed successfully")
            time.sleep(1)

            # Try to find and click send button
            send_button = self._find_send_button()

            if send_button:
                send_button.click()
                logger.info("✅ Message sent via send button")
            else:
                # Fallback: try Enter key
                input_field.send_keys(Keys.RETURN)
                logger.info("✅ Message sent via Enter key")

            return True

        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False

    def _find_send_button(self):
        """Find the send button"""
        send_selectors = [
            "button[aria-label*='Send' i]",
            "button[title*='Send' i]",
            "button[data-testid*='send' i]",
            "button[type='submit']",
            "*[role='button'][aria-label*='Send' i]"
        ]

        for selector in send_selectors:
            try:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for btn in buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn_label = (btn.get_attribute("aria-label") or
                                   btn.get_attribute("title") or "").lower()
                        if "send" in btn_label:
                            return btn
            except:
                continue

        return None

    def _wait_for_response(self, timeout: int = 60) -> bool:
        """Wait for Copilot to complete its response"""
        logger.info("⏳ Waiting for Copilot response...")

        # Get initial content snapshot
        initial_content = self._get_page_content()
        initial_length = len(initial_content)

        start_time = time.time()
        last_length = initial_length
        stable_count = 0
        response_detected = False

        while time.time() - start_time < timeout:
            try:
                # Check for typing/thinking indicators
                if self._is_copilot_thinking():
                    logger.info("⌨️  Copilot is thinking...")
                    stable_count = 0
                    response_detected = True
                    time.sleep(2)
                    continue

                # Check content changes
                current_content = self._get_page_content()
                current_length = len(current_content)
                growth = current_length - initial_length

                # Response detected if significant growth
                if growth > 100:
                    response_detected = True

                    # Check if content is stable
                    if current_length == last_length:
                        stable_count += 1
                        logger.info(f"✅ Response stable ({stable_count}/3) - {current_length} chars (+{growth})")

                        if stable_count >= 3:
                            logger.info("✅ Response complete!")
                            return True
                    else:
                        stable_count = 0
                        logger.info(f"📝 Response in progress... {current_length} chars (+{growth})")

                    last_length = current_length

                time.sleep(2)

            except Exception as e:
                logger.warning(f"⚠️  Error waiting: {e}")
                time.sleep(2)

        if response_detected:
            logger.warning(f"⏰ Timeout but response was detected - continuing")
            return True
        else:
            logger.warning(f"⏰ No response detected after {timeout}s")
            return False

    def _is_copilot_thinking(self) -> bool:
        """Check if Copilot is currently processing"""
        thinking_selectors = [
            "*[class*='typing' i]",
            "*[class*='thinking' i]",
            "*[class*='loading' i]",
            "*[class*='processing' i]",
            "*[class*='generating' i]",
            "*[aria-label*='typing' i]",
            "*[aria-label*='thinking' i]",
            "*[aria-label*='generating' i]",
            "*[data-testid*='typing' i]",
            "*[data-testid*='loading' i]"
        ]

        for selector in thinking_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if any(el.is_displayed() for el in elements):
                    return True
            except:
                continue

        return False

    def _get_page_content(self) -> str:
        """Get current page content"""
        content_selectors = [
            "*[role='main']",
            "main",
            "*[class*='conversation' i]",
            "*[class*='chat' i]",
            "*[class*='messages' i]",
            "body"
        ]

        for selector in content_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return elements[0].text
            except:
                continue

        return ""

    def navigate_to_copilot(self) -> bool:
        """Navigate to M365 Copilot"""
        try:
            logger.info("🚀 Initializing M365 Copilot session...")

            if not self._setup_browser():
                return False

            logger.info("📍 Navigating to M365 Copilot...")
            self.driver.get("https://m365.cloud.microsoft/chat")
            time.sleep(5)

            logger.info("✅ Successfully navigated to M365 Copilot")
            logger.info(f"   📄 Title: {self.driver.title}")
            logger.info(f"   🔗 URL: {self.driver.current_url}")

            return True

        except Exception as e:
            logger.error(f"❌ Navigation error: {e}")
            return False

    def wait_for_authentication(self) -> bool:
        """Wait for page to load (authentication should already be done via default profile)"""
        logger.info(f"\n{'='*70}")
        logger.info("⏳ WAITING FOR COPILOT INTERFACE TO LOAD")
        logger.info(f"{'='*70}")
        logger.info("Using your default Edge profile (already signed in)")
        logger.info("")
        logger.info("If the page loads automatically:")
        logger.info("  ✅ Great! Just press ENTER to start")
        logger.info("")
        logger.info("If you need to sign in:")
        logger.info("  1. Complete sign-in in the browser window")
        logger.info("  2. Wait for chat interface to load")
        logger.info("  3. Then press ENTER")
        logger.info(f"{'='*70}")
        logger.info("Press ENTER when you see the chat interface...")
        logger.info(f"{'='*70}\n")

        try:
            input()
            logger.info("✅ Ready to start - beginning automation")
            return True
        except KeyboardInterrupt:
            logger.info("\n❌ Cancelled by user")
            return False

    def run_deal_progression_conversation(self) -> bool:
        """Execute the complete deal progression conversation"""
        logger.info(f"\n{'='*70}")
        logger.info("🎯 DEAL PROGRESSION INTELLIGENCE CONVERSATION")
        logger.info(f"{'='*70}")
        logger.info(f"Will ask {len(self.conversation)} questions about:")
        logger.info("  • Stalled deals and pipeline health")
        logger.info("  • Deal health scoring")
        logger.info("  • Stakeholder engagement analysis")
        logger.info("  • Win probability assessment")
        logger.info("  • Recovery action recommendations")
        logger.info(f"{'='*70}\n")

        # Give interface time to settle
        logger.info("⏳ Allowing interface to fully load...")
        time.sleep(5)

        successful = 0
        failed = 0

        for i, turn in enumerate(self.conversation, 1):
            logger.info(f"\n🔄 Question {i}/{len(self.conversation)}")

            # Send message
            if self._send_message(turn["message"], turn["context"]):
                # Wait for response
                if self._wait_for_response(timeout=90):
                    successful += 1
                    logger.info(f"✅ Turn {i} completed successfully\n")

                    # Wait before next question
                    if i < len(self.conversation):
                        wait_time = 8
                        logger.info(f"⏳ Waiting {wait_time}s before next question...")
                        for countdown in range(wait_time, 0, -1):
                            print(f"   Next question in {countdown}s...   ", end='\r')
                            time.sleep(1)
                        print(f"   Ready for next question!            ")
                else:
                    logger.warning(f"⚠️  Turn {i} - response timeout, continuing...")
                    successful += 1  # Count as success since message was sent
            else:
                failed += 1
                logger.error(f"❌ Turn {i} failed")

                # Retry logic
                logger.info("🔄 Attempting retry...")
                time.sleep(3)

                if self._send_message(turn["message"], turn["context"]):
                    if self._wait_for_response(timeout=90):
                        successful += 1
                        failed -= 1
                        logger.info(f"✅ Turn {i} succeeded on retry\n")
                    else:
                        logger.warning(f"⚠️  Turn {i} retry - response timeout\n")
                else:
                    logger.error(f"❌ Turn {i} retry also failed\n")

        # Summary
        logger.info(f"\n{'='*70}")
        logger.info("📊 CONVERSATION SUMMARY")
        logger.info(f"{'='*70}")
        logger.info(f"✅ Successful: {successful}/{len(self.conversation)}")
        logger.info(f"❌ Failed: {failed}/{len(self.conversation)}")

        if successful == len(self.conversation):
            logger.info("🎉 Perfect! All questions completed successfully!")
        elif successful > 0:
            logger.info("✅ Conversation completed with some successes")
        else:
            logger.info("❌ No questions completed successfully")

        logger.info(f"{'='*70}\n")

        return successful > 0

    def run(self):
        """Main execution method"""
        try:
            logger.info("╔═══════════════════════════════════════════════════════════════════╗")
            logger.info("║   M365 Copilot - Deal Progression Intelligence Automation        ║")
            logger.info("╚═══════════════════════════════════════════════════════════════════╝")
            logger.info("")
            logger.info("This automation will:")
            logger.info("  1. Open Edge with your default profile (already signed in)")
            logger.info("  2. Navigate to M365 Copilot chat interface")
            logger.info("  3. Automatically conduct deal progression conversation")
            logger.info("  4. Ask 5 intelligent questions about deal health")
            logger.info("  5. Wait for and detect Copilot responses")
            logger.info("")
            logger.info("💡 Using your existing Edge profile - no re-authentication needed!")
            logger.info("")
            logger.info("════════════════════════════════════════════════════════════════════")

            # Navigate
            if not self.navigate_to_copilot():
                logger.error("❌ Failed to navigate to Copilot")
                return False

            # Wait for auth
            if not self.wait_for_authentication():
                logger.error("❌ Authentication not completed")
                return False

            # Run conversation
            logger.info("\n🚀 Starting automated conversation...")
            logger.info("   From this point, everything runs automatically!")
            logger.info("   Sit back and watch the magic happen ✨\n")

            success = self.run_deal_progression_conversation()

            if success:
                logger.info("\n🎉 Automation completed successfully!")
                logger.info("💡 Browser will remain open for your review")
            else:
                logger.info("\n⚠️  Automation encountered issues")
                logger.info("🔍 Check the logs above for details")

            return success

        except KeyboardInterrupt:
            logger.info("\n⚠️  Interrupted by user")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if self.driver:
                logger.info("\n🧹 Session complete - browser remains open")
                # Keep browser open for review

if __name__ == "__main__":
    automation = M365DealProgressionAutomation()
    automation.run()
