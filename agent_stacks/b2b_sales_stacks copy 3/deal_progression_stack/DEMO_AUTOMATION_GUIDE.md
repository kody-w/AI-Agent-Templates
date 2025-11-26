# Demo Automation Guide

## Overview

The `run_demo_automation.py` script provides fully automated playback of the Deal Progression Agent Stack demo with intelligent monitoring and control capabilities.

## Features

✅ **Automated Demo Playback** - Automatically loads and plays the demo
✅ **Real-time Monitoring** - Tracks demo progress with live updates
✅ **Interactive Mode** - Manual control over demo playback
✅ **Content Capture** - Extracts and displays demo content
✅ **Smart Detection** - Automatically finds demo HTML file
✅ **Browser Persistence** - Keeps browser open for manual inspection

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements_demo.txt
```

Or manually:
```bash
pip install selenium webdriver-manager
```

### 2. Install ChromeDriver

**macOS**:
```bash
brew install chromedriver
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# Or download from: https://chromedriver.chromium.org/
```

**Windows**:
```bash
# Download from: https://chromedriver.chromium.org/
# Add to PATH
```

## Usage

### Automatic Mode (Recommended)

Run the full demo with automated playback and monitoring:

```bash
python run_demo_automation.py
```

Or make it executable and run:
```bash
./run_demo_automation.py
```

**What happens:**
1. ✅ Loads demo HTML in Chrome
2. ✅ Automatically clicks "Start Demo"
3. ✅ Monitors progress in real-time
4. ✅ Displays message count updates
5. ✅ Detects when demo completes
6. ✅ Keeps browser open for inspection

**Sample Output:**
```
======================================================================
Deal Progression Agent Stack - Demo Automation
======================================================================
This automation will:
1. Load the demo HTML file in Chrome
2. Start the demo playback automatically
3. Monitor progress with real-time updates
4. Capture and display demo content
5. Complete the entire demo flow
======================================================================

2025-10-25 14:30:15 - INFO - Initializing Chrome browser...
2025-10-25 14:30:16 - INFO - ✅ Chrome browser initialized successfully
2025-10-25 14:30:16 - INFO - 📂 Loading demo file: /Users/kodyw/.../deal_progression_demo.html
2025-10-25 14:30:18 - INFO - ✅ Demo loaded successfully
2025-10-25 14:30:18 - INFO -    📄 Title: M365 Copilot - Deal Progression
2025-10-25 14:30:21 - INFO - 🎬 Starting demo playback...
2025-10-25 14:30:21 - INFO - ✅ Demo started

📊 Monitoring demo progress...
======================================================================
2025-10-25 14:30:23 - INFO - 📝 New message(s): 1 (Total: 1)
2025-10-25 14:30:25 - INFO - ⌨️  Agent is typing...
2025-10-25 14:30:30 - INFO - 📝 New message(s): 1 (Total: 2)
2025-10-25 14:30:35 - INFO - 📝 New message(s): 1 (Total: 3)
...
2025-10-25 14:32:45 - INFO - 🎉 Demo completed successfully!
2025-10-25 14:32:45 - INFO - 📊 Total messages displayed: 20
2025-10-25 14:32:45 - INFO - ⏱️  Total time: 144.2 seconds
```

### Interactive Mode

For manual control over demo playback:

```bash
python run_demo_automation.py --mode interactive
```

**Interactive Menu:**
```
----------------------------------------------------------------------
Demo Controls:
  1 - Start/Resume Demo
  2 - Pause Demo
  3 - Skip to Next Message
  4 - Reset Demo
  5 - Show Current Status
  6 - Capture Demo Content
  0 - Exit
----------------------------------------------------------------------

Enter your choice:
```

### Advanced Options

**Disable monitoring** (just play and wait):
```bash
python run_demo_automation.py --no-monitor
```

**Capture demo content** at the end:
```bash
python run_demo_automation.py --capture
```

**Specify custom demo file**:
```bash
python run_demo_automation.py --demo-file /path/to/custom_demo.html
```

**Combine options**:
```bash
python run_demo_automation.py --capture --no-monitor
```

## How It Works

### 1. Automatic Demo Detection

The script automatically finds the demo HTML file:
```python
# Looks in these locations (in order):
1. ./demos/deal_progression_demo.html
2. ./deal_progression_demo.html
3. ../demos/deal_progression_demo.html
```

### 2. Browser Automation

Uses Selenium to:
- Open Chrome browser
- Load the demo HTML file (file:// URL)
- Find and click demo control buttons
- Monitor page state changes
- Detect typing indicators
- Count messages displayed

### 3. Real-time Monitoring

Monitors:
- ✅ **Status indicator** - Checks statusText element for "Demo Complete"
- ✅ **Message count** - Counts .message elements on the page
- ✅ **Typing indicator** - Detects #typingIndicator element
- ✅ **Button states** - Checks which control buttons are enabled

### 4. Smart Controls

Finds and interacts with demo controls:
- `#startBtn` - Start demo playback
- `#pauseBtn` - Pause demo
- `#resetBtn` - Reset to beginning
- `#skipBtn` - Skip to next message

## Troubleshooting

### ChromeDriver Not Found

**Error**: `selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solution**:
```bash
# macOS
brew install chromedriver

