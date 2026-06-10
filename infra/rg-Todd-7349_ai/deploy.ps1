[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SubscriptionId,

    [Parameter(Mandatory = $false)]
    [string]$ResourceGroupName = 'rg-Todd-7349_ai',

    [Parameter(Mandatory = $false)]
    [string]$Location = 'eastus2',

    [Parameter(Mandatory = $false)]
    [string]$TemplateFile = (Join-Path $PSScriptRoot 'main.bicep'),

    [Parameter(Mandatory = $false)]
    [string]$ParametersFile = (Join-Path $PSScriptRoot 'main.bicepparam'),

    [Parameter(Mandatory = $false)]
    [string]$DeploymentName = ("rg-Todd-7349_ai-{0}" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
)

$ErrorActionPreference = 'Stop'

Write-Host "Starting deployment: $DeploymentName" -ForegroundColor Cyan

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw 'Azure CLI (az) is not installed or not available in PATH.'
}

if ($SubscriptionId) {
    Write-Host "Setting active subscription to: $SubscriptionId" -ForegroundColor Yellow
    az account set --subscription $SubscriptionId | Out-Null
}

Write-Host "Ensuring resource group exists: $ResourceGroupName ($Location)" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location | Out-Null

$parametersArgument = if ([System.IO.Path]::GetExtension($ParametersFile) -ieq '.bicepparam') {
    $ParametersFile
}
else {
    "@$ParametersFile"
}

$deploymentArgs = @(
    'deployment', 'group', 'create',
    '--name', $DeploymentName,
    '--resource-group', $ResourceGroupName,
    '--template-file', $TemplateFile,
    '--parameters', $parametersArgument
)

Write-Host 'Running az deployment group create...' -ForegroundColor Yellow
$deploymentResult = az @deploymentArgs | ConvertFrom-Json

Write-Host 'Deployment completed successfully.' -ForegroundColor Green
Write-Host ("Storage Account ID: {0}" -f $deploymentResult.properties.outputs.storageAccountId.value)
Write-Host ("Key Vault ID:       {0}" -f $deploymentResult.properties.outputs.keyVaultId.value)
Write-Host ("Key Vault URI:      {0}" -f $deploymentResult.properties.outputs.keyVaultUri.value)
Write-Host ("AI Services ID:     {0}" -f $deploymentResult.properties.outputs.aiServicesId.value)
Write-Host ("AI Services URL:    {0}" -f $deploymentResult.properties.outputs.aiServicesEndpoint.value)
Write-Host ("Hub Workspace ID:   {0}" -f $deploymentResult.properties.outputs.hubWorkspaceId.value)
