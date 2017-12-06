import requests
import json
import base64
import os
import shutil
#%%
uaaUrl = "https://d25dd486-88f2-4504-b3bf-f38cdc2a64cf.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token"
client_id="inbox"
client_secret="Inbox123"

token = str(base64.b64encode(b'inbox:Inbox123'))


headers = {
        'authorization': "Basic " + token,
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request('POST', uaaUrl, data="grant_type=client_credentials", headers=headers)
print(json.loads(response.text))
token = json.loads(response.text)['access_token']

#%%
#create a catalog entry
analytics_catalog = "https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics"
analytics_zone_id = "78d00131-2c29-43f3-8618-10e675fecf9c"
headers = {
        'predix-zone-id': "78d00131-2c29-43f3-8618-10e675fecf9c",
        'authorization': "Bearer " + token,
        'content-type': "application/json"
    }
body={
  "name": "demo-adder-py",
  "version": "v1",
  "supportedLanguage": "Python",
  "taxonomyLocation": "",
  "author": "Adeel",
  "description": "This analytic does simple math",
  "customMetadata": "{\"assetid\":\"abc\"}"
}
response = requests.request('POST', analytics_catalog, data=json.dumps(body), headers=headers)
print(json.loads(response.text))
analytic_id=json.loads(response.text)['id']

#%%
analytics_uploadurl="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/artifacts"
headers ={
        'predix-zone-id': "78d00131-2c29-43f3-8618-10e675fecf9c",
        'authorization': "Bearer " + token,
#        'content-type': "multipart/form-data"
    }
path="D:\predix\predix-analytics-sample\\analytics\demo-adder"
dir_name="demo-adder-py"
output_filename="demo-adder-py"
shutil.make_archive(os.path.join(path,output_filename), 'zip', os.path.join(path,dir_name))
with open(os.path.join(path,output_filename+".zip"), 'rb') as f:
    body={
      "file": f,
      "catalogEntryId": analytic_id,
      "type": "Executable",
      "description": "This analytic does simple math"
      }
    response = requests.request('POST', analytics_uploadurl, files=body, headers=headers)
print(json.loads(response.text))

#%%
#validate analytic
analytics_validate="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics/" + analytic_id + "/validation"
headers ={
        'predix-zone-id': "78d00131-2c29-43f3-8618-10e675fecf9c",
        'authorization': "Bearer " + token
    }

body={
  "number1": 700,
  "number2": 800
}

response = requests.request('POST', analytics_validate, data=json.dumps(body), headers=headers)
print(json.loads(response.text))
validationRequestId=json.loads(response.text)['validationRequestId']
#%%
validation_resulturl="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics/"+analytic_id+"/validation/"+validationRequestId
headers ={
        'predix-zone-id': "78d00131-2c29-43f3-8618-10e675fecf9c",
        'authorization': "Bearer " + token
    }
response=requests.request('GET',validation_resulturl,headers=headers)
print(json.loads(response.text))