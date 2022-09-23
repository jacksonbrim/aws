import json
import os

import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    # request
    print('request: {}'.format(json.dumps(event)))

    # update dynamodb table
    table.update_item(
        Key={'path': event['path']},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1}
    )

    # invoke lambda
    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'],
        Payload=json.dumps(event),
    )

    body = resp['Payload'].read()
    
    print(f"hitcount.py:\n\nbody: {body}")

    # invoked lambda response
    print('downstream.response: {}'.format(body))
    return json.loads(body)
