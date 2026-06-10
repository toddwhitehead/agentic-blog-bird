targetScope = 'resourceGroup'

@description('Azure region for the Static Web App.')
param location string = 'westus2'

@description('Name of the Azure Static Web App.')
param staticSiteName string = 'getinyourtree'

@description('SKU for the Azure Static Web App (Free or Standard).')
@allowed([
  'Free'
  'Standard'
])
param staticSiteSkuName string = 'Free'

@description('DNS zone name.')
param dnsZoneName string = 'getinyourtree.com'

@description('Enable GitHub source control linkage on the Static Web App.')
param enableGitHubIntegration bool = false

@description('Repository URL used by the Static Web App when source control linkage is enabled.')
param repositoryUrl string = 'https://github.com/toddwhitehead/acme-giyt-web'

@description('Repository branch used by the Static Web App when source control linkage is enabled.')
param repositoryBranch string = 'main'

@description('Source control provider for the Static Web App when source control linkage is enabled.')
param repositoryProvider string = 'GitHub'

@secure()
@description('Repository access token used when source control linkage is enabled.')
param repositoryToken string = ''

@description('TXT record validation token for the zone apex.')
param apexTxtValidationValue string = '_xvv07w8gokicjvuhmn1c9a2rlmpaiff'

@description('TTL (seconds) for the apex A record alias.')
param apexAliasTtl int = 3600

@description('TTL (seconds) for the www CNAME record.')
param wwwCnameTtl int = 3600

@description('TTL (seconds) for the apex TXT validation record.')
param apexTxtTtl int = 3600

var staticSiteBaseProperties = {
  allowConfigFileUpdates: true
  stagingEnvironmentPolicy: 'Enabled'
}

var staticSiteSourceControlProperties = {
  provider: repositoryProvider
  repositoryUrl: repositoryUrl
  branch: repositoryBranch
  repositoryToken: repositoryToken
}

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticSiteName
  location: location
  sku: {
    name: staticSiteSkuName
    tier: staticSiteSkuName
  }
  properties: union(
    staticSiteBaseProperties,
    enableGitHubIntegration ? staticSiteSourceControlProperties : {}
  )
}

resource dnsZone 'Microsoft.Network/dnszones@2018-05-01' = {
  name: dnsZoneName
  location: 'global'
  properties: {
    zoneType: 'Public'
  }
}

resource apexARecord 'Microsoft.Network/dnszones/A@2018-05-01' = {
  name: '@'
  parent: dnsZone
  properties: {
    TTL: apexAliasTtl
    targetResource: {
      id: staticWebApp.id
    }
  }
}

resource apexTxtRecord 'Microsoft.Network/dnszones/TXT@2018-05-01' = {
  name: '@'
  parent: dnsZone
  properties: {
    TTL: apexTxtTtl
    TXTRecords: [
      {
        value: [
          apexTxtValidationValue
        ]
      }
    ]
  }
}

resource wwwCnameRecord 'Microsoft.Network/dnszones/CNAME@2018-05-01' = {
  name: 'www'
  parent: dnsZone
  properties: {
    TTL: wwwCnameTtl
    CNAMERecord: {
      cname: staticWebApp.properties.defaultHostname
    }
  }
}

output staticWebAppId string = staticWebApp.id
output staticWebAppDefaultHostname string = staticWebApp.properties.defaultHostname
output dnsZoneId string = dnsZone.id
output deployedRootDomain string = dnsZone.name
output deployedWwwDomain string = 'www.${dnsZone.name}'
