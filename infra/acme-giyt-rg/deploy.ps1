[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SubscriptionId,

    [Parameter(Mandatory = $false)]
    [string]$ResourceGroupName = 'acme-giyt-rg',

    [Parameter(Mandatory = $false)]
    [string]$Location = 'westus2',

    [Parameter(Mandatory = $false)]
    [string]$TemplateFile = (Join-Path $PSScriptRoot 'main.bicep'),

    [Parameter(Mandatory = $false)]
    [string]$ParametersFile = (Join-Path $PSScriptRoot 'main.bicepparam'),

    [Parameter(Mandatory = $false)]
    [string]$DeploymentName = ("acme-giyt-rg-{0}" -f (Get-Date -Format 'yyyyMMdd-HHmmss')),

    [Parameter(Mandatory = $false)]
    [switch]$EnableGitHubIntegration,

    [Parameter(Mandatory = $false)]
    [string]$RepositoryToken
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

if ($EnableGitHubIntegration.IsPresent) {
    if ([string]::IsNullOrWhiteSpace($RepositoryToken)) {
        throw 'RepositoryToken is required when -EnableGitHubIntegration is specified.'
    }

    $deploymentArgs += @(
        '--parameters',
        'enableGitHubIntegration=true',
        'repositoryToken={0}' -f $RepositoryToken
    )
}

Write-Host 'Running az deployment group create...' -ForegroundColor Yellow
$deploymentResult = az @deploymentArgs | ConvertFrom-Json

Write-Host 'Deployment completed successfully.' -ForegroundColor Green
Write-Host ("Static Web App ID: {0}" -f $deploymentResult.properties.outputs.staticWebAppId.value)
Write-Host ("Static Web App Hostname: {0}" -f $deploymentResult.properties.outputs.staticWebAppDefaultHostname.value)
Write-Host ("DNS Zone ID: {0}" -f $deploymentResult.properties.outputs.dnsZoneId.value)
Write-Host ("Domain: {0}" -f $deploymentResult.properties.outputs.deployedRootDomain.value)
Write-Host ("WWW Domain: {0}" -f $deploymentResult.properties.outputs.deployedWwwDomain.value)
