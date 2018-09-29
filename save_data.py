import json
import boto3
import os
from pathlib import Path

S3_BUCKET = "title-influence-visual"
AWS_PROFILE = ""

def save_locally(key, data): 
    return _save_locally('data/', key, data)

# Saves the file; returns False if this works 
def _save_locally(path, key, data): 
    base_filename = path + str(key) 
    filename = base_filename
    data_file = Path(filename + '.json')
    counter = 1
    while data_file.exists(): 
        # we are about to overwrite a file... 
        filename = base_filename + '_' + str(counter) + '.json'
        data_file = Path(filename)
        counter+=1
    with data_file.open('w') as f: 
        json.dump(data, f)
    return filename

def save_s3(key, data): 
    #session = boto3.session.Session(profile_name="personal-heroku")
    s3 = boto3.resource('s3')
    bytestring = json.dumps(data).encode()
    r = s3.Object(S3_BUCKET, key).put(Body=bytestring, ContentType='application/json')
    print(r)
    return
