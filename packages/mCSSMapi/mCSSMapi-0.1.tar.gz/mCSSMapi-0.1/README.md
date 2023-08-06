# mCSSMAPI - Mini Cisco Smart Software Manager API
The mcssmapi library is providing access to Cisco Smart Account licensing API with python.

I needed to access licensing portal to get SLR licensing process a little bit easier.
I was inspired to create API by great app https://developer.cisco.com/codeexchange/github/repo/CiscoDevNet/smart-license-app/.

## Version
(TODO)
- more API calls
- logging

0.1 (21.6.2021)
- initial release with only slr reserve call

## Prerequisite

For use the module you need to have:
- CCO/Cisco.com Account
- Valid Smart Account (SA) and Virtual Account in CSSM
- IOS-XE devices with Smart Licensing enalbed image version (>16.10.1)
- Generated API access (Client ID and Client Secret)

## Installation

```
$ pip install mcssmapi
```
### API access
For accessing CSSM API you will need to request for API access on https://apidocs-prod.cisco.com/

How to request API access is described here: https://anypoint.mulesoft.com/apiplatform/apx#/portals/organizations/1c92147b-332d-4f44-8c0e-ad3997b5e06d/apis/5418104/versions/102456/pages/425744


## Usage

All code is only an example. Values are not valid.

```
import mcssmapi
import json

CLIENT_ID = "abcd1234"
CLIENT_SECRET = "secret1234"
SAD = "sadomain.com"
VA = "Test Account"
REQUEST_CODE = "CE-ZC9300-48P-4X:XDC240312LB5-A6rZG7jGd-75"

# init api instance
api = mcssmapi.Licensing(CLIENT_ID, CLIENT_SECRET)
# get oauth token
api.bearer_update()

# license definition

licenses = [
       {
           "quantity" : 1,
           "entitlementTag" : "regid.2018-05.com.cisco.C9300-DNA-E-48,1.0_e213fd3f-18f9-4940-a21c-617b92efdaae"
       },
       {
           "quantity" : 1,
           "entitlementTag" : "regid.2018-05.com.cisco.C9300-NW-E-48,1.0_52d2a0bd-de8a-480f-b70b-1d57e7738aec"
       },
   ]
result = api.reserve_license(SAD,VA,REQUEST_CODE, licenses)

print(json.dumps(result, indent=2)

```
## License

App is released under the MIT License. See LICENSE for details.

## Contact

Github: 
