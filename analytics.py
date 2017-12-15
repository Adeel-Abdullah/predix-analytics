import base64
import time

import analytics_utils as au

uaaUrl = "https://d25dd486-88f2-4504-b3bf-f38cdc2a64cf.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token"
client_id = "inbox"
client_secret = "Inbox123"

client_id_secret = str(base64.b64encode(b'inbox:Inbox123'))

token = au.client_login(uaaUrl, client_id_secret)

#create a catalog entry
analytics_catalogUrl = "https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics"
analytics_zone_id = "78d00131-2c29-43f3-8618-10e675fecf9c"
body = {
    "name": "demo-adder-py",
    "version": "v1",
    "supportedLanguage": "Python",
    "taxonomyLocation": "",
    "author": "Adeel",
    "description": "This analytic does simple math",
    "customMetadata": "{\"assetid\":\"abc\"}"
    }

analytic_id = au.create_catalog_entry(analytics_catalogUrl,analytics_zone_id,token, body)

#upload analytic
path = "D:\\predix\\predix-analytics-sample\\analytics\\demo-adder"
dir_name = "demo-adder-py"
output_filename = "demo-adder-py"

au.create_zip(path, dir_name, output_filename)

print(au.upload_analytic(token, path, output_filename, analytic_id, analytics_zone_id))

#validate analytic
input_json = {
    "number1": 700,
    "number2": 800
    }

validationRequestId = au.validate_analytic(token, analytic_id, analytics_zone_id, input_json)
print(validationRequestId)

response = au.check_result(token, validationRequestId, analytic_id)

while response['status'] != "COMPLETED":
    response = au.check_result(token, validationRequestId, analytic_id)
    print(response['status'])
    time.sleep(60)
