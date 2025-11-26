# Navigation Recorder & Playback Guide

Record your manual navigation to the M365 Copilot chat interface, then automatically replay it every time!

## Why Use the Recorder?

If getting to the M365 Copilot chat requires:
- ✅ Clicking through multiple pages
- ✅ Dismissing popups or dialogs
- ✅ Navigating through menus
- ✅ Selecting specific options
- ✅ Any multi-step process

**Record it once, replay it forever!**

## Quick Start

### Step 1: Record Your Navigation

```bash
python record_navigation.py
```

**What happens:**
1. Browser opens to https://m365.cloud.microsoft/chat
2. You manually navigate to the chat interface
3. You describe each action you take using simple commands
4. Recording is saved to `navigation_recording.json`

### Step 2: Test the Recording

```bash
python playback_navigation.py
```

**What happens:**
- Browser opens and automatically replays your recorded steps
- Should end up at the chat interface
- Verify it worked correctly

### Step 3: Use in Automation

```bash
python m365_copilot_automation.py
```

**What happens:**
- Automatically uses your recording to navigate
- No manual navigation needed
- Goes straight to conversation automation

## Recording Commands

While recording, use these commands to log your actions:

### Navigation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `w [seconds]` | Wait for N seconds | `w 3` |
| `c [selector]` | Click element (CSS selector) | `c button.next` |
| `t [text]` | Type text into active field | `t mypassword` |
| `n [url]` | Navigate to URL | `n https://example.com` |
| `m [note]` | Mark a checkpoint | `m "Reached dashboard"` |
| `s` | Show all recorded actions | `s` |
| `d` | Done - save and exit | `d` |
| `h` | Show help | `h` |

## Recording Workflow

### Example Recording Session

```bash
$ python record_navigation.py

🎬 M365 COPILOT NAVIGATION RECORDER
══════════════════════════════════════════════════════════════
Recording will track your actions to reach the chat interface
══════════════════════════════════════════════════════════════

✅ Browser is ready. Now recording your actions...

[Step 1] Current URL: https://m365.cloud.microsoft/chat

# Browser is loading, wait for it
Command: w 5

⏳ Waiting 5 seconds...
📝 Recorded: wait - {'seconds': 5.0}

[Step 2] Current URL: https://m365.cloud.microsoft/chat

# Click "Get Started" button (inspect element to get selector)
Command: c button.get-started

🖱️  Recording click on: button.get-started
📝 Recorded: click - {'selector': 'button.get-started', 'method': 'css'}

[Step 3] Current URL: https://m365.cloud.microsoft/chat/onboarding

# Wait for next page to load
Command: w 3

⏳ Waiting 3 seconds...

[Step 4] Current URL: https://m365.cloud.microsoft/chat/onboarding

# Click "Skip Tutorial"
Command: c a.skip-tutorial

🖱️  Recording click on: a.skip-tutorial

[Step 5] Current URL: https://m365.cloud.microsoft/chat

# Mark that we've reached the final destination
Command: m Reached chat interface

📌 Marking checkpoint...
📝 Recorded: checkpoint - {'url': 'https://m365.cloud.microsoft/chat', ...}

# We're done!
Command: d

✅ Finishing recording...
📝 Recorded: final_checkpoint
✅ Recording saved to: navigation_recording.json
📊 Total actions: 5

🎉 Recording Complete!
```

## Finding CSS Selectors

### Method 1: Browser DevTools (Easiest)

1. **Right-click** the element you want to click
2. Select **"Inspect"** or **"Inspect Element"**
3. DevTools opens with the element highlighted
4. **Right-click** the highlighted HTML
5. Select **"Copy > Copy selector"**
6. Paste into the recorder command

### Method 2: Manual Inspection

Common selector patterns:

| Element Type | Selector Example |
|--------------|------------------|
| Button with class | `button.submit-btn` |
| Link with ID | `a#next-link` |
| Button with text | `button:contains("Next")` |
| Input field | `input[name="username"]` |
| Any clickable | `[role="button"]` |
| Specific button | `button[aria-label="Continue"]` |

### Tips for Good Selectors

✅ **Good selectors:**
- `button.primary-action`
- `a#continue-link`
- `input[type="email"]`
- `[data-testid="submit-btn"]`

❌ **Avoid:**
- Long nested selectors (brittle)
- Dynamically generated IDs
- Overly specific paths

## Recording Best Practices

### 1. Record in Logical Steps

Break navigation into clear checkpoints:
```bash
# Step 1: Initial load
w 5
m "Page loaded"

# Step 2: Dismiss popup
c button.close-popup
w 2
m "Popup closed"

# Step 3: Navigate to chat
c a.chat-link
w 3
m "Chat interface ready"

# Done
d
```

### 2. Add Generous Wait Times

Give the browser time to:
- Load pages completely
- Render dynamic content
- Execute JavaScript
- Update the DOM

```bash
# After navigation
w 5

# After clicking something that triggers loading
w 3

# Before typing (ensure field is ready)
w 1
```

