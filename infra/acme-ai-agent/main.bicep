targetScope = 'resourceGroup'

@description('Public network access for the AI Services accounts and search services.')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccess string = 'Enabled'

// --- Regions -----------------------------------------------------------------

@description('Region for the Sweden Central resources.')
param swedenLocation string = 'swedencentral'

@description('Region for the Australia East resources.')
param australiaLocation string = 'australiaeast'

@description('Region for the East US 2 resources.')
param usLocation string = 'eastus2'

// --- Resource names ----------------------------------------------------------

@description('Name of the first Sweden Central search service.')
param searchSwedenPrimaryName string = 'acme-birdai'

@description('Name of the second Sweden Central search service.')
param searchSwedenSecondaryName string = 'acme-bird-ai-srch'

@description('Name of the Sweden Central storage account.')
param storageSwedenName string = 'acmebird'

@description('Name of the Australia East search service used by the agent.')
param searchAgentName string = 'acme-bird-agent'

@description('Name of the Australia East storage account.')
param storageAustraliaName string = 'acmebirddataau'

@description('Name of the Australia East AI Services account.')
param aiAustraliaName string = 'acme-bird-ai'

@description('Name of the Australia East Foundry project.')
param projectAustraliaName string = 'acme-bird-agent'

@description('Name of the East US 2 AI Services account.')
param aiUsName string = 'acme-bird-us-resource'

@description('Name of the East US 2 Foundry project.')
param projectUsName string = 'acme-bird-us'

@description('Name of the Cognitive Search connection on the Australia East account.')
@minLength(3)
@maxLength(32)
param searchConnectionAustraliaName string = 'acmebirdagent15jhr0'

@description('Name of the Cognitive Search connection on the East US 2 account.')
@minLength(3)
@maxLength(32)
param searchConnectionUsName string = 'acmebirdagentd37uin'

// --- SKUs --------------------------------------------------------------------

type searchSkuName = 'free' | 'basic' | 'standard' | 'standard2' | 'standard3' | 'storage_optimized_l1' | 'storage_optimized_l2'

@description('SKU for the Sweden Central search services.')
param searchSwedenSku searchSkuName = 'basic'

@description('SKU for the Australia East (agent) search service.')
param searchAgentSku searchSkuName = 'standard'

type storageSkuName = 'Standard_LRS' | 'Standard_GRS' | 'Standard_RAGRS' | 'Standard_ZRS' | 'Premium_LRS'

@description('SKU for both storage accounts.')
param storageSku storageSkuName = 'Standard_LRS'

// --- Shared building blocks --------------------------------------------------

var searchBaseProperties = {
  replicaCount: 1
  partitionCount: 1
  hostingMode: 'Default'
  semanticSearch: 'free'
  disableLocalAuth: true
  publicNetworkAccess: publicNetworkAccess
}

var storageBaseProperties = {
  accessTier: 'Hot'
  minimumTlsVersion: 'TLS1_2'
  supportsHttpsTrafficOnly: true
  allowBlobPublicAccess: false
  networkAcls: {
    bypass: 'AzureServices'
    defaultAction: 'Allow'
  }
}

// --- Sweden Central ----------------------------------------------------------

resource searchSwedenPrimary 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchSwedenPrimaryName
  location: swedenLocation
  sku: {
    name: searchSwedenSku
  }
  properties: searchBaseProperties
}

resource searchSwedenSecondary 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchSwedenSecondaryName
  location: swedenLocation
  sku: {
    name: searchSwedenSku
  }
  properties: searchBaseProperties
}

resource storageSweden 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageSwedenName
  location: swedenLocation
  kind: 'StorageV2'
  sku: {
    name: storageSku
  }
  properties: storageBaseProperties
}

// --- Australia East ----------------------------------------------------------

resource searchAgent 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchAgentName
  location: australiaLocation
  sku: {
    name: searchAgentSku
  }
  properties: searchBaseProperties
}

resource storageAustralia 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageAustraliaName
  location: australiaLocation
  kind: 'StorageV2'
  sku: {
    name: storageSku
  }
  properties: storageBaseProperties
}

resource aiAustralia 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiAustraliaName
  location: australiaLocation
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: aiAustraliaName
    publicNetworkAccess: publicNetworkAccess
    allowProjectManagement: true
  }
}

resource projectAustralia 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  name: projectAustraliaName
  parent: aiAustralia
  location: australiaLocation
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: projectAustraliaName
    description: 'Default project created with the resource'
  }
}

resource grokFastDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  name: 'grok-4-1-fast-reasoning'
  parent: aiAustralia
  sku: {
    name: 'GlobalStandard'
    capacity: 50
  }
  properties: {
    model: {
      format: 'xAI'
      name: 'grok-4-1-fast-reasoning'
      version: '1'
    }
  }
}

resource searchConnectionAustralia 'Microsoft.CognitiveServices/accounts/connections@2025-06-01' = {
  name: searchConnectionAustraliaName
  parent: aiAustralia
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${searchAgent.name}.search.windows.net/'
    authType: 'AAD'
    isSharedToAll: true
  }
}

// --- East US 2 ---------------------------------------------------------------

resource aiUs 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiUsName
  location: usLocation
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: aiUsName
    publicNetworkAccess: publicNetworkAccess
    allowProjectManagement: true
    disableLocalAuth: false
  }
}

resource projectUs 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  name: projectUsName
  parent: aiUs
  location: usLocation
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  name: 'text-embedding-3-small'
  parent: aiUs
  sku: {
    name: 'GlobalStandard'
    capacity: 250
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-3-small'
      version: '1'
    }
  }
}

resource grokReasoningDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  name: 'grok-4-20-reasoning'
  parent: aiUs
  sku: {
    name: 'GlobalStandard'
    capacity: 50
  }
  properties: {
    model: {
      format: 'xAI'
      name: 'grok-4-20-reasoning'
      version: '1'
    }
  }
  // Deployments on the same account must be created sequentially.
  dependsOn: [
    embeddingDeployment
  ]
}

resource searchConnectionUs 'Microsoft.CognitiveServices/accounts/connections@2025-06-01' = {
  name: searchConnectionUsName
  parent: aiUs
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${searchAgent.name}.search.windows.net/'
    authType: 'AAD'
    isSharedToAll: true
  }
}

// --- Outputs -----------------------------------------------------------------

output searchSwedenPrimaryId string = searchSwedenPrimary.id
output searchSwedenSecondaryId string = searchSwedenSecondary.id
output searchAgentId string = searchAgent.id
output storageSwedenId string = storageSweden.id
output storageAustraliaId string = storageAustralia.id
output aiAustraliaId string = aiAustralia.id
output aiAustraliaEndpoint string = aiAustralia.properties.endpoint
output projectAustraliaId string = projectAustralia.id
output aiUsId string = aiUs.id
output aiUsEndpoint string = aiUs.properties.endpoint
output projectUsId string = projectUs.id
