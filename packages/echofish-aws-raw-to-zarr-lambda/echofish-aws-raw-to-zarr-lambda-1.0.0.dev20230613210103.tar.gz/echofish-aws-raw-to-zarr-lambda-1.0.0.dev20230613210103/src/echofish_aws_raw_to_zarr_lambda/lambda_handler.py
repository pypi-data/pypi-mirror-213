import os
import json
from .lambda_executor import LambdaExecutor
from .s3_operations import S3Operations
from .dynamo_operations import DynamoOperations

input_bucket=os.environ['INPUT_BUCKET']
output_bucket=os.environ['OUTPUT_BUCKET']
table_name=os.environ['TABLE_NAME']
output_bucket_access_key=os.environ['OUTPUT_BUCKET_ACCESS_KEY']
output_bucket_secret_access_key=os.environ['OUTPUT_BUCKET_SECRET_ACCESS_KEY']

executor = LambdaExecutor(S3Operations(), DynamoOperations(), input_bucket, output_bucket, table_name, output_bucket_access_key, output_bucket_secret_access_key)

def handler(sqs_event, context):
    print("Event : " + str(sqs_event))
    print("Context : " + str(context))
    for record in sqs_event['Records']:
        message = json.loads(record['body'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sqs_event))

