#!/usr/bin/env python3
"""
M365 Copilot Connection Test
Quick test to validate setup before running full automation.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def test_selenium():
    """Test if Selenium is installed"""
    logger.info("Testing Selenium installation...")
    try:
        import selenium
        logger.info(f"✅ Selenium installed (version {selenium.__version__})")
        return True
    except ImportError:
        logger.error("❌ Selenium not installed")
        logger.error("   Install with: pip install selenium")
        return False

def test_edge_driver():
    """Test if Edge WebDriver is available"""
    logger.info("\nTesting Edge WebDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Edge(options=options)
        driver.quit()

        logger.info("✅ Edge WebDriver working correctly")
        return True
    except Exception as e:
        logger.error(f"❌ Edge WebDriver error: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("  macOS: brew install --cask microsoft-edge")
        logger.error("  Windows: Edge is pre-installed")
        logger.error("  Linux: Install Microsoft Edge from official repo")
        return False

def test_browser_launch():
    """Test if browser can launch and navigate"""
    logger.info("\nTesting browser launch and navigation...")
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options

        options = Options()
        # Use default profile (same as automation script)

        driver = webdriver.Edge(options=options)
        logger.info("✅ Browser launched successfully (default profile)")

        driver.get("https://www.microsoft.com")
        logger.info("✅ Navigation working")

        title = driver.title
        logger.info(f"✅ Page loaded: {title}")

        driver.quit()
        logger.info("✅ Browser closed cleanly")
        return True

    except Exception as e:
        logger.error(f"❌ Browser test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    logger.info("╔═══════════════════════════════════════════════════════════╗")
    logger.info("║   M365 Copilot Automation - Setup Validation             ║")
    logger.info("╚═══════════════════════════════════════════════════════════╝\n")

    tests = [
        ("Selenium Installation", test_selenium),
        ("Edge WebDriver", test_edge_driver),
        ("Browser Launch", test_browser_launch)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"❌ {name} test crashed: {e}")
            results.append((name, False))

    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")

    logger.info("="*60)
    logger.info(f"Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("\n🎉 All tests passed! You're ready to run the automation.")
        logger.info("   Run: python m365_copilot_automation.py")
        return True
    else:
        logger.info(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        logger.info("   Review M365_AUTOMATION_README.md for troubleshooting help")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
