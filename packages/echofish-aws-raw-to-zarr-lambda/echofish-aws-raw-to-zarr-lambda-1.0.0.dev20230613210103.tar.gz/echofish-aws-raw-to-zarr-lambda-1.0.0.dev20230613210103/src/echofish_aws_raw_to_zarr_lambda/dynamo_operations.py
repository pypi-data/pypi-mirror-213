import boto3

class DynamoOperations:

    def get_item(self, table_name, key):
        response = boto3.Session().client('dynamodb').get_item(TableName=table_name, Key=key)
        item = None
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Item' in response:
                item = response['Item']
        return item

    def put_item(self, table_name, item):
        response = boto3.Session().client('dynamodb').put_item(TableName=table_name, Item=item)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        assert(status_code == 200), "Unable to update dynamodb table"

    def update_item(self, table_name, key, attribute_names, attribute_values, expression):
        response = boto3.Session().client('dynamodb').update_item(ExpressionAttributeNames=attribute_names, ExpressionAttributeValues=attribute_values, Key=key, TableName=table_name, UpdateExpression=expression)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        assert(status_code == 200), "Unable to update dynamodb table"

