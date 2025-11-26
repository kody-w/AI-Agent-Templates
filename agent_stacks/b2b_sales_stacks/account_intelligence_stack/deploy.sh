#!/bin/bash

###############################################################################
# Azure Function Deployment Script for Account Intelligence Stack
# Deploys the Account Intelligence system to Azure Functions for Copilot Studio
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration (update these values)
RESOURCE_GROUP="${RESOURCE_GROUP:-account-intelligence-rg}"
LOCATION="${LOCATION:-westus2}"
FUNCTION_APP_NAME="${FUNCTION_APP_NAME:-account-intel-func-$(date +%s)}"
STORAGE_ACCOUNT="${STORAGE_ACCOUNT:-acctintelstorage$(date +%s | tail -c 8)}"
APP_INSIGHTS_NAME="${APP_INSIGHTS_NAME:-account-intel-insights}"
KEY_VAULT_NAME="${KEY_VAULT_NAME:-acct-intel-kv-$(date +%s | tail -c 8)}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Account Intelligence Stack Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Resource Group: ${YELLOW}$RESOURCE_GROUP${NC}"
echo -e "Location: ${YELLOW}$LOCATION${NC}"
echo -e "Function App: ${YELLOW}$FUNCTION_APP_NAME${NC}"
echo ""

# Step 1: Login to Azure
echo -e "${GREEN}[Step 1/8]${NC} Checking Azure login..."
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Not logged in. Please login to Azure...${NC}"
    az login
fi

# Get subscription info
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo -e "Using subscription: ${YELLOW}$SUBSCRIPTION_ID${NC}"
echo ""

# Step 2: Create Resource Group
echo -e "${GREEN}[Step 2/8]${NC} Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output none
echo -e "${GREEN}✓${NC} Resource group created"
echo ""

# Step 3: Create Storage Account
echo -e "${GREEN}[Step 3/8]${NC} Creating storage account..."
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS \
    --output none
echo -e "${GREEN}✓${NC} Storage account created"
echo ""

# Step 4: Create Application Insights
echo -e "${GREEN}[Step 4/8]${NC} Creating Application Insights..."
az monitor app-insights component create \
    --app $APP_INSIGHTS_NAME \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --output none
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
    --app $APP_INSIGHTS_NAME \
    --resource-group $RESOURCE_GROUP \
    --query instrumentationKey -o tsv)
echo -e "${GREEN}✓${NC} Application Insights created"
echo ""

# Step 5: Create Key Vault
echo -e "${GREEN}[Step 5/8]${NC} Creating Key Vault..."
az keyvault create \
    --name $KEY_VAULT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --output none
echo -e "${GREEN}✓${NC} Key Vault created"
echo ""

# Step 6: Create Function App
echo -e "${GREEN}[Step 6/8]${NC} Creating Function App..."
az functionapp create \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --storage-account $STORAGE_ACCOUNT \
    --consumption-plan-location $LOCATION \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --os-type Linux \
    --app-insights $APP_INSIGHTS_NAME \
    --output none
echo -e "${GREEN}✓${NC} Function App created"
echo ""

# Step 7: Configure Function App Settings
echo -e "${GREEN}[Step 7/8]${NC} Configuring environment variables..."
az functionapp config appsettings set \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        "FUNCTIONS_WORKER_RUNTIME=python" \
        "PYTHON_ENABLE_WORKER_EXTENSIONS=1" \
        "APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY" \
    --output none

echo -e "${YELLOW}⚠ Please configure these secrets in Azure Key Vault:${NC}"
echo -e "  - DYNAMICS_365_URL"
echo -e "  - AZURE_OPENAI_ENDPOINT"
echo -e "  - AZURE_OPENAI_KEY"
echo -e "  - GRAPH_API_CLIENT_ID"
echo -e "  - GRAPH_API_CLIENT_SECRET"
echo -e "  - AZURE_AI_SEARCH_ENDPOINT"
echo -e "  - AZURE_AI_SEARCH_KEY"
echo ""

# Step 8: Deploy Function Code
echo -e "${GREEN}[Step 8/8]${NC} Deploying function code..."
cd "$(dirname "$0")"

# Create deployment package
echo -e "Creating deployment package..."
zip -r deploy.zip . \
    -x "*.git*" \
    -x "*.DS_Store" \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x "deploy.sh" \
    -x "deploy.zip" \
    > /dev/null 2>&1

# Deploy to Azure
echo -e "Uploading to Azure..."
az functionapp deployment source config-zip \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --src deploy.zip \
    --output none

# Clean up
rm deploy.zip

echo -e "${GREEN}✓${NC} Function code deployed"
echo ""

# Get Function URL
FUNCTION_URL=$(az functionapp function show \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --function-name intelligence \
    --query invokeUrlTemplate -o tsv 2>/dev/null || echo "https://${FUNCTION_APP_NAME}.azurewebsites.net/api/intelligence")

# Get Function Key
FUNCTION_KEY=$(az functionapp keys list \
    --name $FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query functionKeys.default -o tsv)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Function Endpoint:${NC}"
echo -e "  $FUNCTION_URL"
echo ""
echo -e "${YELLOW}Function Key:${NC}"
echo -e "  $FUNCTION_KEY"
echo ""
echo -e "${YELLOW}Test with curl:${NC}"
echo -e 'curl -X POST "$FUNCTION_URL?code=$FUNCTION_KEY" \\'
echo -e '  -H "Content-Type: application/json" \\'
echo -e '  -d '"'"'{'
echo -e '    "operation": "account_briefing",'
echo -e '    "account_id": "CONTOSO001"'
echo -e '  }'"'"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. Configure secrets in Key Vault: https://portal.azure.com/#@/resource/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME"
echo -e "2. Update Function App settings to reference Key Vault secrets"
echo -e "3. Register this endpoint in Copilot Studio as a Plugin/Action"
echo -e "4. Test the integration from Microsoft Teams"
echo ""
echo -e "${GREEN}Documentation:${NC} See README_COPILOT_STUDIO_INTEGRATION.md"
echo ""
