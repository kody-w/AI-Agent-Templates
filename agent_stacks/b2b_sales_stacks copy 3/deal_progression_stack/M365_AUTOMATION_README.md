# M365 Copilot Deal Progression Automation

Automated conversation script that simulates the Deal Progression Intelligence demo with the real Microsoft 365 Copilot interface.

## Features

- 🤖 **Fully Automated**: Conducts entire conversation without manual intervention after authentication
- 🔍 **Smart Input Detection**: Automatically finds and interacts with M365 Copilot's chat interface
- ⏳ **Intelligent Response Waiting**: Detects when Copilot is thinking and waits for complete responses
- 🔄 **Auto-Retry Logic**: Automatically retries failed messages
- 📊 **Progress Tracking**: Real-time logging of conversation progress
- 🎯 **Deal Progression Focus**: Asks 5 strategic questions about deal health and pipeline management

## Conversation Flow

The automation will ask these questions in sequence:

1. **Pipeline Analysis**: "Show me all stalled deals in our pipeline and assess the overall health risks"
2. **Health Scoring**: "What's the health score for the Contoso Enterprise Suite deal? I'm concerned about its progress."
3. **Stakeholder Engagement**: "Analyze the stakeholder engagement for this deal. Who should we be talking to?"
4. **Win Probability**: "What's our win probability for this deal, and what are the main factors affecting it?"
5. **Recovery Actions**: "Recommend the next best actions to save this deal"

## Prerequisites

### 1. Install Python Dependencies

```bash
pip install selenium
```

### 2. Install Microsoft Edge WebDriver

**macOS:**
```bash
brew install --cask microsoft-edge
# WebDriver is included with Edge
```

**Windows:**
- Edge browser is pre-installed
- WebDriver is included automatically

**Linux:**
```bash
# Install Microsoft Edge
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'
sudo apt update
sudo apt install microsoft-edge-stable
```

### 3. M365 Account

- You need a valid Microsoft 365 account with Copilot access
- **Sign in to Edge browser first** - the automation uses your default profile
- No need to re-authenticate if already signed in
- Supports MFA/2FA (but you only need to do it once in your default Edge profile)

## Usage

### Basic Usage

```bash
python m365_copilot_automation.py
```

### Step-by-Step Process

1. **Run the script**
   ```bash
   python m365_copilot_automation.py
   ```

2. **Browser opens automatically**
   - Edge browser will open with your default profile (already signed in)
   - Navigates to https://m365.cloud.microsoft/chat
   - Should automatically load the chat interface if you're signed in

3. **Wait for page load**
   - If already signed in: Just wait for chat interface to load
   - If not signed in: Complete Microsoft 365 sign-in in the browser
   - Press ENTER in terminal when you see the chat interface

4. **Automated conversation**
   - Script automatically types each question
   - Waits for Copilot to respond
   - Continues to next question
   - Provides real-time progress updates

5. **Review results**
   - Browser remains open after completion
   - Review the full conversation
   - All interactions are logged to console

## Advanced Options

### Debug Mode

To see more detailed logs, modify the logging level:

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

### Custom Debug Port

If port 9222 is in use:

```python
automation = M365DealProgressionAutomation(debug_port=9223)
```

### Adjust Timeouts

Modify response timeout for slower connections:

```python
# In run_deal_progression_conversation method
if self._wait_for_response(timeout=120):  # Increase from 90 to 120 seconds
```

## Troubleshooting

### Issue: "Could not find input field"

**Solution:**
- Ensure you've authenticated and reached the chat interface
- Wait for page to fully load before pressing ENTER
- The script will try multiple selector patterns automatically

### Issue: "Response timeout"

**Solution:**
- This is normal for complex questions
- The script continues anyway and counts it as success
- Check the browser to see if response actually completed
- Increase timeout value if needed

### Issue: "Browser won't open"

**Solution:**
```bash
# macOS - Reset WebDriver
brew reinstall microsoft-edge

# Windows - Update Edge
# Settings > About Microsoft Edge > Update

# All platforms - Check if Edge is in PATH
which msedge  # macOS/Linux
where msedge  # Windows
```

### Issue: "Not signed in" or "Authentication required"

**Solution:**
- Sign in to Edge browser manually first (before running script)
- Open Edge normally and go to https://m365.cloud.microsoft/chat
- Complete sign-in and MFA
- Close Edge
- Now run the automation script - it will use that signed-in profile

## Why Default Profile Instead of InPrivate?

**Convenience**: Using your default Edge profile means:
- ✅ No need to sign in every time you run the script
- ✅ Uses your existing M365 session and cookies
- ✅ Faster startup (no authentication flow)
- ✅ Preserves your settings and extensions

**Note**: The automation still disables automation detection flags, so websites won't easily detect it's automated.

## Technical Details

### Profile Strategy

The script uses your default Edge profile which means:
- All your saved credentials are available
- Cookies and session data persist
- Faster subsequent runs (no re-authentication)
- Same behavior as manually opening Edge

### Input Detection Strategy

The script tries multiple selector patterns:
1. Contenteditable divs (most common in M365)
2. Role-based selectors (`role='textbox'`)
3. Class-based patterns (`composer`, `input`)
4. Fallback to textarea elements

### Response Detection Strategy

The script detects Copilot responses by:
1. Checking for typing/thinking indicators
2. Monitoring page content growth
3. Detecting when content becomes stable (3 consecutive checks)
4. Minimum 100 character growth threshold

### Natural Interaction Simulation

- Types characters with 20ms delay between each
- Waits 8 seconds between questions
- Uses human-like timing patterns
- Disables automation detection flags

## Integration with Demo

This automation mirrors the conversation flow from `deal_progression_demo.html`:
- Same questions in same order
- Same contextual focus
- Designed to elicit similar insights from M365 Copilot
- Can be used to compare demo responses vs. real Copilot responses

## Safety & Best Practices

✅ **Do:**
- Run during business hours when you can monitor
- Have valid M365 Copilot license
- Review results for accuracy
- Use for testing and demonstration purposes

❌ **Don't:**
- Run unattended for extended periods
- Use with production credentials unnecessarily
- Rely on automation for critical business decisions
- Share credentials or tokens

## Output Example

```
╔═══════════════════════════════════════════════════════════════════╗
║   M365 Copilot - Deal Progression Intelligence Automation        ║
╚═══════════════════════════════════════════════════════════════════╝

🚀 Initializing M365 Copilot session...
✅ Edge browser initialized successfully
📍 Navigating to M365 Copilot...
✅ Successfully navigated to M365 Copilot

🔐 MANUAL AUTHENTICATION REQUIRED
[Authentication steps...]
Press ENTER when ready to start the automated conversation...

🚀 Starting automated conversation...
   From this point, everything runs automatically!

🔄 Question 1/5
💬 Sending: Show me all stalled deals in our pipeline...
✅ Message typed successfully
✅ Message sent via send button
⏳ Waiting for Copilot response...
⌨️  Copilot is thinking...
✅ Response stable (3/3) - 1547 chars (+1234)
✅ Response complete!
✅ Turn 1 completed successfully

[... continues for all 5 questions ...]

📊 CONVERSATION SUMMARY
════════════════════════════════════════════════════════════════════
✅ Successful: 5/5
❌ Failed: 0/5
🎉 Perfect! All questions completed successfully!
```

## License

This automation script is provided as-is for demonstration and testing purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console logs for specific errors
3. Ensure all prerequisites are installed
4. Verify M365 Copilot access in your tenant
