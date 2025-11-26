# M365 Copilot Automation - Complete Summary

## What Was Created

I've built a complete automation system that simulates your Deal Progression demo conversation with the **real Microsoft 365 Copilot** interface at https://m365.cloud.microsoft/chat.

### Files Created

1. **`m365_copilot_automation.py`** (Main automation script)
   - Fully automated conversation with M365 Copilot
   - Asks 5 strategic deal progression questions
   - Smart input detection and response waiting
   - Auto-retry logic for failed messages

2. **`test_m365_connection.py`** (Setup validation)
   - Tests Selenium installation
   - Validates Edge WebDriver
   - Confirms browser can launch and navigate

3. **`M365_AUTOMATION_README.md`** (Comprehensive documentation)
   - Installation instructions
   - Usage guide
   - Troubleshooting tips
   - Technical details

4. **`AUTOMATION_SUMMARY.md`** (This file)
   - Quick overview
   - Getting started guide

## Quick Start

### 1. Install Dependencies

```bash
# Install Selenium
pip install selenium

# Edge browser should already be installed on your system
# If not, download from: https://www.microsoft.com/edge
```

### 2. Test Your Setup

```bash
python test_m365_connection.py
```

Expected output:
```
✅ PASS - Selenium Installation
✅ PASS - Edge WebDriver
✅ PASS - Browser Launch

Results: 3/3 tests passed
🎉 All tests passed! You're ready to run the automation.
```

### 3. Run the Automation

```bash
python m365_copilot_automation.py
```

**What happens:**
1. Edge browser opens in InPrivate mode
2. Navigates to https://m365.cloud.microsoft/chat
3. **YOU MANUALLY AUTHENTICATE** (sign in, complete MFA)
4. Press ENTER when you see the chat interface
5. **Automation takes over** - sits back and watch!
6. Asks 5 questions automatically
7. Waits for and detects responses
8. Provides real-time progress updates
9. Browser stays open for you to review

## The Conversation Flow

The automation will conduct this conversation with M365 Copilot:

### Question 1: Pipeline Overview
> "Show me all stalled deals in our pipeline and assess the overall health risks"

**Purpose:** Get comprehensive pipeline analysis and identify at-risk deals

### Question 2: Deal Health Assessment
> "What's the health score for the Contoso Enterprise Suite deal? I'm concerned about its progress."

**Purpose:** Deep dive into specific deal health metrics

### Question 3: Stakeholder Analysis
> "Analyze the stakeholder engagement for this deal. Who should we be talking to?"

**Purpose:** Understand relationship dynamics and engagement gaps

### Question 4: Win Probability
> "What's our win probability for this deal, and what are the main factors affecting it?"

**Purpose:** Get AI-driven probability assessment with contributing factors

### Question 5: Action Recommendations
> "Recommend the next best actions to save this deal"

**Purpose:** Receive prioritized recovery plan with specific action items

## Key Features

### 🔍 Smart Input Detection
- Automatically finds M365 Copilot's chat input field
- Tries 15+ different selector patterns
- Tests each field to confirm it accepts input
- Caches working selectors for speed

### ⏳ Intelligent Response Waiting
- Detects typing/thinking indicators
- Monitors page content growth
- Waits for content to stabilize (3 checks)
- Minimum 100 character growth threshold
- 60-90 second timeout per response

### 🔄 Auto-Retry Logic
- Automatically retries failed messages
- 2 retry attempts per question
- Continues conversation even if one question fails
- Detailed logging of all attempts

### 🎯 Natural Interaction
- Types characters with 20ms delay (appears human)
- 8 second pause between questions
- Uses Enter or Send button (whichever works)
- Disables automation detection flags

## Output Example

```
╔═══════════════════════════════════════════════════════════════════╗
║   M365 Copilot - Deal Progression Intelligence Automation        ║
╚═══════════════════════════════════════════════════════════════════╝

🚀 Initializing M365 Copilot session...
✅ Edge browser initialized with default profile
   Using existing authentication from your Edge profile
📍 Navigating to M365 Copilot...
✅ Successfully navigated to M365 Copilot
   📄 Title: Microsoft 365 Copilot
   🔗 URL: https://m365.cloud.microsoft/chat

⏳ WAITING FOR COPILOT INTERFACE TO LOAD
════════════════════════════════════════════════════════════════════
Using your default Edge profile (already signed in)

If the page loads automatically:
  ✅ Great! Just press ENTER to start

If you need to sign in:
  1. Complete sign-in in the browser window
  2. Wait for chat interface to load
  3. Then press ENTER
════════════════════════════════════════════════════════════════════
Press ENTER when you see the chat interface...

[Press ENTER]

✅ Authentication confirmed - starting automation

🎯 DEAL PROGRESSION INTELLIGENCE CONVERSATION
════════════════════════════════════════════════════════════════════
Will ask 5 questions about:
  • Stalled deals and pipeline health
  • Deal health scoring
  • Stakeholder engagement analysis
  • Win probability assessment
  • Recovery action recommendations
════════════════════════════════════════════════════════════════════

🔄 Question 1/5
════════════════════════════════════════════════════════════════════
💬 Sending: Show me all stalled deals in our pipeline and assess the overall health risks
📋 Context: Analyzing pipeline for stalled deals and risk assessment
════════════════════════════════════════════════════════════════════
🔍 Detecting chat input field...
✅ Found input field: <div> with selector: div[contenteditable='true'][role='textbox']
✅ Message typed successfully
✅ Message sent via send button
⏳ Waiting for Copilot response...
⌨️  Copilot is thinking...
⌨️  Copilot is thinking...
📝 Response in progress... 458 chars (+458)
📝 Response in progress... 892 chars (+892)
✅ Response stable (1/3) - 1247 chars (+1247)
✅ Response stable (2/3) - 1247 chars (+1247)
✅ Response stable (3/3) - 1247 chars (+1247)
✅ Response complete!
✅ Turn 1 completed successfully

⏳ Waiting 8s before next question...
   Next question in 1s...

[... continues for all 5 questions ...]

📊 CONVERSATION SUMMARY
════════════════════════════════════════════════════════════════════
✅ Successful: 5/5
❌ Failed: 0/5
🎉 Perfect! All questions completed successfully!
════════════════════════════════════════════════════════════════════

🎉 Automation completed successfully!
💡 Browser will remain open for your review
```