### 3. Use Checkpoints

Mark important milestones:
```bash
m "Login complete"
m "Reached dashboard"
m "Chat interface visible"
```

This helps with debugging playback issues.

### 4. Test Each Step

Before moving to the next step:
- Verify the action completed
- Wait for any loading to finish
- Check URL changed (if expected)

## Playback Testing

### Basic Playback

```bash
python playback_navigation.py
```

Plays back and keeps browser open for verification.

### Quick Playback

```bash
python playback_navigation.py --no-wait
```

Plays back and closes browser automatically.

### Custom Recording File

```bash
python playback_navigation.py --recording my_custom_recording.json
```

## Integration with Main Automation

The main automation script automatically uses your recording:

```bash
python m365_copilot_automation.py
```

**How it works:**
1. Checks if `navigation_recording.json` exists
2. If yes: Plays back recorded navigation
3. If no: Uses direct navigation (simple URL visit)
4. Then proceeds with deal progression conversation

### Disable Recording Playback

If you want to skip the recording:

```python
# In m365_copilot_automation.py
automation = M365DealProgressionAutomation(use_recording=False)
```

## Recording File Format

The recording is saved as JSON:

```json
{
  "version": "1.0",
  "recorded_at": "2024-12-20 14:30:00",
  "start_url": "https://m365.cloud.microsoft/chat",
  "final_url": "https://m365.cloud.microsoft/chat",
  "total_actions": 5,
  "actions": [
    {
      "type": "navigate",
      "timestamp": 1703089800.0,
      "url": "https://m365.cloud.microsoft/chat",
      "data": {
        "url": "https://m365.cloud.microsoft/chat"
      }
    },
    {
      "type": "wait",
      "timestamp": 1703089805.0,
      "url": "https://m365.cloud.microsoft/chat",
      "data": {
        "seconds": 5
      }
    },
    {
      "type": "click",
      "timestamp": 1703089810.0,
      "url": "https://m365.cloud.microsoft/chat/onboarding",
      "data": {
        "selector": "button.get-started",
        "method": "css"
      }
    }
  ]
}
```

### Manual Editing

You can manually edit the recording:

```json
{
  "type": "wait",
  "data": {
    "seconds": 10  // Increase wait time
  }
}
```

```json
{
  "type": "click",
  "data": {
    "selector": "button.new-selector"  // Update selector
  }
}
```

## Troubleshooting

### Recording Issues

**Issue: "Can't find element to click"**
- Use browser DevTools to inspect and copy correct selector
- Try a simpler selector (class or ID)
- Check if element is in an iframe

**Issue: "Actions not working during playback"**
- Add more wait time between actions
- Use checkpoints to identify where it fails
- Check if selectors are correct

### Playback Issues

**Issue: "Element not found during playback"**
```bash
# Solution 1: Update selector in recording file
# Solution 2: Add longer wait before click
{
  "type": "wait",
  "data": {"seconds": 5}
}
```

**Issue: "Too fast - steps skip ahead"**
```bash
# Add wait steps between actions
w 3
c button.next
w 3
c button.continue
```

**Issue: "Playback stops at certain step"**
- Check the URL in the checkpoint
- Verify the page actually loaded
- Look for errors in console
- Try manual navigation to see what's different

## Advanced Usage

### Multiple Recordings

Create different recordings for different scenarios:

```bash
# Record normal flow
python record_navigation.py
# Saves to: navigation_recording.json

# For testing, rename it
mv navigation_recording.json navigation_normal.json

# Record alternate flow
python record_navigation.py
mv navigation_recording.json navigation_alternate.json

# Use specific recording
python playback_navigation.py --recording navigation_alternate.json
```

### Conditional Navigation

Edit the main automation to choose recording based on conditions:

```python
if some_condition:
    automation = M365DealProgressionAutomation(use_recording=True)
    automation.recording_file = Path("navigation_alternate.json")
else:
    automation = M365DealProgressionAutomation(use_recording=False)
```

## FAQ

**Q: Do I need to record every time?**
A: No! Record once, use forever. Only re-record if the M365 interface changes.

**Q: Can I edit the recording file?**
A: Yes! It's JSON - edit wait times, selectors, add/remove steps.

**Q: What if M365 changes their interface?**
A: Just record again. Takes 2-3 minutes.

**Q: Can I record keyboard shortcuts?**
A: Not yet, but you can manually add them to the JSON.

**Q: Does this work with MFA/authentication?**
A: The recording starts after you're signed in. It records navigation through the interface, not the login process.

**Q: How long does playback take?**
A: Depends on your recording - usually 10-30 seconds.

## Summary

1. **Record once**: `python record_navigation.py`
2. **Test it**: `python playback_navigation.py`
3. **Use it**: `python m365_copilot_automation.py` (automatic!)

That's it! The automation will handle navigation automatically from now on.

---

**Created**: December 2024
**Version**: 1.0
**Purpose**: Record and replay navigation to M365 Copilot chat interface
