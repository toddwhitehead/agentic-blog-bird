targetScope = 'resourceGroup'

@description('Base name used to derive resource names.')
@minLength(2)
@maxLength(8)
param workloadName string = 'aihub'

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Unique suffix used to keep globally-scoped resource names unique.')
param uniqueSuffix string = uniqueString(resourceGroup().id)

@description('Name of the Storage account backing the AI Foundry hub.')
param storageAccountName string = take(toLower('st${workloadName}${uniqueSuffix}'), 24)

@description('Name of the Key Vault backing the AI Foundry hub.')
param keyVaultName string = take(toLower('kv-${workloadName}-${uniqueSuffix}'), 24)

@description('Name of the Azure AI Services (Cognitive Services) account.')
param aiServicesName string = toLower('ai-${workloadName}-${uniqueSuffix}')

@description('Name of the Azure Machine Learning hub workspace.')
param hubWorkspaceName string = '${workloadName}-hub'

@description('Friendly (display) name for the hub workspace.')
param hubFriendlyName string = '${workloadName} hub'

@description('Tenant ID used for the Key Vault.')
param tenantId string = subscription().tenantId

type StorageSkuName = 'Standard_LRS' | 'Standard_GRS' | 'Standard_RAGRS' | 'Standard_ZRS' | 'Premium_LRS'

@description('SKU for the Storage account.')
param storageSkuName StorageSkuName = 'Standard_LRS'

@description('Public network access for the AI Services account and hub workspace.')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccess string = 'Enabled'

resource storageAccount 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: storageSkuName
  }
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    allowCrossTenantReplication: false
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2025-05-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableSoftDelete: true
    enableRbacAuthorization: false
    enabledForDeployment: false
    publicNetworkAccess: 'Enabled'
    accessPolicies: []
  }
}

resource aiServices 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiServicesName
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: aiServicesName
    publicNetworkAccess: publicNetworkAccess
  }
}

resource hubWorkspace 'Microsoft.MachineLearningServices/workspaces@2025-09-01' = {
  name: hubWorkspaceName
  location: location
  kind: 'Hub'
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: hubFriendlyName
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    hbiWorkspace: false
    publicNetworkAccess: publicNetworkAccess
  }
}

resource hubKeyVaultAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2025-05-01' = {
  name: 'add'
  parent: keyVault
  properties: {
    accessPolicies: [
      {
        tenantId: hubWorkspace.identity.tenantId
        objectId: hubWorkspace.identity.principalId
        permissions: {
          certificates: [
            'all'
          ]
          keys: [
            'all'
          ]
          secrets: [
            'all'
          ]
          storage: []
        }
      }
    ]
  }
}

output storageAccountId string = storageAccount.id
output keyVaultId string = keyVault.id
output keyVaultUri string = keyVault.properties.vaultUri
output aiServicesId string = aiServices.id
output aiServicesEndpoint string = aiServices.properties.endpoint
output hubWorkspaceId string = hubWorkspace.id
output hubWorkspacePrincipalId string = hubWorkspace.identity.principalId
