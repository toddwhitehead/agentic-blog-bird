using './main.bicep'

// Base name used to derive all resource names. Override per environment.
param workloadName = 'aihub'

// Defaults to the resource group's location when omitted.
// param location = 'eastus2'

param storageSkuName = 'Standard_LRS'
param publicNetworkAccess = 'Enabled'

// Resource names default to generated, unique values derived from workloadName
// and a hash of the resource group id. Uncomment to pin specific names.
// param storageAccountName = '<storage-account-name>'
// param keyVaultName = '<key-vault-name>'
// param aiServicesName = '<ai-services-name>'
// param hubWorkspaceName = '<hub-workspace-name>'
// param hubFriendlyName = '<hub-display-name>'

// Defaults to the deploying subscription's tenant. Override only if the
// Key Vault must live in a different tenant.
// param tenantId = '<tenant-guid>'
