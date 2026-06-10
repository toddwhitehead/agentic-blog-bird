using './main.bicep'

param publicNetworkAccess = 'Enabled'

param swedenLocation = 'swedencentral'
param australiaLocation = 'australiaeast'
param usLocation = 'eastus2'

param searchSwedenPrimaryName = 'acme-birdai'
param searchSwedenSecondaryName = 'acme-bird-ai-srch'
param storageSwedenName = 'acmebird'

param searchAgentName = 'acme-bird-agent'
param storageAustraliaName = 'acmebirddataau'
param aiAustraliaName = 'acme-bird-ai'
param projectAustraliaName = 'acme-bird-agent'

param aiUsName = 'acme-bird-us-resource'
param projectUsName = 'acme-bird-us'

param searchConnectionAustraliaName = 'acmebirdagent15jhr0'
param searchConnectionUsName = 'acmebirdagentd37uin'

param searchSwedenSku = 'basic'
param searchAgentSku = 'standard'
param storageSku = 'Standard_LRS'
