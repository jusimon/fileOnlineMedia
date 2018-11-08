import os
import boto3
import json


s3 = boto3.resource('s3')
obj = s3.Object("elasticbeanstalk-us-west-1-687611171333","config.json")
ret = obj.get()
fdata =  (((ret)['Body']).read()).decode('utf-8')
jdata = json.loads(fdata)
LOCAL_FILE = "/home/julian/.google/config.json"


def getAwskey_id():
    return jdata['key_id']

def getAwsAccess_key():
    return jdata['access_key'] 

def getAwsBucket():
    return jdata['bucket']


def getAwsRdsHost():
    return jdata['rds_host']

def getAwsUsername():
    return jdata['username']


def getAwsPassword():
    return jdata['password']


def getAwsDbName():
    return jdata['db_name']

def getGoogleClientId():
    if (os.path.isfile(LOCAL_FILE)):
        ljson_data=open(LOCAL_FILE).read() 
        ljdata = json.loads(ljson_data) 
        return ljdata['g_client_id']
    return jdata['g_client_id']

def getGoogleAccess():
    if (os.path.isfile(LOCAL_FILE)):
        ljson_data=open(LOCAL_FILE).read() 
        ljdata = json.loads(ljson_data) 
        return ljdata['g_secret_id']
    return jdata['g_secret_id']