# Or use webdriver-manager (auto-downloads)
pip install webdriver-manager
```

### Demo File Not Found

**Error**: `FileNotFoundError: Could not find deal_progression_demo.html`

**Solution**:
```bash
# Specify the file path explicitly
python run_demo_automation.py --demo-file /full/path/to/deal_progression_demo.html
```

### Browser Opens But Nothing Happens

**Possible causes:**
1. Demo controls have different IDs
2. JavaScript not enabled
3. Page not fully loaded

**Solution**:
- Check the demo HTML file has the expected button IDs
- Increase wait time in script
- Run in interactive mode to manually debug

### Demo Doesn't Complete

If monitoring times out:
- Demo might have different completion signal
- Check browser console for JavaScript errors
- Try running without monitoring: `--no-monitor`

## Architecture

### Script Structure

```python
class DealProgressionDemoAutomation:
    # Core Methods
    _setup_browser()        # Initialize Chrome with Selenium
    load_demo()            # Load HTML file

    # Demo Controls
    start_demo()           # Click start button
    pause_demo()           # Click pause button
    reset_demo()           # Click reset button
    skip_to_next()         # Click skip button

    # Monitoring
    monitor_demo_progress()  # Real-time monitoring loop
    get_status()            # Get current status text
    count_messages()        # Count displayed messages
    is_typing_indicator_visible()  # Check for typing

    # Content Capture
    capture_demo_content()  # Extract and display messages

    # Execution Modes
    run_full_demo()        # Automated mode
    interactive_mode()     # Interactive mode
```

### Data Flow

```
1. Load HTML File (file://)
        ↓
2. Find Demo Controls (#startBtn, etc.)
        ↓
3. Click Start Button
        ↓
4. Enter Monitoring Loop
        ↓
5. Check Status Every 2 Seconds:
   - Status text (#statusText)
   - Message count (.message elements)
   - Typing indicator (#typingIndicator)
        ↓
6. Detect Completion (status == "Demo Complete")
        ↓
7. Optionally Capture Content
        ↓
8. Keep Browser Open
```

## Examples

### Example 1: Quick Demo Playback

```bash
# Just run the demo and watch
python run_demo_automation.py
```

### Example 2: Capture All Content

```bash
# Run demo and extract all messages at the end
python run_demo_automation.py --capture
```

Output includes:
```
📸 Capturing demo content...
======================================================================

--- Message 1 ---
From: You
Content: Show me deals that have been stalled for more than 30 days...

--- Message 2 ---
From: Deal Progression
Content: I've analyzed your pipeline and identified several stalled deals...
📊 Agent Card: Stalled Deal Analysis

--- Message 3 ---
From: You
Content: Tell me more about Contoso Enterprise...
```

### Example 3: Interactive Control

```bash
# Full manual control
python run_demo_automation.py --mode interactive
```

Then use menu to:
1. Start demo
2. Watch first few messages
3. Pause to inspect
4. Skip through quickly
5. Reset and replay

### Example 4: Headless Execution

Edit script to add headless mode:
```python
# In _setup_browser():
options.add_argument("--headless")  # Uncomment this line
```

Then run:
```bash
python run_demo_automation.py
```

Demo runs invisibly in background!

## Integration with Testing

### Use in Automated Tests

```python
from run_demo_automation import DealProgressionDemoAutomation

def test_demo_playback():
    automation = DealProgressionDemoAutomation()
    success = automation.run_full_demo(monitor=True, capture_content=False)
    assert success, "Demo should complete successfully"

    # Check message count
    message_count = automation.count_messages()
    assert message_count >= 10, "Demo should display at least 10 messages"

    automation.cleanup()
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run Demo Automation
  run: |
    pip install -r requirements_demo.txt
    python run_demo_automation.py --no-monitor
```

## Performance

### Typical Execution Times

- **Demo Load**: 2-3 seconds
- **Full Demo Playback**: 2-3 minutes (depends on demo script)
- **Monitoring Overhead**: ~0.5 seconds per check
- **Content Capture**: 1-2 seconds

### Resource Usage

- **Memory**: ~200-300 MB (Chrome browser)
- **CPU**: Low (< 5% when idle, spikes during page updates)
- **Disk**: Minimal (temporary browser cache)

## Advanced Usage

### Custom Monitoring Logic

Modify `monitor_demo_progress()` to add custom checks:

```python
def monitor_demo_progress(self, check_interval=2, timeout=300):
    # Your custom monitoring logic
    while time.time() - start_time < timeout:
        # Check for specific agent cards
        agent_cards = self.driver.find_elements(By.CLASS_NAME, 'agent-card')
        if len(agent_cards) >= 10:
            logger.info("✅ All 10 agent cards displayed!")

        # Check for specific content
        page_text = self.driver.find_element(By.TAG_NAME, 'body').text
        if 'Contoso Enterprise' in page_text:
            logger.info("🎯 Contoso deal analysis found!")
```

### Screenshot Capture

Add screenshot capability:

```python
def capture_screenshot(self, filename='demo_screenshot.png'):
    """Capture screenshot of current demo state"""
    self.driver.save_screenshot(filename)
    logger.info(f"📸 Screenshot saved: {filename}")
```

### Video Recording

For video recording, integrate with tools like:
- **ffmpeg** for screen recording
- **selenium-video** package
- Browser's built-in recording capabilities

## Support

For issues or questions:
1. Check browser console (F12) for JavaScript errors
2. Verify demo HTML file is properly formatted
3. Ensure ChromeDriver version matches Chrome version
4. Try running in interactive mode for debugging

## License

Same as Deal Progression Agent Stack (MIT)
