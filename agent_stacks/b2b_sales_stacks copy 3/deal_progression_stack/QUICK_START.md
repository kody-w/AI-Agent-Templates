# M365 Copilot Automation - Quick Start

Get started in 3 simple steps!

## 🎯 What This Does

Automatically asks M365 Copilot 5 intelligent questions about deal progression:
1. Stalled deals analysis
2. Deal health scoring
3. Stakeholder engagement
4. Win probability
5. Recovery action plan

## 🚀 Three Ways to Run

### Option 1: Simple (No Recording)

**Best if:** M365 Copilot loads directly at the URL with no extra clicks

```bash
python m365_copilot_automation.py
```

1. Browser opens (already signed in with your Edge profile)
2. Press ENTER when chat loads
3. Watch automation run!

---

### Option 2: With Navigation Recording (Recommended)

**Best if:** You need to click through menus/popups to reach the chat

#### Step 1: Record Your Navigation (Once)
```bash
python record_navigation.py
```

**What to do:**
- Browser opens to M365 Copilot
- Manually navigate to the chat interface
- Use simple commands to describe your actions:
  - `w 3` = wait 3 seconds
  - `c button.next` = click button with class "next"
  - `m "checkpoint"` = mark a checkpoint
  - `d` = done, save recording
- See `RECORDER_GUIDE.md` for detailed instructions

#### Step 2: Test the Recording
```bash
python playback_navigation.py
```

Replays your recorded navigation to verify it works.

#### Step 3: Run Full Automation
```bash
python m365_copilot_automation.py
```

Automatically uses your recording, then runs the conversation!

---

### Option 3: Test Playback Only

```bash
python playback_navigation.py
```

Just test the navigation recording without running the full conversation.

## 📋 Prerequisites

### Install Python Package
```bash
pip install selenium
```

### Sign In to Edge (One Time)
1. Open Edge browser manually
2. Go to https://m365.cloud.microsoft/chat
3. Sign in with M365 account
4. Complete MFA
5. Close Edge

Now you're ready! The automation uses this profile.

## 🎬 Complete Workflow

### First Time Setup

```bash
# 1. Test your setup
python test_m365_connection.py

# 2. Record navigation (if needed)
python record_navigation.py
# Follow prompts, use commands to log actions

# 3. Test the recording
python playback_navigation.py

# 4. Run full automation
python m365_copilot_automation.py
```

### Every Time After

```bash
# Just run it!
python m365_copilot_automation.py
```

The automation:
- ✅ Opens Edge with your profile (already signed in)
- ✅ Uses recorded navigation (if exists)
- ✅ Asks 5 questions automatically
- ✅ Waits for responses intelligently
- ✅ Provides real-time progress updates

## 📊 What You'll See

```
╔═══════════════════════════════════════════════════════════════════╗
║   M365 Copilot - Deal Progression Intelligence Automation        ║
╚═══════════════════════════════════════════════════════════════════╝

🚀 Initializing M365 Copilot session...
✅ Edge browser initialized with default profile
   Using existing authentication from your Edge profile

📼 Found navigation recording - using recorded steps
🎬 Playing back 5 recorded actions...
  [1/5] navigate
  [2/5] wait
  [3/5] click
  [4/5] wait
  [5/5] checkpoint
✅ Navigation via recording successful
   📄 Title: Microsoft 365 Copilot
   🔗 URL: https://m365.cloud.microsoft/chat

⏳ WAITING FOR COPILOT INTERFACE TO LOAD
════════════════════════════════════════════════════════════════════
Using your default Edge profile (already signed in)
Press ENTER when you see the chat interface...

[You press ENTER]

🎯 DEAL PROGRESSION INTELLIGENCE CONVERSATION
════════════════════════════════════════════════════════════════════
Will ask 5 questions about:
  • Stalled deals and pipeline health
  • Deal health scoring
  • Stakeholder engagement analysis
  • Win probability assessment
  • Recovery action recommendations

🔄 Question 1/5
💬 Sending: Show me all stalled deals in our pipeline...
✅ Message sent
⏳ Waiting for Copilot response...
⌨️  Copilot is thinking...
✅ Response complete!
✅ Turn 1 completed successfully

[Continues through all 5 questions...]

📊 CONVERSATION SUMMARY
════════════════════════════════════════════════════════════════════
✅ Successful: 5/5
❌ Failed: 0/5
🎉 Perfect! All questions completed successfully!
```

## 🛠️ Troubleshooting

### "Could not find input field"
**Fix:** Wait longer after pressing ENTER. Ensure chat interface is fully loaded.

### "Recording not found"
**Fix:** Run `python record_navigation.py` first to create a recording.

### "Browser won't open"
**Fix:** Ensure Edge is installed and updated.

### "Not signed in"
**Fix:**
1. Open Edge manually
2. Go to https://m365.cloud.microsoft/chat
3. Sign in and complete MFA
4. Close Edge and try again

## 📁 Files You Have

| File | Purpose |
|------|---------|
| `m365_copilot_automation.py` | Main automation script |
| `record_navigation.py` | Record your navigation path |
| `playback_navigation.py` | Test recorded navigation |
| `test_m365_connection.py` | Validate setup |
| `navigation_recording.json` | Your saved navigation (created by recorder) |

## 📚 Documentation

- **`RECORDER_GUIDE.md`** - Complete guide to recording navigation
- **`M365_AUTOMATION_README.md`** - Full technical documentation
- **`AUTOMATION_SUMMARY.md`** - Detailed overview
- **`WHATS_NEW.md`** - Recent changes (default profile mode)

## 💡 Tips

1. **Record Once**: Navigation recording only needs to be done once (unless M365 interface changes)

2. **Test First**: Always run `test_m365_connection.py` before first use

3. **Watch Output**: The console shows detailed progress - watch for any errors

4. **Keep Browser Open**: Browser stays open after completion so you can review the conversation

5. **Edit Recording**: The JSON file can be manually edited if needed

## 🎯 Common Scenarios

### Scenario 1: Direct Access
M365 Copilot chat loads directly at the URL
```bash
# No recording needed
python m365_copilot_automation.py
```

### Scenario 2: One-Time Popup
Need to click "Get Started" or dismiss a welcome popup
```bash
# Record it once
python record_navigation.py
# Command: w 3
# Command: c button.get-started
# Command: d

# Use forever
python m365_copilot_automation.py
```

### Scenario 3: Multi-Step Navigation
Need to navigate through menus
```bash
# Record full path
python record_navigation.py
# Use all the commands: w, c, m, etc.
# Command: d when done

# Verify
python playback_navigation.py

# Run
python m365_copilot_automation.py
```

## 🔄 Update Recording

If M365 interface changes:

```bash
# Delete old recording
rm navigation_recording.json

# Record new navigation
python record_navigation.py

# Test it
python playback_navigation.py

# Use it
python m365_copilot_automation.py
```

## ✅ Success Checklist

Before first run:
- [ ] Selenium installed (`pip install selenium`)
- [ ] Edge browser installed
- [ ] Signed in to M365 in Edge browser
- [ ] Tested with `test_m365_connection.py`
- [ ] (Optional) Created navigation recording
- [ ] (Optional) Tested playback

You're ready to go! 🚀

---

**Need Help?**
- Recording help: `RECORDER_GUIDE.md`
- Technical details: `M365_AUTOMATION_README.md`
- Full overview: `AUTOMATION_SUMMARY.md`

**Quick Support:**
```bash
# Test your setup
python test_m365_connection.py

# View recording
cat navigation_recording.json

# Test recording playback
python playback_navigation.py
```
