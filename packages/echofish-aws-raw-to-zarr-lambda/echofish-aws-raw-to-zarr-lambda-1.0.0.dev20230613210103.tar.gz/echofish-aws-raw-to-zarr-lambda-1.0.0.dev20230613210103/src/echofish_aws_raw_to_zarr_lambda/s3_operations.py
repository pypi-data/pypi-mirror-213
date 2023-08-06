import boto3

class S3Operations:


    def __get_client(self, access_key=None, secret_access_key=None):
        client = None
        if access_key:
            client = boto3.Session().client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_access_key
            )
        else:
            client = boto3.Session().client('s3')
        return client

    def list_objects(self, bucket_name, prefix, access_key=None, secret_access_key=None):
        keys = []
        for page in self.__get_client(access_key, secret_access_key).get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=prefix):
            contents = page["Contents"]
            for obj in contents:
                keys.append(obj["Key"])
        return keys

    def download_file(self, bucket_name, key, file_name, access_key=None, secret_access_key=None):
        self.__get_client(access_key, secret_access_key).download_file(bucket_name, key, file_name)

    def delete(self, bucket_name, key, access_key=None, secret_access_key=None):
        self.__get_client(access_key, secret_access_key).delete_object(
            Bucket=bucket_name,
            Key=key,
        )

    def upload_file(self, file_name, bucket_name, key, access_key=None, secret_access_key=None):
        self.__get_client(access_key, secret_access_key).upload_file(file_name, bucket_name, key)
