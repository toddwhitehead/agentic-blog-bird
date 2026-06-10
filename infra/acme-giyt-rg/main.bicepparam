using './main.bicep'

param location = 'westus2'
param staticSiteName = 'getinyourtree'
param staticSiteSkuName = 'Free'
param dnsZoneName = 'getinyourtree.com'

// Keep false by default to avoid requiring a repository token at deploy time.
param enableGitHubIntegration = false

param repositoryUrl = 'https://github.com/toddwhitehead/acme-giyt-web'
param repositoryBranch = 'main'
param repositoryProvider = 'GitHub'

param apexTxtValidationValue = '_xvv07w8gokicjvuhmn1c9a2rlmpaiff'
param apexAliasTtl = 3600
param wwwCnameTtl = 3600
param apexTxtTtl = 3600
