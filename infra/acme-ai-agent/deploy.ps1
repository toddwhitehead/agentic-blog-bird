[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SubscriptionId,

    [Parameter(Mandatory = $false)]
    [string]$ResourceGroupName = 'acme-ai-agent',

    [Parameter(Mandatory = $false)]
    [string]$Location = 'australiaeast',

    [Parameter(Mandatory = $false)]
    [string]$TemplateFile = (Join-Path $PSScriptRoot 'main.bicep'),

    [Parameter(Mandatory = $false)]
    [string]$ParametersFile = (Join-Path $PSScriptRoot 'main.bicepparam'),

    [Parameter(Mandatory = $false)]
    [string]$DeploymentName = ("acme-ai-agent-{0}" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
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
Write-Host ("AU AI Services ID:   {0}" -f $deploymentResult.properties.outputs.aiAustraliaId.value)
Write-Host ("AU AI Endpoint:      {0}" -f $deploymentResult.properties.outputs.aiAustraliaEndpoint.value)
Write-Host ("AU Project ID:       {0}" -f $deploymentResult.properties.outputs.projectAustraliaId.value)
Write-Host ("US AI Services ID:   {0}" -f $deploymentResult.properties.outputs.aiUsId.value)
Write-Host ("US AI Endpoint:      {0}" -f $deploymentResult.properties.outputs.aiUsEndpoint.value)
Write-Host ("US Project ID:       {0}" -f $deploymentResult.properties.outputs.projectUsId.value)
Write-Host ("Agent Search ID:     {0}" -f $deploymentResult.properties.outputs.searchAgentId.value)