## Comparison: Demo vs Real Copilot

### Demo HTML (`deal_progression_demo.html`)
- ✅ Pre-scripted responses
- ✅ Instant response time
- ✅ Perfect formatting
- ✅ Controlled environment
- ❌ Not real AI responses
- ❌ Not connected to real data

### M365 Copilot Automation (`m365_copilot_automation.py`)
- ✅ Real AI responses from M365 Copilot
- ✅ Potentially connected to real D365/CRM data
- ✅ Contextual understanding
- ✅ Natural language processing
- ⚠️ Requires M365 Copilot license
- ⚠️ Responses vary based on data access
- ⚠️ Slower response time (real AI processing)

## Use Cases

### 1. Demo Preparation
Run the automation before a customer demo to:
- Test M365 Copilot's responses to your questions
- Identify which questions work best
- Understand response quality and timing
- Prepare for potential customer questions

### 2. Training
Use for training sales teams on:
- How to interact with M365 Copilot
- What questions to ask about deals
- How to interpret Copilot's responses
- Best practices for deal analysis

### 3. Comparison Testing
Compare responses between:
- Your demo HTML (controlled)
- Real M365 Copilot (live AI)
- Different data sets
- Different phrasings of questions

### 4. Quality Assurance
Validate that:
- M365 Copilot understands your questions
- Responses are relevant and actionable
- Integration with D365/CRM works
- Performance meets expectations

## Troubleshooting

### "Could not find input field"
**Solution:** Wait longer after authentication. Ensure chat interface is fully loaded.

### "Response timeout"
**Normal behavior.** Script continues anyway. Check browser to verify response completed.

### Edge WebDriver errors
```bash
# macOS
brew reinstall microsoft-edge

# Windows - Update Edge
# Settings > About Microsoft Edge > Update
```

### Not signed in / Authentication issues
**Solution:** Sign in to Edge manually first:
- Open Edge browser normally
- Go to https://m365.cloud.microsoft/chat
- Complete sign-in and MFA
- Close Edge
- Run automation script - it will use that profile

## Technical Architecture

### Browser Control
- Uses Selenium WebDriver
- Edge browser (best compatibility with M365)
- **Default profile mode** (uses your signed-in session)
- Remote debugging port (9222)
- No need to re-authenticate each time!

### Input Detection Strategy
1. Tries contenteditable divs (M365's typical pattern)
2. Tries role='textbox' elements
3. Falls back to textarea/input elements
4. Tests each candidate by sending a character
5. Caches working selector for speed

### Response Detection Strategy
1. Captures initial page content
2. Monitors for typing indicators
3. Tracks content growth (minimum 100 chars)
4. Waits for content stability (3 consecutive checks at same length)
5. Times out after 60-90 seconds

### Safety Features
- Uses your default profile (convenient and secure)
- Browser stays open for review
- All actions logged
- Auto-retry prevents transient failures
- Timeout prevents infinite waiting
- Automation detection disabled

## What's Next?

### Extend the Conversation
Add more questions in `m365_copilot_automation.py`:

```python
self.conversation = [
    {
        "message": "Your new question here",
        "context": "What this question is about"
    },
    # ... existing questions ...
]
```

### Customize Timing
Adjust waits and delays:

```python
# Character typing delay
time.sleep(0.02)  # Change from 20ms

# Between questions
wait_time = 8  # Change from 8 seconds

# Response timeout
self._wait_for_response(timeout=90)  # Change from 90s
```

### Add Screenshots
Capture screenshots at each step:

```python
def _send_message(self, message: str, context: str = "") -> bool:
    # ... existing code ...
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    self.driver.save_screenshot(f"screenshot_{timestamp}.png")
```

### Export Conversation
Save the conversation to a file:

```python
def _save_conversation(self):
    content = self._get_page_content()
    with open(f"conversation_{timestamp}.txt", "w") as f:
        f.write(content)
```

## Requirements Summary

- **Python**: 3.7+
- **Selenium**: `pip install selenium`
- **Edge Browser**: Pre-installed on Windows, brew install on macOS
- **M365 Account**: With Copilot access
- **Internet**: Stable connection for real-time AI responses

## Support

1. **Test Setup First**: `python test_m365_connection.py`
2. **Check README**: `M365_AUTOMATION_README.md` has detailed troubleshooting
3. **Review Logs**: Console output shows detailed progress and errors
4. **Verify Access**: Ensure M365 Copilot is enabled in your tenant

---

**Created**: December 2024
**Purpose**: Automate Deal Progression Intelligence conversation with M365 Copilot
**Status**: Ready to use ✅
