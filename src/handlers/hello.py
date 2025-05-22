import json
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context, table=None):
    if table is None:
        table = get_table()
    response = "Hello, world!"
    try:
        todo_id = str(uuid.uuid4())

        item = {
            'id': todo_id,
            'time': str(datetime.now()),
            'response': response
        }

        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': response})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Somthing went wrong!\n{e}'})
        }