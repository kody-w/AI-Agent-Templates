<#
.SYNOPSIS
    Deploys agents from the universal library to any Azure Function App based on manifest

.DESCRIPTION
    This script reads an agent manifest file and deploys the specified agents from the
    centralized library to the target Azure environment.

.PARAMETER ManifestPath
    Path to the agent-manifest.json file (local or URL)

.PARAMETER ResourceGroup
    Target resource group name

.PARAMETER StorageAccount
    Target storage account (auto-detected if not provided)

.PARAMETER SkipOptional
    Skip deployment of optional agents

.EXAMPLE
    .\deploy-agents.ps1 -ManifestPath "./templates/sales-voice-agent/agent-manifest.json" -ResourceGroup "rg-salesvoice"

.EXAMPLE
    .\deploy-agents.ps1 -ManifestPath "https://raw.githubusercontent.com/user/repo/main/agent-manifest.json" -ResourceGroup "rg-prod"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$ManifestPath,

    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,

    [Parameter(Mandatory=$false)]
    [string]$StorageAccount = "",

    [Parameter(Mandatory=$false)]
    [switch]$SkipOptional,

    [Parameter(Mandatory=$false)]
    [string]$AgentLibraryPath = "./agents",

    [Parameter(Mandatory=$false)]
    [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"

# Color functions
function Write-Status {
    param([string]$Message, [string]$Type = "Info")

    switch ($Type) {
        "Success" { Write-Host "✅ $Message" -ForegroundColor Green }
        "Error" { Write-Host "❌ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "Info" { Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
        default { Write-Host $Message }
    }
}

function Write-Step {
    param([string]$Step, [int]$Number)
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    Write-Host "  Step $Number: $Step" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
}

# Function to read manifest from file or URL
function Get-Manifest {
    param([string]$Path)

    if ($Path -match "^https?://") {
        Write-Status "Downloading manifest from URL..." "Info"
        $manifest = Invoke-RestMethod -Uri $Path
    }
    else {
        Write-Status "Reading manifest from local file..." "Info"
        if (-not (Test-Path $Path)) {
            throw "Manifest file not found: $Path"
        }
        $manifest = Get-Content $Path -Raw | ConvertFrom-Json
    }

    return $manifest
}

# Function to validate agent exists in library
function Test-AgentExists {
    param([string]$AgentPath, [string]$LibraryPath)

    $fullPath = Join-Path $LibraryPath "$AgentPath.py"
    return Test-Path $fullPath
}

# Function to get agent version
function Get-AgentVersion {
    param([string]$AgentPath, [string]$LibraryPath)

    $fullPath = Join-Path $LibraryPath "$AgentPath.py"
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw
        if ($content -match 'VERSION\s*=\s*"([^"]+)"') {
            return $matches[1]
        }
    }
    return "Unknown"
}

try {
    Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║               UNIVERSAL AGENT DEPLOYMENT TOOL                  ║
║                    Microsoft AI Accelerate                     ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

    # Step 1: Load and validate manifest
    Write-Step "Loading Agent Manifest" 1

    $manifest = Get-Manifest -Path $ManifestPath

    Write-Status "Manifest loaded: $($manifest.name) v$($manifest.version)" "Success"
    Write-Status "Description: $($manifest.description)" "Info"

    # Step 2: Validate agent library
    Write-Step "Validating Agent Library" 2

    if (-not (Test-Path $AgentLibraryPath)) {
        throw "Agent library not found at: $AgentLibraryPath"
    }

    $missingAgents = @()
    $agentVersions = @{}

    # Check required agents
    foreach ($agent in $manifest.agents.required) {
        if (Test-AgentExists -AgentPath $agent -LibraryPath $AgentLibraryPath) {
            $version = Get-AgentVersion -AgentPath $agent -LibraryPath $AgentLibraryPath
            $agentVersions[$agent] = $version
            Write-Status "✓ $agent (v$version)" "Success"
        }
        else {
            $missingAgents += $agent
            Write-Status "✗ $agent - NOT FOUND" "Error"
        }
    }

    # Check optional agents
    if (-not $SkipOptional -and $manifest.agents.optional) {
        Write-Status "`nChecking optional agents..." "Info"
        foreach ($agent in $manifest.agents.optional) {
            if (Test-AgentExists -AgentPath $agent -LibraryPath $AgentLibraryPath) {
                $version = Get-AgentVersion -AgentPath $agent -LibraryPath $AgentLibraryPath
                $agentVersions[$agent] = $version
                Write-Status "✓ $agent (v$version) [optional]" "Success"
            }
            else {
                Write-Status "○ $agent [optional] - Not found, skipping" "Warning"
            }
        }
    }

    if ($missingAgents.Count -gt 0) {
        throw "Missing required agents: $($missingAgents -join ', ')"
    }

    if ($ValidateOnly) {
        Write-Status "`nValidation completed successfully!" "Success"
        Write-Status "All required agents are available in the library." "Info"
        exit 0
    }

    # Step 3: Connect to Azure
    Write-Step "Connecting to Azure" 3

    $azVersion = az version 2>$null
    if (-not $azVersion) {
        throw "Azure CLI is not installed. Please install from: https://aka.ms/installazurecli"
    }

    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        Write-Status "Not logged in to Azure. Initiating login..." "Warning"
        az login
        $account = az account show | ConvertFrom-Json
    }

    Write-Status "Connected as: $($account.user.name)" "Success"

    # Step 4: Find storage account
    Write-Step "Locating Storage Resources" 4

    # Verify resource group exists
    $rg = az group show --name $ResourceGroup 2>$null | ConvertFrom-Json
    if (-not $rg) {
        throw "Resource group '$ResourceGroup' not found"
    }

    # Find or validate storage account
    if (-not $StorageAccount) {
        Write-Status "Auto-detecting storage account..." "Info"
        $storageAccounts = az storage account list --resource-group $ResourceGroup --output json | ConvertFrom-Json

        # Try to find function app storage
        $functionApps = az functionapp list --resource-group $ResourceGroup --output json | ConvertFrom-Json
        if ($functionApps.Count -gt 0) {
            $appSettings = az functionapp config appsettings list --name $functionApps[0].name --resource-group $ResourceGroup --output json | ConvertFrom-Json
            $storageConnection = ($appSettings | Where-Object { $_.name -eq "AzureWebJobsStorage" }).value
            if ($storageConnection -match "AccountName=([^;]+)") {
                $StorageAccount = $matches[1]
                Write-Status "Found storage account from Function App: $StorageAccount" "Success"
            }
        }

        if (-not $StorageAccount -and $storageAccounts.Count -eq 1) {
            $StorageAccount = $storageAccounts[0].name
            Write-Status "Found storage account: $StorageAccount" "Success"
        }
        elseif (-not $StorageAccount) {
            throw "Could not auto-detect storage account. Please specify with -StorageAccount parameter"
        }
    }

    # Get storage key
    Write-Status "Getting storage account key..." "Info"
    $storageKey = az storage account keys list `
        --resource-group $ResourceGroup `
        --account-name $StorageAccount `
        --query "[0].value" `
        --output tsv

    # Find file share
    Write-Status "Finding file share..." "Info"
    $fileShares = az storage share list `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output json | ConvertFrom-Json

    if ($fileShares.Count -eq 0) {
        throw "No file shares found in storage account"
    }

    $fileShareName = $fileShares[0].name
    Write-Status "Using file share: $fileShareName" "Info"

    # Step 5: Deploy agents
    Write-Step "Deploying Agents" 5

    # Create agents directory
    az storage directory create `
        --name "agents" `
        --share-name $fileShareName `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output none 2>$null

    $deployedCount = 0
    $allAgents = $manifest.agents.required
    if (-not $SkipOptional -and $manifest.agents.optional) {
        $allAgents += $manifest.agents.optional
    }

    foreach ($agentPath in $allAgents) {
        $agentFile = Join-Path $AgentLibraryPath "$agentPath.py"

        if (-not (Test-Path $agentFile)) {
            if ($manifest.agents.optional -contains $agentPath) {
                Write-Status "Skipping optional agent: $agentPath" "Warning"
                continue
            }
            else {
                throw "Required agent file not found: $agentFile"
            }
        }

        $fileName = Split-Path $agentPath -Leaf
        Write-Status "Deploying: $fileName.py (v$($agentVersions[$agentPath]))" "Info"

        # Upload agent file
        az storage file upload `
            --share-name $fileShareName `
            --source $agentFile `
            --path "agents/$fileName.py" `
            --account-name $StorageAccount `
            --account-key $storageKey `
            --output none

        $deployedCount++
    }

    # Step 6: Create configuration file
    Write-Step "Creating Configuration" 6

    $configData = @{
        manifest = $manifest
        deploymentTime = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        deployedAgents = $agentVersions
        configuration = $manifest.configuration
    }

    $configJson = $configData | ConvertTo-Json -Depth 10
    $configFile = Join-Path $env:TEMP "agent-config.json"
    $configJson | Out-File -FilePath $configFile -Encoding UTF8

    az storage file upload `
        --share-name $fileShareName `
        --source $configFile `
        --path "agents/config.json" `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output none

    Remove-Item $configFile -Force
    Write-Status "Configuration file created" "Success"

    # Step 7: Verify deployment
    Write-Step "Verifying Deployment" 7

    $deployedFiles = az storage file list `
        --share-name $fileShareName `
        --path "agents" `
        --account-name $StorageAccount `
        --account-key $storageKey `
        --output json | ConvertFrom-Json

    $deployedFileNames = $deployedFiles | Where-Object { $_.name -like "*.py" } | Select-Object -ExpandProperty name
    Write-Status "Deployed files: $($deployedFileNames -join ', ')" "Info"

    # Summary
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "  DEPLOYMENT COMPLETE" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

    Write-Host "`nDeployment Summary:"
    Write-Host "  Template:        " -NoNewline; Write-Host $manifest.name -ForegroundColor Yellow
    Write-Host "  Version:         " -NoNewline; Write-Host $manifest.version -ForegroundColor Yellow
    Write-Host "  Resource Group:  " -NoNewline; Write-Host $ResourceGroup -ForegroundColor Yellow
    Write-Host "  Storage Account: " -NoNewline; Write-Host $StorageAccount -ForegroundColor Yellow
    Write-Host "  File Share:      " -NoNewline; Write-Host $fileShareName -ForegroundColor Yellow
    Write-Host "  Agents Deployed: " -NoNewline; Write-Host "$deployedCount agents" -ForegroundColor Yellow

    Write-Host "`n✅ Agents deployed successfully!" -ForegroundColor Green
    Write-Host "`n📋 Next Steps:"
    Write-Host "  1. Deploy or update your Function App code"
    Write-Host "  2. Configure app settings if needed"
    Write-Host "  3. Test the agent endpoints"

}
catch {
    Write-Status "Deployment failed: $_" "Error"
    Write-Status "Error details: $($_.Exception.Message)" "Error"
    exit 1
}
