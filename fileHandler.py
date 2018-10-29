import boto3
import aws
import os
import datetime
from clientDB import client



class filehandler:
    """ This class provided the user file handler routines """    
    def __init__(self):
        self.s3 = boto3.resource('s3',
                aws_access_key_id=aws.getAwskey_id(),
                aws_secret_access_key=aws.getAwsAccess_key())
        self.client = boto3.client('s3',
                aws_access_key_id=aws.getAwskey_id(),
                aws_secret_access_key=aws.getAwsAccess_key())
        self.bkt = aws.getAwsBucket()


    def get_path(self, username):
        c = client() 
        if 0 == c.is_admin_user(username):
            return username+"/"
        return ""
        

    def list_files(self, username):
        my_bucket = self.s3.Bucket(self.bkt)

        path = self.get_path(username)
        result = []

        for objects in my_bucket.objects.filter(Prefix=path):
            if path != "":
                if str.strip(objects.key, path) == '':
                    continue
            upd_time = str(objects.last_modified)
            mdata = objects.get()['Metadata']
            uname, fname = str.split(objects.key, "/")
            an_item = dict(username = uname, filename = fname,
                           upd_time = str.rstrip(upd_time,"+00:00"),
                           add_time = mdata['add_time'][:-7],
                           desc = mdata['desc'])
            result.append(an_item)
        return (result)


    def del_file(self, username, filename):
        self.client.delete_object(Bucket=self.bkt, Key=filename)

    def del_userfiles(self, username):
        my_bucket = self.s3.Bucket(self.bkt)

        path = self.get_path(username)
        result = []

        for objects in my_bucket.objects.filter(Prefix=path):
           objects.delete()
     

    def add_file(self, username, filename, filedesc, content):
        my_bucket = self.s3.Bucket(self.bkt)

        key = username+"/"+filename
        try:
            obj = my_bucket.Object(key)
            cur_time = obj.get()['Metadata']['add_time'] 
            print(cur_time)
        except:
            cur_time = str(datetime.datetime.utcnow())
        
        mdata = dict(desc = filedesc, add_time = cur_time)
        try:
            my_bucket.put_object(Key=key, Body=content, Metadata = mdata)
        except my_bucket.InternalError as error:
            code, message = error.args

        
    def get_object(self, username, filename):
        my_bucket = self.s3.Bucket(self.bkt)
        path = self.get_path(username)
        key = path+filename
        return self.client.get_object(Bucket=self.bkt, Key=key)['Body'].read()




##
##hdl  = filehandler()
##
##hdl.add_file('test', 'test2.txt','B File', 'MMMMMMMMMMMMMMMMMMMMMMMhihihihihih')
##rslt = hdl.list_files('test')
##for dist in rslt:
##        print (dist['filename'], dist['upd_time'], dist['add_time'], dist['desc'])
##
##rslt = hdl.del_file('test', 'test/test2.txt')
##print(rslt)
##rslt = hdl.list_files('test')
##for dist in rslt:
##        print (dist['filename'], dist['upd_time'], dist['add_time'], dist['desc'])
##


