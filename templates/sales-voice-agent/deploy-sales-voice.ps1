<#
.SYNOPSIS
    Deploys the Sales Voice Copilot infrastructure to Azure using centralized agents

.DESCRIPTION
    This script automates the deployment of all Azure resources required for the Sales Voice Copilot,
    including Function App, Storage, Key Vault, and pulls agents from the central library.

.PARAMETER ResourceGroupName
    Name of the resource group to create/use

.PARAMETER Location
    Azure region for deployment

.PARAMETER ProjectName
    Project name prefix for resources (3-11 characters)

.PARAMETER AzureOpenAIEndpoint
    Your Azure OpenAI endpoint URL

.PARAMETER AzureOpenAIApiKey
    Your Azure OpenAI API key

.PARAMETER SkipAgentUpload
    Skip the agent deployment step

.EXAMPLE
    .\deploy-sales-voice.ps1 -ResourceGroupName "rg-salesvoice-prod" -Location "East US" -ProjectName "salesvoice" -AzureOpenAIEndpoint "https://myopenai.openai.azure.com/" -AzureOpenAIApiKey "mykey"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory=$true)]
    [string]$Location,

    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "salesvoice",

    [Parameter(Mandatory=$true)]
    [string]$AzureOpenAIEndpoint,

    [Parameter(Mandatory=$true)]
    [string]$AzureOpenAIApiKey,

    [Parameter(Mandatory=$false)]
    [string]$AzureOpenAIDeploymentName = "gpt-4",

    [Parameter(Mandatory=$false)]
    [bool]$EnableDynamics365 = $false,

    [Parameter(Mandatory=$false)]
    [string]$Dynamics365Resource = "",

    [Parameter(Mandatory=$false)]
    [string]$Dynamics365ClientId = "",

    [Parameter(Mandatory=$false)]
    [string]$Dynamics365ClientSecret = "",

    [Parameter(Mandatory=$false)]
    [bool]$EnableSharePoint = $false,

    [Parameter(Mandatory=$false)]
    [string]$SharePointSiteUrl = "",

    [Parameter(Mandatory=$false)]
    [string]$SharePointClientId = "",

    [Parameter(Mandatory=$false)]
    [string]$SharePointClientSecret = "",

    [Parameter(Mandatory=$false)]
    [bool]$EnableVoiceServices = $true,

    [Parameter(Mandatory=$false)]
    [string]$Environment = "Production",

    [Parameter(Mandatory=$false)]
    [switch]$SkipAgentUpload,

    [Parameter(Mandatory=$false)]
    [switch]$UseExistingResourceGroup,

    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername = "YOUR-USERNAME"
)

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Color coding for output
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

