// Helper function to generate trading card HTML without template literals
function generateTradingCardHTML(template, agentCode) {
  // Escape HTML for code content
  function escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }
  
  const escapedCode = {};
  for (const [filename, code] of Object.entries(agentCode)) {
    escapedCode[filename] = escapeHtml(code);
  }
  
  // Build all the dynamic components
  const codeTabs = Object.keys(agentCode).map((filename, index) => 
    '<button class="code-tab' + (index === 0 ? ' active' : '') + '" onclick="showCode(\'' + filename + '\')">' + filename + '</button>'
  ).join('');
  
  const codeContent = Object.entries(escapedCode).map(([filename, code], index) => 
    '<div class="code-content" id="code-' + filename + '" style="display: ' + (index === 0 ? 'block' : 'none') + ';"><pre>' + code + '</pre></div>'
  ).join('');
  
  const demoButton = template.demo && template.demo.available ? 
    '<button onclick="window.location.href=\'' + template.demo.url + '\'" class="btn btn-success">🎮 Try Demo</button>' : '';
  
  const agentsList = template.agents.map(agentId => 
    '<div class="agent-item"><strong>' + agentId.replace(/_/g, ' ').replace('.py', '') + '</strong></div>'
  ).join('');
  
  const featuresHtml = (template.features || template.benefits || []).slice(0, 6).map(feature => 
    '<div class="feature-item"><span>✓</span><span>' + feature + '</span></div>'
  ).join('');
  
  let apiKeysHtml = '';
  if (template.technicalRequirements && template.technicalRequirements.apiKeys) {
    const keysHtml = template.technicalRequirements.apiKeys.map(key => 
      '<code style="background: white; padding: 0.25rem 0.5rem; border-radius: 4px;">' + key + '</code>'
    ).join('');
    
    apiKeysHtml = '<div style="margin-top: 1rem; padding: 1rem; background: #fef3c7; border-radius: 8px;">' +
      '<strong style="color: #92400e;">Required API Keys:</strong>' +
      '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">' + keysHtml + '</div></div>';
  }
  
  const complexityStars = template.complexity === 'starter' ? '⭐' : 
                         template.complexity === 'intermediate' ? '⭐⭐' : '⭐⭐⭐';
  
  const agentCodeJSON = JSON.stringify(agentCode);
  
  // Build HTML string
  let html = '';
  html += '<!DOCTYPE html>\n';
  html += '<html lang="en">\n';
  html += '<head>\n';
  html += '    <meta charset="UTF-8">\n';
  html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n';
  html += '    <title>' + template.name + ' - AI Agent Stack Trading Card</title>\n';
  html += '    <style>\n';
  html += '        * { margin: 0; padding: 0; box-sizing: border-box; }\n';
  html += '        body { font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }\n';
  html += '        .trading-card { max-width: 1400px; margin: 0 auto; background: white; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }\n';
  html += '        .card-header { background: linear-gradient(135deg, #742774 0%, #00a651 100%); color: white; padding: 2rem; position: relative; overflow: hidden; }\n';
  html += '        .card-header::before { content: ""; position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: shimmer 3s infinite; }\n';
  html += '        @keyframes shimmer { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(180deg); } }\n';
  html += '        .card-title { font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; position: relative; z-index: 1; }\n';
  html += '        .card-subtitle { font-size: 1.2rem; opacity: 0.95; position: relative; z-index: 1; }\n';
  html += '        .card-badges { display: flex; gap: 1rem; margin-top: 1rem; position: relative; z-index: 1; }\n';
  html += '        .badge { padding: 0.5rem 1rem; background: rgba(255, 255, 255, 0.2); border-radius: 20px; font-weight: 600; }\n';
  html += '        .card-content { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; padding: 2rem; }\n';
  html += '        .section { background: #f8f9fa; padding: 1.5rem; border-radius: 12px; }\n';
  html += '        .section h3 { color: #333; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }\n';
  html += '        .agent-list { display: flex; flex-direction: column; gap: 0.5rem; }\n';
  html += '        .agent-item { background: white; padding: 0.75rem; border-radius: 8px; border-left: 3px solid #742774; }\n';
  html += '        .feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }\n';
  html += '        .feature-item { display: flex; align-items: center; gap: 0.5rem; color: #666; }\n';
  html += '        .deployment-section { grid-column: 1 / -1; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #0ea5e9; }\n';
  html += '        .code-section { grid-column: 1 / -1; background: #1e1e1e; color: #d4d4d4; font-family: "Consolas", "Monaco", monospace; position: relative; }\n';
  html += '        .code-tabs { display: flex; background: #2d2d2d; border-bottom: 1px solid #3e3e3e; overflow-x: auto; }\n';
  html += '        .code-tab { padding: 0.75rem 1.5rem; background: none; border: none; color: #d4d4d4; cursor: pointer; white-space: nowrap; transition: background 0.3s; }\n';
  html += '        .code-tab:hover { background: #3e3e3e; }\n';
  html += '        .code-tab.active { background: #1e1e1e; color: #4fc3f7; border-bottom: 2px solid #4fc3f7; }\n';
  html += '        .code-content { padding: 1.5rem; max-height: 400px; overflow-y: auto; }\n';
  html += '        .code-content pre { white-space: pre-wrap; word-wrap: break-word; }\n';
  html += '        .action-buttons { padding: 2rem; background: #f8f9fa; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }\n';
  html += '        .btn { padding: 1rem 2rem; border: none; border-radius: 8px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; }\n';
  html += '        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); }\n';
  html += '        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }\n';
  html += '        .btn-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }\n';
  html += '        .btn-azure { background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; }\n';
  html += '        .status-indicator { width: 12px; height: 12px; background: #10b981; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; }\n';
  html += '        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }\n';
  html += '        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; padding: 1.5rem; background: white; border-radius: 12px; margin-bottom: 2rem; }\n';
  html += '        .stat-item { text-align: center; padding: 1rem; }\n';
  html += '        .stat-value { font-size: 2rem; font-weight: bold; color: #742774; }\n';
  html += '        .stat-label { color: #666; font-size: 0.9rem; margin-top: 0.25rem; }\n';
  html += '        @media (max-width: 768px) { .card-content { grid-template-columns: 1fr; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }\n';
  html += '    </style>\n';
  html += '</head>\n';
  html += '<body>\n';
  html += '    <div class="trading-card">\n';
  html += '        <div class="card-header">\n';
  html += '            <h1 class="card-title">🎴 ' + template.name + '</h1>\n';
  html += '            <p class="card-subtitle">' + template.description + '</p>\n';
  html += '            <div class="card-badges">\n';
  html += '                <span class="badge">📦 ' + template.agents.length + ' Agents</span>\n';
  html += '                <span class="badge">⚡ ' + template.complexity + '</span>\n';
  html += '                <span class="badge">⏱️ ' + template.estimatedTime + '</span>\n';
  html += '                <span class="badge">✨ ' + (template.version || 'v1.0.0') + '</span>\n';
  html += '            </div>\n';
  html += '        </div>\n';
  html += '        <div class="stats-grid">\n';
  html += '            <div class="stat-item">\n';
  html += '                <div class="stat-value">' + template.agents.length + '</div>\n';
  html += '                <div class="stat-label">Total Agents</div>\n';
  html += '            </div>\n';
  html += '            <div class="stat-item">\n';
  html += '                <div class="stat-value">' + complexityStars + '</div>\n';
  html += '                <div class="stat-label">Complexity</div>\n';
  html += '            </div>\n';
  html += '            <div class="stat-item">\n';
  html += '                <div class="stat-value">' + template.estimatedTime.split(' ')[0] + '</div>\n';
  html += '                <div class="stat-label">Setup Time</div>\n';
  html += '            </div>\n';
  html += '            <div class="stat-item">\n';
  html += '                <div class="stat-value"><span class="status-indicator"></span></div>\n';
  html += '                <div class="stat-label">Ready to Deploy</div>\n';
  html += '            </div>\n';
  html += '        </div>\n';
  html += '        <div class="card-content">\n';
  html += '            <div class="section">\n';
  html += '                <h3>📦 Stack Components</h3>\n';
  html += '                <div class="agent-list">\n';
  html += '                    ' + agentsList + '\n';
  html += '                </div>\n';
  html += '            </div>\n';
  html += '            <div class="section">\n';
  html += '                <h3>✨ Key Features</h3>\n';
  html += '                <div class="feature-grid">\n';
  html += '                    ' + featuresHtml + '\n';
  html += '                </div>\n';
  html += '            </div>\n';
  html += '            <div class="section deployment-section">\n';
  html += '                <h3>🚀 Azure Deployment Instructions</h3>\n';
  html += '                <ol style="margin-left: 1.5rem; color: #0369a1;">\n';
  html += '                    <li style="margin: 0.5rem 0;">\n';
  html += '                        <strong>Deploy Base Infrastructure:</strong><br>\n';
  html += '                        Visit <a href="https://github.com/kody-w/Copilot-Agent-365" target="_blank" style="color: #0ea5e9;">Copilot-Agent-365</a> and click "Deploy to Azure"\n';
  html += '                    </li>\n';
  html += '                    <li style="margin: 0.5rem 0;">\n';
  html += '                        <strong>Run Setup Script:</strong><br>\n';
  html += '                        After deployment, copy the setup script from Azure Portal Outputs tab\n';
  html += '                    </li>\n';
  html += '                    <li style="margin: 0.5rem 0;">\n';
  html += '                        <strong>Add Stack Agents:</strong><br>\n';
  html += '                        Copy the agent files below to your Copilot-Agent-365/agents/ folder\n';
  html += '                    </li>\n';
  html += '                    <li style="margin: 0.5rem 0;">\n';
  html += '                        <strong>Test Your Stack:</strong><br>\n';
  html += '                        Run <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">func start</code> and test with the included demo\n';
  html += '                    </li>\n';
  html += '                </ol>\n';
  html += '                ' + apiKeysHtml + '\n';
  html += '            </div>\n';
  html += '            <div class="section code-section">\n';
  html += '                <div class="code-tabs">\n';
  html += '                    ' + codeTabs + '\n';
  html += '                </div>\n';
  html += '                ' + codeContent + '\n';
  html += '            </div>\n';
  html += '        </div>\n';
  html += '        <div class="action-buttons">\n';
  html += '            <a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2FCopilot-Agent-365%2Fmain%2Fazuredeploy.json" target="_blank" class="btn btn-azure">☁️ Deploy to Azure</a>\n';
  html += '            ' + demoButton + '\n';
  html += '            <button onclick="copyAgentCode()" class="btn btn-primary">📋 Copy All Agent Code</button>\n';
  html += '        </div>\n';
  html += '    </div>\n';
  html += '    <script>\n';
  html += '        function showCode(filename) {\n';
  html += '            document.querySelectorAll(".code-content").forEach(content => {\n';
  html += '                content.style.display = "none";\n';
  html += '            });\n';
  html += '            document.querySelectorAll(".code-tab").forEach(tab => {\n';
  html += '                tab.classList.remove("active");\n';
  html += '            });\n';
  html += '            const codeElement = document.getElementById("code-" + filename);\n';
  html += '            if (codeElement) {\n';
  html += '                codeElement.style.display = "block";\n';
  html += '            }\n';
  html += '            event.target.classList.add("active");\n';
  html += '        }\n';
  html += '        function copyAgentCode() {\n';
  html += '            const allCode = ' + agentCodeJSON + ';\n';
  html += '            const codeText = Object.entries(allCode).map(([filename, code]) => {\n';
  html += '                return "# File: " + filename + "\\n\\n" + code;\n';
  html += '            }).join("\\n\\n" + "=".repeat(80) + "\\n\\n");\n';
  html += '            navigator.clipboard.writeText(codeText).then(() => {\n';
  html += '                alert("All agent code copied to clipboard!");\n';
  html += '            }).catch(err => {\n';
  html += '                console.error("Failed to copy:", err);\n';
  html += '                alert("Failed to copy code. Please select and copy manually.");\n';
  html += '            });\n';
  html += '        }\n';
  html += '        document.addEventListener("DOMContentLoaded", () => {\n';
  html += '            document.querySelectorAll(".stat-value").forEach((stat, index) => {\n';
  html += '                stat.style.opacity = "0";\n';
  html += '                stat.style.transform = "translateY(20px)";\n';
  html += '                setTimeout(() => {\n';
  html += '                    stat.style.transition = "all 0.5s ease";\n';
  html += '                    stat.style.opacity = "1";\n';
  html += '                    stat.style.transform = "translateY(0)";\n';
  html += '                }, index * 100);\n';
  html += '            });\n';
  html += '        });\n';
  html += '    </script>\n';
  html += '</body>\n';
  html += '</html>';
  
  return html;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = generateTradingCardHTML;
}