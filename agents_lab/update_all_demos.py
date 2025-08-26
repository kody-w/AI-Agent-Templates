#!/usr/bin/env python3
"""
Update all 60 agent stack demos with chat-based conversational pattern
"""

import os
import json

# Base HTML template for all demos
def get_demo_template(title, emoji, description, demo_script):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Conversational Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #742774;
            --primary-dark: #4f1c4f;
            --secondary: #00a651;
            --secondary-dark: #008441;
            --accent: #40e0d0;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #1f2937;
            --gray: #6b7280;
            --light: #f3f4f6;
            --lighter: #f9fafb;
            --border: #e5e7eb;
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #742774 0%, #00a651 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--text-primary);
        }}

        .main-container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 24px;
            box-shadow: var(--shadow-xl);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 2.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .header p {{
            font-size: 1.15rem;
            opacity: 0.95;
            max-width: 700px;
            margin: 0 auto;
        }}

        .mode-selector {{
            background: var(--lighter);
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }}

        .config-panel {{
            background: var(--lighter);
            padding: 1.5rem;
            border-bottom: 2px solid var(--border);
            display: none;
        }}

        .config-panel.active {{
            display: block;
        }}

        .config-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            gap: 1rem;
        }}

        .input-row {{
            display: grid;
            grid-template-columns: 1fr 1fr auto;
            gap: 1rem;
            align-items: end;
        }}

        .input-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .input-group label {{
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
        }}

        .input-group input {{
            padding: 0.75rem;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }}

        .input-group input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(116, 39, 116, 0.1);
        }}

        .connection-status {{
            padding: 0.75rem 1rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            background: var(--light);
            color: var(--text-secondary);
            justify-content: center;
            margin-top: 1rem;
        }}

        .connection-status.connected {{
            background: #d1fae5;
            color: #065f46;
        }}

        .connection-status.error {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .mode-toggle {{
            background: white;
            border-radius: 12px;
            padding: 4px;
            display: flex;
            gap: 4px;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
        }}

        .mode-btn {{
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            background: transparent;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .mode-btn.active {{
            background: var(--primary);
            color: white;
            box-shadow: var(--shadow-md);
        }}

        .mode-btn:hover:not(.active) {{
            background: var(--light);
        }}

        .content-area {{
            display: grid;
            grid-template-columns: 350px 1fr;
            height: 600px;
        }}

        .sidebar {{
            background: var(--lighter);
            border-right: 1px solid var(--border);
            padding: 1.5rem;
            overflow-y: auto;
        }}

        .control-section {{
            margin-bottom: 2rem;
        }}

        .control-section h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .demo-controls {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}

        .control-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }}

        .btn {{
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            white-space: nowrap;
        }}

        .btn-primary {{
            background: var(--primary);
            color: white;
        }}

        .btn-primary:hover {{
            background: var(--primary-dark);
        }}

        .btn-success {{
            background: var(--success);
            color: white;
        }}

        .btn-success:hover {{
            background: #059669;
        }}

        .btn-secondary {{
            background: var(--gray);
            color: white;
        }}

        .btn-secondary:hover {{
            background: #4b5563;
        }}

        .btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .speed-control {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }}

        .speed-label {{
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
        }}

        .speed-slider {{
            flex: 1;
            -webkit-appearance: none;
            appearance: none;
            height: 6px;
            border-radius: 3px;
            background: var(--border);
            outline: none;
        }}

        .speed-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--primary);
            cursor: pointer;
        }}

        .progress-section {{
            margin-bottom: 2rem;
        }}

        .progress-bar {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 1rem;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 4px;
            width: 0%;
            transition: width 0.5s ease;
        }}

        .step-indicators {{
            display: flex;
            justify-content: space-between;
            gap: 0.5rem;
        }}

        .step-indicator {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            flex: 1;
        }}

        .step-circle {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: white;
            border: 3px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: var(--text-secondary);
            transition: all 0.3s ease;
        }}

        .step-indicator.active .step-circle {{
            background: var(--primary);
            border-color: var(--primary);
            color: white;
            transform: scale(1.1);
        }}

        .step-indicator.completed .step-circle {{
            background: var(--success);
            border-color: var(--success);
            color: white;
        }}

        .step-label {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-align: center;
        }}

        .chat-container {{
            background: white;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .chat-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chat-title {{
            font-size: 1.1rem;
            font-weight: 600;
        }}

        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .status-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10b981;
            animation: none;
        }}

        .status-dot.processing {{
            background: #f59e0b;
            animation: statusPulse 1s infinite;
        }}

        @keyframes statusPulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            background: var(--lighter);
        }}

        .message {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            animation: messageSlide 0.3s ease;
        }}

        @keyframes messageSlide {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .message-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            flex-shrink: 0;
        }}

        .message.user .message-avatar {{
            background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%);
        }}

        .message.assistant .message-avatar {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        }}

        .message-content {{
            flex: 1;
        }}

        .message-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        .message-sender {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .message-time {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        .message-text {{
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            line-height: 1.6;
            border: 1px solid var(--border);
        }}

        .message.user .message-text {{
            background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%);
            color: white;
            border: none;
        }}

        .result-card {{
            background: white;
            border: 2px solid var(--primary);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
        }}

        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border);
        }}

        .result-title {{
            font-weight: 600;
            color: var(--primary);
            font-size: 1.1rem;
        }}

        .result-status {{
            padding: 0.25rem 0.75rem;
            background: var(--success);
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .result-fields {{
            display: grid;
            gap: 0.75rem;
        }}

        .result-field {{
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 0.5rem;
            padding: 0.5rem;
            background: var(--lighter);
            border-radius: 6px;
        }}

        .result-label {{
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        .result-value {{
            color: var(--text-primary);
        }}

        .typing-indicator {{
            display: none;
            padding: 0.75rem 1rem;
            background: white;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
            width: fit-content;
        }}

        .typing-indicator.active {{
            display: inline-block;
        }}

        .typing-dots {{
            display: flex;
            gap: 4px;
        }}

        .typing-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--gray);
            animation: typingPulse 1.4s infinite ease-in-out;
        }}

        .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
        .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}

        @keyframes typingPulse {{
            0%, 80%, 100% {{
                opacity: 0.5;
                transform: scale(1);
            }}
            40% {{
                opacity: 1;
                transform: scale(1.2);
            }}
        }}

        @media (max-width: 1024px) {{
            .content-area {{
                grid-template-columns: 1fr;
                height: auto;
            }}

            .sidebar {{
                border-right: none;
                border-bottom: 1px solid var(--border);
            }}
        }}

        @media (max-width: 640px) {{
            .header h1 {{
                font-size: 1.75rem;
            }}

            .mode-selector {{
                padding: 1rem;
            }}

            .chat-messages {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <div class="header-content">
                <h1>{emoji} {title}</h1>
                <p>{description}</p>
            </div>
        </div>

        <div class="mode-selector">
            <div class="mode-toggle">
                <button class="mode-btn active" onclick="switchMode('demo')" id="demoModeBtn">
                    <span>🎬</span>
                    <span>Demo Mode</span>
                </button>
                <button class="mode-btn" onclick="switchMode('live')" id="liveModeBtn">
                    <span>🔴</span>
                    <span>Live Mode</span>
                </button>
            </div>
        </div>

        <div class="config-panel" id="liveConfig">
            <div class="config-content">
                <div class="input-row">
                    <div class="input-group">
                        <label>Azure Function Key</label>
                        <input type="password" id="apiKey" placeholder="Enter your function key">
                    </div>
                    <div class="input-group">
                        <label>Function App URL</label>
                        <input type="text" id="apiEndpoint" placeholder="https://your-app.azurewebsites.net/api/{title.lower().replace(' ', '-')}">
                    </div>
                    <button class="btn btn-primary" onclick="testConnection()">
                        Test Connection
                    </button>
                </div>
                <div class="connection-status" id="connectionStatus">
                    <span class="status-dot idle"></span>
                    <span>Not Connected</span>
                </div>
            </div>
        </div>

        <div class="content-area">
            <div class="sidebar">
                <div class="control-section">
                    <h3>🎮 Demo Controls</h3>
                    <div class="demo-controls">
                        <div class="control-row">
                            <button class="btn btn-success" onclick="startDemo()" id="startBtn">
                                ▶️ Start Demo
                            </button>
                            <button class="btn btn-secondary" onclick="pauseDemo()" id="pauseBtn" disabled>
                                ⏸️ Pause
                            </button>
                        </div>
                        <div class="control-row">
                            <button class="btn btn-secondary" onclick="resetDemo()" id="resetBtn">
                                🔄 Reset
                            </button>
                            <button class="btn btn-secondary" onclick="skipToNext()" id="skipBtn" disabled>
                                ⏭️ Skip
                            </button>
                        </div>
                    </div>
                    <div class="speed-control">
                        <span class="speed-label">Speed:</span>
                        <input type="range" class="speed-slider" id="speedSlider" min="0.5" max="3" step="0.5" value="1">
                        <span class="speed-label" id="speedLabel">1x</span>
                    </div>
                </div>

                <div class="progress-section">
                    <h3>📊 Demo Progress</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressBar"></div>
                    </div>
                    <div class="step-indicators">
                        <div class="step-indicator" id="step1">
                            <div class="step-circle">📝</div>
                            <div class="step-label">Collect</div>
                        </div>
                        <div class="step-indicator" id="step2">
                            <div class="step-circle">🧠</div>
                            <div class="step-label">Process</div>
                        </div>
                        <div class="step-indicator" id="step3">
                            <div class="step-circle">✅</div>
                            <div class="step-label">Complete</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chat-container">
                <div class="chat-header">
                    <div class="chat-title">Conversation</div>
                    <div class="status-indicator">
                        <span class="status-dot" id="statusDot"></span>
                        <span id="statusText">Ready</span>
                    </div>
                </div>

                <div class="chat-messages" id="chatMessages">
                    <!-- Messages will be inserted here -->
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global state
        let currentMode = 'demo';
        let demoState = {{
            isPlaying: false,
            isPaused: false,
            currentMessageIndex: 0,
            currentStep: 0,
            speed: 1,
            typingTimer: null,
            messageTimer: null
        }};

        let liveState = {{
            isConnected: false,
            apiKey: '',
            endpoint: ''
        }};

        // Demo script
        const demoScript = {demo_script};

        let currentScriptIndex = 0;
        let currentMessageIndex = 0;

        // Initialize on page load
        window.addEventListener('DOMContentLoaded', () => {{
            setupEventListeners();
            addInitialMessage();
        }});

        function setupEventListeners() {{
            const speedSlider = document.getElementById('speedSlider');
            speedSlider.addEventListener('input', (e) => {{
                demoState.speed = parseFloat(e.target.value);
                document.getElementById('speedLabel').textContent = `${{demoState.speed}}x`;
            }});
        }}

        function addInitialMessage() {{
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = `
                <div class="message assistant">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-header">
                            <span class="message-sender">AI Assistant</span>
                            <span class="message-time">${{getCurrentTime()}}</span>
                        </div>
                        <div class="message-text">
                            Welcome to the {title} Demo! 
                            
                            Click "Start Demo" to see how I can help, or switch to "Live Mode" to connect to your system.
                        </div>
                    </div>
                </div>
            `;
        }}

        function switchMode(mode) {{
            currentMode = mode;
            document.getElementById('demoModeBtn').classList.toggle('active', mode === 'demo');
            document.getElementById('liveModeBtn').classList.toggle('active', mode === 'live');
            document.getElementById('liveConfig').classList.toggle('active', mode === 'live');
            
            if (mode === 'demo') {{
                resetDemo();
            }} else {{
                const savedConfig = localStorage.getItem('agentConfig');
                if (savedConfig) {{
                    const config = JSON.parse(savedConfig);
                    document.getElementById('apiKey').value = config.apiKey || '';
                    document.getElementById('apiEndpoint').value = config.endpoint || '';
                }}
            }}
        }}

        async function testConnection() {{
            const apiKey = document.getElementById('apiKey').value;
            const endpoint = document.getElementById('apiEndpoint').value;
            
            if (!apiKey || !endpoint) {{
                updateConnectionStatus('error', 'Please enter both API Key and Endpoint');
                return;
            }}
            
            updateConnectionStatus('processing', 'Testing connection...');
            
            try {{
                const response = await fetch(endpoint, {{
                    method: 'POST',
                    headers: {{
                        'x-functions-key': apiKey,
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        action: 'health',
                        test: true
                    }})
                }});
                
                if (response.ok) {{
                    liveState.isConnected = true;
                    liveState.apiKey = apiKey;
                    liveState.endpoint = endpoint;
                    
                    localStorage.setItem('agentConfig', JSON.stringify({{
                        apiKey: apiKey,
                        endpoint: endpoint
                    }}));
                    
                    updateConnectionStatus('connected', 'Connected Successfully');
                }} else {{
                    throw new Error(`Connection failed: ${{response.status}}`);
                }}
            }} catch (error) {{
                updateConnectionStatus('error', `Connection Failed: ${{error.message}}`);
                liveState.isConnected = false;
            }}
        }}

        function updateConnectionStatus(status, message) {{
            const statusElement = document.getElementById('connectionStatus');
            statusElement.className = `connection-status ${{status}}`;
            statusElement.innerHTML = `
                <span class="status-dot ${{status}}"></span>
                <span>${{message}}</span>
            `;
        }}

        function startDemo() {{
            if (demoState.isPlaying && !demoState.isPaused) return;
            
            demoState.isPlaying = true;
            demoState.isPaused = false;
            
            document.getElementById('startBtn').disabled = true;
            document.getElementById('pauseBtn').disabled = false;
            document.getElementById('skipBtn').disabled = false;
            
            updateStatus('processing', 'Running Demo...');
            
            if (currentScriptIndex === 0 && currentMessageIndex === 0) {{
                const messagesContainer = document.getElementById('chatMessages');
                messagesContainer.innerHTML = '';
            }}
            
            playNextMessage();
        }}

        function pauseDemo() {{
            demoState.isPaused = true;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
            
            clearTimeout(demoState.messageTimer);
            clearTimeout(demoState.typingTimer);
            
            updateStatus('idle', 'Paused');
        }}

        function resetDemo() {{
            clearTimeout(demoState.messageTimer);
            clearTimeout(demoState.typingTimer);
            
            demoState.isPlaying = false;
            demoState.isPaused = false;
            demoState.currentStep = 0;
            currentScriptIndex = 0;
            currentMessageIndex = 0;
            
            document.getElementById('startBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
            document.getElementById('skipBtn').disabled = true;
            
            document.getElementById('progressBar').style.width = '0%';
            
            document.querySelectorAll('.step-indicator').forEach(step => {{
                step.classList.remove('active', 'completed');
            }});
            
            updateStatus('idle', 'Ready');
            addInitialMessage();
        }}

        function skipToNext() {{
            clearTimeout(demoState.messageTimer);
            clearTimeout(demoState.typingTimer);
            
            currentMessageIndex++;
            if (currentMessageIndex >= demoScript[currentScriptIndex].messages.length) {{
                currentScriptIndex++;
                currentMessageIndex = 0;
            }}
            
            if (currentScriptIndex < demoScript.length) {{
                playNextMessage();
            }}
        }}

        function playNextMessage() {{
            if (!demoState.isPlaying || demoState.isPaused) return;
            
            if (currentScriptIndex >= demoScript.length) {{
                completeDemo();
                return;
            }}
            
            const currentSection = demoScript[currentScriptIndex];
            const currentMessage = currentSection.messages[currentMessageIndex];
            
            if (!currentMessage) {{
                currentScriptIndex++;
                currentMessageIndex = 0;
                if (currentScriptIndex < demoScript.length) {{
                    playNextMessage();
                }} else {{
                    completeDemo();
                }}
                return;
            }}
            
            showTypingIndicator();
            
            demoState.typingTimer = setTimeout(() => {{
                hideTypingIndicator();
                addMessage(currentMessage, currentSection);
                
                updateProgress();
                
                if (currentMessage.action) {{
                    updateStep(currentMessage.action);
                }}
                
                currentMessageIndex++;
                if (currentMessageIndex >= currentSection.messages.length) {{
                    currentScriptIndex++;
                    currentMessageIndex = 0;
                }}
                
                const delay = (currentMessage.delay || 2000) / demoState.speed;
                demoState.messageTimer = setTimeout(() => {{
                    playNextMessage();
                }}, delay);
                
            }}, (currentMessage.typingTime || 2000) / demoState.speed);
        }}

        function addMessage(message, section) {{
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{message.role}}`;
            
            let contentHTML = `
                <div class="message-avatar">${{message.role === 'user' ? '👤' : '🤖'}}</div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-sender">${{message.role === 'user' ? 'You' : 'AI Assistant'}}</span>
                        <span class="message-time">${{getCurrentTime()}}</span>
                    </div>
                    <div class="message-text">${{message.content}}</div>
            `;
            
            if (message.showResult && message.resultData) {{
                contentHTML += createResultCard(message.resultData);
            }}
            
            contentHTML += '</div>';
            messageDiv.innerHTML = contentHTML;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        function createResultCard(data) {{
            let html = '';
            
            for (const [key, value] of Object.entries(data)) {{
                html += `
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-title">${{key.charAt(0).toUpperCase() + key.slice(1)}}</div>
                            <div class="result-status">Success</div>
                        </div>
                        <div class="result-fields">
                `;
                
                for (const [field, fieldValue] of Object.entries(value)) {{
                    html += `
                        <div class="result-field">
                            <div class="result-label">${{field.replace(/([A-Z])/g, ' $1').trim()}}:</div>
                            <div class="result-value">${{fieldValue}}</div>
                        </div>
                    `;
                }}
                
                html += `
                        </div>
                    </div>
                `;
            }}
            
            return html;
        }}

        function showTypingIndicator() {{
            const messagesContainer = document.getElementById('chatMessages');
            const indicator = document.createElement('div');
            indicator.className = 'typing-indicator active';
            indicator.id = 'typingIndicator';
            indicator.innerHTML = `
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            messagesContainer.appendChild(indicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        function hideTypingIndicator() {{
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {{
                indicator.remove();
            }}
        }}

        function updateProgress() {{
            const totalMessages = demoScript.reduce((sum, section) => sum + section.messages.length, 0);
            const currentProgress = (currentScriptIndex * 10 + currentMessageIndex) / totalMessages * 100;
            document.getElementById('progressBar').style.width = `${{currentProgress}}%`;
        }}

        function updateStep(action) {{
            if (action === 'step1') {{
                document.getElementById('step1').classList.add('active');
            }} else if (action === 'step2') {{
                document.getElementById('step1').classList.remove('active');
                document.getElementById('step1').classList.add('completed');
                document.getElementById('step2').classList.add('active');
            }} else if (action === 'step3') {{
                document.getElementById('step2').classList.remove('active');
                document.getElementById('step2').classList.add('completed');
                document.getElementById('step3').classList.add('active');
            }}
        }}

        function updateStatus(status, text) {{
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            
            statusDot.className = `status-dot ${{status}}`;
            statusText.textContent = text;
        }}

        function completeDemo() {{
            demoState.isPlaying = false;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
            document.getElementById('skipBtn').disabled = true;
            
            document.getElementById('step3').classList.remove('active');
            document.getElementById('step3').classList.add('completed');
            
            document.getElementById('progressBar').style.width = '100%';
            
            updateStatus('idle', 'Demo Complete');
        }}

        function getCurrentTime() {{
            const now = new Date();
            return now.toLocaleTimeString('en-US', {{ hour: '2-digit', minute: '2-digit' }});
        }}
    </script>
</body>
</html>'''

# Demo configurations for all 60 stacks
demos = {
    # Healthcare Stack (5 demos)
    "patient_intake_stack": {
        "title": "Patient Intake Agent",
        "emoji": "🏥",
        "description": "Streamline patient registration with AI-powered conversational intake",
        "path": "healthcare_stack/patient_intake_stack/demos/patient_intake_demo.html"
    },
    "prior_authorization_stack": {
        "title": "Prior Authorization Agent", 
        "emoji": "📋",
        "description": "Automate insurance prior authorization requests and status tracking",
        "path": "healthcare_stack/prior_authorization_stack/demos/prior_authorization_demo.html"
    },
    "clinical_notes_summarizer_stack": {
        "title": "Clinical Notes Summarizer",
        "emoji": "📝",
        "description": "Summarize clinical consultations and generate structured documentation",
        "path": "healthcare_stack/clinical_notes_summarizer_stack/demos/clinical_notes_summarizer_demo.html"
    },
    "care_gap_closure_stack": {
        "title": "Care Gap Closure Agent",
        "emoji": "🎯",
        "description": "Identify and close care gaps for improved patient outcomes",
        "path": "healthcare_stack/care_gap_closure_stack/demos/care_gap_closure_demo.html"
    },
    "staff_credentialing_stack": {
        "title": "Staff Credentialing Agent",
        "emoji": "🏆",
        "description": "Track and manage healthcare staff credentials and certifications",
        "path": "healthcare_stack/staff_credentialing_stack/demos/staff_credentialing_demo.html"
    },
    
    # Energy Stack (5 demos)
    "asset_maintenance_forecast_stack": {
        "title": "Asset Maintenance Forecast",
        "emoji": "⚡",
        "description": "Predict maintenance needs for energy infrastructure assets",
        "path": "energy_stack/asset_maintenance_forecast_stack/demos/asset_maintenance_forecast_demo.html"
    },
    "regulatory_reporting_stack": {
        "title": "Regulatory Reporting Agent",
        "emoji": "📊",
        "description": "Generate compliant EPA and regulatory reports automatically",
        "path": "energy_stack/regulatory_reporting_stack/demos/regulatory_reporting_demo.html"
    },
    "field_service_dispatch_stack": {
        "title": "Field Service Dispatch",
        "emoji": "🔧",
        "description": "Optimize technician dispatch for emergency and routine service",
        "path": "energy_stack/field_service_dispatch_stack/demos/field_service_dispatch_demo.html"
    },
    "emission_tracking_stack": {
        "title": "Emission Tracking Agent",
        "emoji": "🌍",
        "description": "Monitor and report emission trends across facilities",
        "path": "energy_stack/emission_tracking_stack/demos/emission_tracking_demo.html"
    },
    "permit_license_management_stack": {
        "title": "Permit License Management",
        "emoji": "📜",
        "description": "Track and manage permits and licenses with expiration alerts",
        "path": "energy_stack/permit_license_management_stack/demos/permit_license_management_demo.html"
    },
    
    # Manufacturing Stack (5 demos)
    "supplier_risk_monitoring_stack": {
        "title": "Supplier Risk Monitor",
        "emoji": "🏭",
        "description": "Analyze supply chain risks and vendor dependencies",
        "path": "manufacturing_stack/supplier_risk_monitoring_stack/demos/supplier_risk_monitoring_demo.html"
    },
    "production_line_optimization_stack": {
        "title": "Production Optimization",
        "emoji": "⚙️",
        "description": "Optimize production line throughput and efficiency",
        "path": "manufacturing_stack/production_line_optimization_stack/demos/production_line_optimization_demo.html"
    },
    "inventory_rebalancing_stack": {
        "title": "Inventory Rebalancing",
        "emoji": "📦",
        "description": "Balance inventory levels across warehouses intelligently",
        "path": "manufacturing_stack/inventory_rebalancing_stack/demos/inventory_rebalancing_demo.html"
    },
    "maintenance_scheduling_stack": {
        "title": "Maintenance Scheduling",
        "emoji": "🔨",
        "description": "Schedule preventive maintenance for production equipment",
        "path": "manufacturing_stack/maintenance_scheduling_stack/demos/maintenance_scheduling_demo.html"
    },
    "order_status_communication_stack": {
        "title": "Order Status Communication",
        "emoji": "📬",
        "description": "Update customers on order status and delivery tracking",
        "path": "manufacturing_stack/order_status_communication_stack/demos/order_status_communication_demo.html"
    },
    
    # Software/DP Stack (5 demos)
    "support_ticket_resolution_stack": {
        "title": "Support Ticket Resolution",
        "emoji": "🎫",
        "description": "Resolve customer support tickets with AI assistance",
        "path": "software_dp_stack/support_ticket_resolution_stack/demos/support_ticket_resolution_demo.html"
    },
    "customer_onboarding_stack": {
        "title": "Customer Onboarding",
        "emoji": "🚀",
        "description": "Streamline new customer onboarding and setup",
        "path": "software_dp_stack/customer_onboarding_stack/demos/customer_onboarding_demo.html"
    },
    "competitive_intel_stack": {
        "title": "Competitive Intelligence",
        "emoji": "🔍",
        "description": "Track competitor features and market positioning",
        "path": "software_dp_stack/competitive_intel_stack/demos/competitive_intel_demo.html"
    },
    "product_feedback_synthesizer_stack": {
        "title": "Product Feedback Synthesizer",
        "emoji": "💭",
        "description": "Analyze and synthesize customer product feedback",
        "path": "software_dp_stack/product_feedback_synthesizer_stack/demos/product_feedback_synthesizer_demo.html"
    },
    "license_renewal_expansion_stack": {
        "title": "License Renewal & Expansion",
        "emoji": "📈",
        "description": "Manage license renewals and identify expansion opportunities",
        "path": "software_dp_stack/license_renewal_expansion_stack/demos/license_renewal_expansion_demo.html"
    },
    
    # Professional Services Stack (5 demos)
    "contract_risk_review_stack": {
        "title": "Contract Risk Review",
        "emoji": "⚖️",
        "description": "Review contracts for risk clauses and compliance issues",
        "path": "professional_services_stack/contract_risk_review_stack/demos/contract_risk_review_demo.html"
    },
    "time_entry_billing_stack": {
        "title": "Time Entry & Billing",
        "emoji": "⏰",
        "description": "Generate invoices from project time tracking",
        "path": "professional_services_stack/time_entry_billing_stack/demos/time_entry_billing_demo.html"
    },
    "proposal_copilot_stack": {
        "title": "Proposal Copilot",
        "emoji": "📄",
        "description": "Create winning proposals for client projects",
        "path": "professional_services_stack/proposal_copilot_stack/demos/proposal_copilot_demo.html"
    },
    "resource_utilization_stack": {
        "title": "Resource Utilization",
        "emoji": "👥",
        "description": "Find available consultants with specific expertise",
        "path": "professional_services_stack/resource_utilization_stack/demos/resource_utilization_demo.html"
    },
    "client_health_score_stack": {
        "title": "Client Health Score",
        "emoji": "💚",
        "description": "Monitor account health and engagement metrics",
        "path": "professional_services_stack/client_health_score_stack/demos/client_health_score_demo.html"
    },
    
    # Retail/CPG Stack (5 demos)
    "inventory_visibility_stack": {
        "title": "Inventory Visibility",
        "emoji": "🛒",
        "description": "Check inventory levels across all store locations",
        "path": "retail_cpg_stack/inventory_visibility_stack/demos/inventory_visibility_demo.html"
    },
    "personalized_marketing_stack": {
        "title": "Personalized Marketing",
        "emoji": "🎯",
        "description": "Create targeted campaigns for high-value customers",
        "path": "retail_cpg_stack/personalized_marketing_stack/demos/personalized_marketing_demo.html"
    },
    "store_associate_copilot_stack": {
        "title": "Store Associate Copilot",
        "emoji": "🏪",
        "description": "Assist store associates with customer inquiries",
        "path": "retail_cpg_stack/store_associate_copilot_stack/demos/store_associate_copilot_demo.html"
    },
    "returns_complaints_resolution_stack": {
        "title": "Returns & Complaints Resolution",
        "emoji": "📦",
        "description": "Process returns and resolve customer complaints",
        "path": "retail_cpg_stack/returns_complaints_resolution_stack/demos/returns_complaints_resolution_demo.html"
    },
    "supply_chain_disruption_alert_stack": {
        "title": "Supply Chain Disruption Alert",
        "emoji": "🚨",
        "description": "Alert on supply chain disruptions and delays",
        "path": "retail_cpg_stack/supply_chain_disruption_alert_stack/demos/supply_chain_disruption_alert_demo.html"
    },
    
    # Financial Services Stack (10 demos)
    "customer_onboarding_fs_stack": {
        "title": "Customer Onboarding FS",
        "emoji": "🏦",
        "description": "Onboard new banking customers with compliance checks",
        "path": "financial_services_stack/customer_onboarding_fs_stack/demos/customer_onboarding_fs_demo.html"
    },
    "fraud_detection_alert_stack": {
        "title": "Fraud Detection Alert",
        "emoji": "🚨",
        "description": "Analyze suspicious transaction patterns in real-time",
        "path": "financial_services_stack/fraud_detection_alert_stack/demos/fraud_detection_alert_demo.html"
    },
    "loan_origination_assistant_stack": {
        "title": "Loan Origination Assistant",
        "emoji": "💰",
        "description": "Process mortgage and loan applications efficiently",
        "path": "financial_services_stack/loan_origination_assistant_stack/demos/loan_origination_assistant_demo.html"
    },
    "financial_advisor_copilot_stack": {
        "title": "Financial Advisor Copilot",
        "emoji": "📊",
        "description": "Investment recommendations for client portfolios",
        "path": "financial_services_stack/financial_advisor_copilot_stack/demos/financial_advisor_copilot_demo.html"
    },
    "claims_processing_stack": {
        "title": "Claims Processing",
        "emoji": "📋",
        "description": "Process insurance claims automatically",
        "path": "financial_services_stack/claims_processing_stack/demos/claims_processing_demo.html"
    },
    "regulatory_compliance_fs_stack": {
        "title": "Regulatory Compliance FS",
        "emoji": "✅",
        "description": "Check AML and regulatory compliance",
        "path": "financial_services_stack/regulatory_compliance_fs_stack/demos/regulatory_compliance_fs_demo.html"
    },
    "customer_sentiment_churn_stack": {
        "title": "Customer Sentiment & Churn",
        "emoji": "📉",
        "description": "Identify at-risk customers for retention",
        "path": "financial_services_stack/customer_sentiment_churn_stack/demos/customer_sentiment_churn_demo.html"
    },
    "portfolio_rebalancing_stack": {
        "title": "Portfolio Rebalancing",
        "emoji": "⚖️",
        "description": "Rebalance investment portfolios automatically",
        "path": "financial_services_stack/portfolio_rebalancing_stack/demos/portfolio_rebalancing_demo.html"
    },
    "wealth_insights_generator_stack": {
        "title": "Wealth Insights Generator",
        "emoji": "💎",
        "description": "Generate comprehensive wealth reports",
        "path": "financial_services_stack/wealth_insights_generator_stack/demos/wealth_insights_generator_demo.html"
    },
    "underwriting_support_stack": {
        "title": "Underwriting Support",
        "emoji": "🔍",
        "description": "Assess risk for insurance policy applications",
        "path": "financial_services_stack/underwriting_support_stack/demos/underwriting_support_demo.html"
    },
    
    # SLG Government Stack (5 demos)
    "citizen_service_request_stack": {
        "title": "Citizen Service Request",
        "emoji": "🏛️",
        "description": "Report issues and request city services",
        "path": "slg_government_stack/citizen_service_request_stack/demos/citizen_service_request_demo.html"
    },
    "grants_management_stack": {
        "title": "Grants Management",
        "emoji": "💵",
        "description": "Track grant applications and funding status",
        "path": "slg_government_stack/grants_management_stack/demos/grants_management_demo.html"
    },
    "building_permit_processing_stack": {
        "title": "Building Permit Processing",
        "emoji": "🏗️",
        "description": "Apply for and track building permits",
        "path": "slg_government_stack/building_permit_processing_stack/demos/building_permit_processing_demo.html"
    },
    "utility_billing_assistance_stack": {
        "title": "Utility Billing Assistance",
        "emoji": "💡",
        "description": "Help citizens with utility bill assistance programs",
        "path": "slg_government_stack/utility_billing_assistance_stack/demos/utility_billing_assistance_demo.html"
    },
    "foia_request_assistant_stack": {
        "title": "FOIA Request Assistant",
        "emoji": "📂",
        "description": "Process Freedom of Information Act requests",
        "path": "slg_government_stack/foia_request_assistant_stack/demos/foia_request_assistant_demo.html"
    },
    
    # Federal Government Stack (5 demos)
    "regulatory_compliance_fed_stack": {
        "title": "Regulatory Compliance Federal",
        "emoji": "🛡️",
        "description": "Verify FedRAMP and federal compliance requirements",
        "path": "federal_government_stack/regulatory_compliance_fed_stack/demos/regulatory_compliance_fed_demo.html"
    },
    "federal_grants_oversight_stack": {
        "title": "Federal Grants Oversight",
        "emoji": "📊",
        "description": "Track federal grant spending and compliance",
        "path": "federal_government_stack/federal_grants_oversight_stack/demos/federal_grants_oversight_demo.html"
    },
    "acquisition_support_stack": {
        "title": "Acquisition Support",
        "emoji": "🤝",
        "description": "Evaluate vendor proposals for government contracts",
        "path": "federal_government_stack/acquisition_support_stack/demos/acquisition_support_demo.html"
    },
    "workforce_clearance_onboarding_stack": {
        "title": "Workforce Clearance & Onboarding",
        "emoji": "🎖️",
        "description": "Process security clearances for new employees",
        "path": "federal_government_stack/workforce_clearance_onboarding_stack/demos/workforce_clearance_onboarding_demo.html"
    },
    "mission_reporting_assistant_stack": {
        "title": "Mission Reporting Assistant",
        "emoji": "📈",
        "description": "Generate mission status and progress reports",
        "path": "federal_government_stack/mission_reporting_assistant_stack/demos/mission_reporting_assistant_demo.html"
    },
    
    # B2B Sales Stack (5 demos)
    "sales_qualification_stack": {
        "title": "Sales Qualification",
        "emoji": "🎯",
        "description": "Qualify enterprise leads and opportunities",
        "path": "b2b_sales_stack/sales_qualification_stack/demos/sales_qualification_demo.html"
    },
    "account_intelligence_stack": {
        "title": "Account Intelligence",
        "emoji": "🧠",
        "description": "Get insights on accounts before meetings",
        "path": "b2b_sales_stack/account_intelligence_stack/demos/account_intelligence_demo.html"
    },
    "proposal_generation_stack": {
        "title": "Proposal Generation",
        "emoji": "📝",
        "description": "Generate proposals for enterprise deals",
        "path": "b2b_sales_stack/proposal_generation_stack/demos/proposal_generation_demo.html"
    },
    "deal_progression_stack": {
        "title": "Deal Progression",
        "emoji": "📈",
        "description": "Identify and progress stalled deals",
        "path": "b2b_sales_stack/deal_progression_stack/demos/deal_progression_demo.html"
    },
    "win_loss_analysis_stack": {
        "title": "Win/Loss Analysis",
        "emoji": "📊",
        "description": "Analyze why deals were won or lost",
        "path": "b2b_sales_stack/win_loss_analysis_stack/demos/win_loss_analysis_demo.html"
    },
    
    # B2C Sales Stack (5 demos)
    "personalized_shopping_assistant_stack": {
        "title": "Personalized Shopping Assistant",
        "emoji": "🛍️",
        "description": "Help customers find the perfect products",
        "path": "b2c_sales_stack/personalized_shopping_assistant_stack/demos/personalized_shopping_assistant_demo.html"
    },
    "cart_abandonment_recovery_stack": {
        "title": "Cart Abandonment Recovery",
        "emoji": "🛒",
        "description": "Follow up on abandoned shopping carts",
        "path": "b2c_sales_stack/cart_abandonment_recovery_stack/demos/cart_abandonment_recovery_demo.html"
    },
    "omnichannel_engagement_stack": {
        "title": "Omnichannel Engagement",
        "emoji": "📱",
        "description": "Coordinate campaigns across all channels",
        "path": "b2c_sales_stack/omnichannel_engagement_stack/demos/omnichannel_engagement_demo.html"
    },
    "returns_exchange_stack": {
        "title": "Returns & Exchange",
        "emoji": "🔄",
        "description": "Process returns and exchanges seamlessly",
        "path": "b2c_sales_stack/returns_exchange_stack/demos/returns_exchange_demo.html"
    },
    "customer_loyalty_rewards_stack": {
        "title": "Customer Loyalty & Rewards",
        "emoji": "⭐",
        "description": "Manage loyalty points and rewards programs",
        "path": "b2c_sales_stack/customer_loyalty_rewards_stack/demos/customer_loyalty_rewards_demo.html"
    }
}

# Generate demo scripts for each stack
def get_demo_script(stack_name):
    scripts = {
        "patient_intake_stack": '''[
            {
                type: 'conversation',
                messages: [
                    {
                        role: 'user',
                        content: 'Schedule an appointment for John Smith next Tuesday at 2 PM for a general checkup',
                        typingTime: 1500,
                        delay: 1000
                    },
                    {
                        role: 'assistant',
                        content: 'I\\'ll help you schedule an appointment for John Smith. Let me collect the necessary information and check availability...',
                        typingTime: 2000,
                        delay: 1500,
                        action: 'step1'
                    }
                ]
            },
            {
                type: 'result',
                messages: [
                    {
                        role: 'assistant',
                        content: '✅ Appointment scheduled successfully!',
                        showResult: true,
                        resultData: {
                            appointment: {
                                patientName: 'John Smith',
                                date: 'Tuesday, January 30, 2024',
                                time: '2:00 PM',
                                type: 'General Checkup',
                                provider: 'Dr. Sarah Johnson',
                                location: 'Main Clinic - Room 203'
                            }
                        },
                        typingTime: 2000,
                        delay: 1500,
                        action: 'step2'
                    }
                ]
            }
        ]''',
        
        "prior_authorization_stack": '''[
            {
                type: 'conversation',
                messages: [
                    {
                        role: 'user',
                        content: 'Check prior auth status for patient Mary Johnson\\'s MRI',
                        typingTime: 1500,
                        delay: 1000
                    },
                    {
                        role: 'assistant',
                        content: 'I\\'ll check the prior authorization status for Mary Johnson\\'s MRI request...',
                        typingTime: 2000,
                        delay: 1500,
                        action: 'step1'
                    }
                ]
            },
            {
                type: 'result',
                messages: [
                    {
                        role: 'assistant',
                        content: '✅ Prior Authorization Status Retrieved',
                        showResult: true,
                        resultData: {
                            authorization: {
                                patient: 'Mary Johnson',
                                procedure: 'MRI - Brain',
                                status: 'Approved',
                                authNumber: 'PA-2024-4521',
                                validThrough: 'February 15, 2024',
                                provider: 'Radiology Associates'
                            }
                        },
                        typingTime: 2000,
                        delay: 1500,
                        action: 'step2'
                    }
                ]
            }
        ]''',
        
        # Add more scripts for each stack...
    }
    
    # Default script if specific one not found
    default_script = '''[
        {
            type: 'conversation',
            messages: [
                {
                    role: 'user',
                    content: 'Help me with this task',
                    typingTime: 1500,
                    delay: 1000
                },
                {
                    role: 'assistant',
                    content: 'I\\'ll help you with that. Let me process your request...',
                    typingTime: 2000,
                    delay: 1500,
                    action: 'step1'
                }
            ]
        },
        {
            type: 'result',
            messages: [
                {
                    role: 'assistant',
                    content: '✅ Task completed successfully!',
                    showResult: true,
                    resultData: {
                        result: {
                            status: 'Complete',
                            timestamp: new Date().toISOString(),
                            details: 'Task processed successfully'
                        }
                    },
                    typingTime: 2000,
                    delay: 1500,
                    action: 'step2'
                }
            ]
        }
    ]'''
    
    return scripts.get(stack_name, default_script)

# Generate all demo files
def main():
    base_path = "/Users/kodyw/Documents/GitHub/AI-Agent-Templates/agents_lab"
    
    for stack_name, config in demos.items():
        demo_script = get_demo_script(stack_name)
        html_content = get_demo_template(
            config["title"],
            config["emoji"],
            config["description"],
            demo_script
        )
        
        file_path = os.path.join(base_path, config["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created: {config['path']}")

if __name__ == "__main__":
    main()
    print("\n✅ All 60 demo files have been updated with chat-based conversational pattern!")