try {
    # Display deployment banner
    Clear-Host
    Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║         SALES VOICE COPILOT DEPLOYMENT (v2.0)                 ║
║              With Centralized Agent Library                    ║
║                  Microsoft AI Accelerate                       ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

    Write-Status "Starting deployment process..." "Info"
    Write-Status "Project: $ProjectName" "Info"
    Write-Status "Location: $Location" "Info"
    Write-Status "Environment: $Environment" "Info"

    # Step 1: Check Azure CLI
    Write-Step "Checking Prerequisites" 1

    $azVersion = az version 2>$null
    if (-not $azVersion) {
        throw "Azure CLI is not installed. Please install from: https://aka.ms/installazurecli"
    }
    Write-Status "Azure CLI is installed" "Success"

    # Check if logged in
    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        Write-Status "Not logged in to Azure. Initiating login..." "Warning"
        az login
        $account = az account show | ConvertFrom-Json
    }
    Write-Status "Logged in as: $($account.user.name)" "Success"
    Write-Status "Subscription: $($account.name) ($($account.id))" "Info"

    # Step 2: Create or verify resource group
    Write-Step "Setting up Resource Group" 2

    if ($UseExistingResourceGroup) {
        $rg = az group show --name $ResourceGroupName 2>$null | ConvertFrom-Json
        if (-not $rg) {
            throw "Resource group '$ResourceGroupName' not found"
        }
        Write-Status "Using existing resource group: $ResourceGroupName" "Success"
    }
    else {
        Write-Status "Creating resource group: $ResourceGroupName" "Info"
        az group create `
            --name $ResourceGroupName `
            --location $Location `
            --tags "Application=SalesVoiceCopilot" "Environment=$Environment" | Out-Null
        Write-Status "Resource group created successfully" "Success"
    }

    # Step 3: Prepare parameters
    Write-Step "Preparing Deployment Parameters" 3

    # Set the manifest and library URLs
    $manifestUrl = "https://raw.githubusercontent.com/$GitHubUsername/AI-AGENT-TEMPLATES/main/templates/sales-voice-agent/agent-manifest.json"
    $agentLibraryUrl = "https://github.com/$GitHubUsername/AI-AGENT-TEMPLATES/archive/refs/heads/main.zip"

    $parameters = @{
        projectName = @{ value = $ProjectName }
        location = @{ value = $Location }
        manifestUrl = @{ value = $manifestUrl }
        agentLibraryUrl = @{ value = $agentLibraryUrl }
        azureOpenAIEndpoint = @{ value = $AzureOpenAIEndpoint }
        azureOpenAIApiKey = @{ value = $AzureOpenAIApiKey }
        azureOpenAIDeploymentName = @{ value = $AzureOpenAIDeploymentName }
        enableDynamics365 = @{ value = $EnableDynamics365 }
        dynamics365Resource = @{ value = $Dynamics365Resource }
        dynamics365ClientId = @{ value = $Dynamics365ClientId }
        dynamics365ClientSecret = @{ value = $Dynamics365ClientSecret }
        enableSharePoint = @{ value = $EnableSharePoint }
        sharePointSiteUrl = @{ value = $SharePointSiteUrl }
        sharePointClientId = @{ value = $SharePointClientId }
        sharePointClientSecret = @{ value = $SharePointClientSecret }
        enableVoiceServices = @{ value = $EnableVoiceServices }
        tagEnvironment = @{ value = $Environment }
    }

    $parametersJson = $parameters | ConvertTo-Json -Depth 10
    $parametersFile = Join-Path $env:TEMP "sales-voice-params-$(Get-Date -Format 'yyyyMMddHHmmss').json"
    $parametersJson | Out-File $parametersFile -Encoding UTF8

    Write-Status "Parameters file created: $parametersFile" "Success"

    # Step 4: Deploy ARM template
    Write-Step "Deploying Azure Resources" 4

    Write-Status "Starting ARM template deployment (this may take 10-15 minutes)..." "Info"
    Write-Status "This includes:" "Info"
    Write-Status "  - Function App with Python 3.9 runtime" "Info"
    Write-Status "  - Storage Account with File Shares" "Info"
    Write-Status "  - Key Vault for secure secrets" "Info"
    Write-Status "  - Application Insights for monitoring" "Info"
    if ($EnableVoiceServices) {
        Write-Status "  - Speech Services for voice capabilities" "Info"
    }
    Write-Status "  - Automated agent deployment from central library" "Info"

    # Check if template file exists locally
    $templateFile = Join-Path $PSScriptRoot "azuredeploy.json"
    if (-not (Test-Path $templateFile)) {
        Write-Status "Local template not found, using GitHub URL" "Warning"
        $templateFile = "https://raw.githubusercontent.com/$GitHubUsername/AI-AGENT-TEMPLATES/main/templates/sales-voice-agent/azuredeploy.json"
    }

    $deploymentName = "salesvoice-deployment-$(Get-Date -Format 'yyyyMMddHHmmss')"

    $deployment = az deployment group create `
        --name $deploymentName `
        --resource-group $ResourceGroupName `
        --template-file $templateFile `
        --parameters $parametersFile `
        --output json | ConvertFrom-Json

    if ($deployment.properties.provisioningState -ne "Succeeded") {
        throw "Deployment failed with state: $($deployment.properties.provisioningState)"
    }

    Write-Status "ARM template deployment completed successfully!" "Success"

    # Extract outputs
    $outputs = $deployment.properties.outputs
    $functionAppName = $outputs.functionAppName.value
    $functionEndpoint = $outputs.functionEndpoint.value
    $storageAccountName = $outputs.storageAccountName.value
    $fileShareName = $outputs.fileShareName.value
    $keyVaultName = $outputs.keyVaultName.value

    Write-Status "Function App: $functionAppName" "Info"
    Write-Status "Endpoint: $functionEndpoint" "Info"
    Write-Status "Key Vault: $keyVaultName" "Info"

    # Step 5: Deploy agents from central library (if not done by ARM template)
    if (-not $SkipAgentUpload) {
        Write-Step "Deploying Agents from Central Library" 5

        Write-Status "Checking agent deployment status..." "Info"

        # Check if agents are already deployed by container instance
        $storageKey = az storage account keys list `
            --resource-group $ResourceGroupName `
            --account-name $storageAccountName `
            --query "[0].value" `
            --output tsv

        $agentFiles = az storage file list `
            --share-name $fileShareName `
            --path "agents" `
            --account-name $storageAccountName `
            --account-key $storageKey `
            --output json 2>$null | ConvertFrom-Json

        if ($agentFiles.Count -gt 0) {
            Write-Status "Agents already deployed by ARM template" "Success"
            Write-Status "Found $($agentFiles.Count) agent files" "Info"
        }
        else {
            Write-Status "Running manual agent deployment..." "Info"

            # Use the central deploy-agents.ps1 script
            $deployAgentsScript = Join-Path (Split-Path $PSScriptRoot -Parent) ".." "scripts" "deploy-agents.ps1"

            if (Test-Path $deployAgentsScript) {
                & $deployAgentsScript `
                    -ManifestPath "$manifestUrl" `
                    -ResourceGroup $ResourceGroupName `
                    -StorageAccount $storageAccountName
            }
            else {
                Write-Status "Deploy agents script not found, skipping manual deployment" "Warning"
            }
        }
    }

    # Step 6: Deploy function code
    Write-Step "Next Steps" 6

    Write-Host "`n📋 DEPLOYMENT SUMMARY" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

    Write-Host "`nResource Group:    " -NoNewline; Write-Host $ResourceGroupName -ForegroundColor Yellow
    Write-Host "Function App:      " -NoNewline; Write-Host $functionAppName -ForegroundColor Yellow
    Write-Host "Function Endpoint: " -NoNewline; Write-Host $functionEndpoint -ForegroundColor Yellow
    Write-Host "Storage Account:   " -NoNewline; Write-Host $storageAccountName -ForegroundColor Yellow
    Write-Host "Key Vault:         " -NoNewline; Write-Host $keyVaultName -ForegroundColor Yellow

    Write-Host "`n🚀 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Deploy your function code:"
    Write-Host "   cd templates/sales-voice-agent" -ForegroundColor Gray
    Write-Host "   func azure functionapp publish $functionAppName" -ForegroundColor Gray
    Write-Host "`n2. Test the endpoint:"
    Write-Host "   curl -X POST $functionEndpoint \" -ForegroundColor Gray
    Write-Host "     -H 'Content-Type: application/json' \" -ForegroundColor Gray
    Write-Host "     -d '{\"user_input\": \"Hello\", \"conversation_history\": []}'" -ForegroundColor Gray
    Write-Host "`n3. Configure Copilot Studio with the endpoint URL"
    Write-Host "`n4. Monitor logs in Application Insights"

    Write-Host "`n📚 AGENT INFORMATION:" -ForegroundColor Cyan
    Write-Host "Agents are deployed from the central library at:"
    Write-Host "https://github.com/$GitHubUsername/AI-AGENT-TEMPLATES/tree/main/agents" -ForegroundColor Gray
    Write-Host "`nManifest URL:"
    Write-Host $manifestUrl -ForegroundColor Gray

    Write-Host "`n✅ DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green

    # Clean up temp files
    Remove-Item $parametersFile -Force -ErrorAction SilentlyContinue

    # Optionally open Azure Portal
    $openPortal = Read-Host "`nOpen Azure Portal to view resources? (Y/N)"
    if ($openPortal -eq 'Y') {
        $portalUrl = "https://portal.azure.com/#resource/subscriptions/$($account.id)/resourceGroups/$ResourceGroupName/overview"
        Start-Process $portalUrl
    }
}
catch {
    Write-Status "Deployment failed: $_" "Error"
    Write-Status "Error details: $($_.Exception.Message)" "Error"

    # Clean up on failure
    if (Test-Path $parametersFile) {
        Remove-Item $parametersFile -Force -ErrorAction SilentlyContinue
    }

    exit 1
}
