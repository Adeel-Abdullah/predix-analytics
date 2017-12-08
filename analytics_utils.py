# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 16:25:15 2017

@author: Adeel Abdullah
"""
import requests
import json
import shutil
import os

def client_login(uaaUrl, client_id_secret):
    headers = {
            'authorization': "Basic " + client_id_secret,
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
    response = requests.request('POST', uaaUrl, data="grant_type=client_credentials", headers=headers)
    print(json.loads(response.text))
    return json.loads(response.text)['access_token']

def create_catalog_entry(analytics_catalogUrl, analytics_zone_id, token):
    headers = {
            'predix-zone-id': analytics_zone_id,
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
    response = requests.request('POST', analytics_catalogUrl, data=json.dumps(body), headers=headers)
    print(json.loads(response.text))
    return json.loads(response.text)['id']

def create_zip(path,dir_name,output_zipfile):
    shutil.make_archive(os.path.join(path,output_zipfile), 'zip', os.path.join(path,dir_name))
    
def upload_analytic(token, path, filename, analytic_id, analytics_zone_id):
    analytics_uploadurl="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/artifacts"
    headers ={
            'predix-zone-id': analytics_zone_id,
            'authorization': "Bearer " + token
        }    
    with open(os.path.join(path,filename+".zip"), 'rb') as f:
        body={
          "file": f,
          "catalogEntryId": analytic_id,
          "type": "Executable",
          "description": "This analytic does simple math"
          }
        response = requests.request('POST', analytics_uploadurl, files=body, headers=headers)
    return json.loads(response.text)

def validate_analytic(token, analytic_id, analytics_zone_id, body):
    analytics_validate="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics/" + analytic_id + "/validation"
    headers ={
            'predix-zone-id': analytics_zone_id,
            'authorization': "Bearer " + token
        }
    response = requests.request('POST', analytics_validate, data=body, headers=headers)
    validationRequestId=json.loads(response.text)['validationRequestId']
    return validationRequestId

def check_result(token, validationRequestId, analytic_id):
    validation_resulturl="https://predix-analytics-catalog-release.run.aws-usw02-pr.ice.predix.io/api/v1/catalog/analytics/"+analytic_id+"/validation/"+validationRequestId
    headers ={
            'predix-zone-id': "78d00131-2c29-43f3-8618-10e675fecf9c",
            'authorization': "Bearer " + token
        }
    response=requests.request('GET',validation_resulturl,headers=headers)
    return json.loads(response.text)