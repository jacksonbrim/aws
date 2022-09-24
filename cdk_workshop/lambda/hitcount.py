import json
import os

import boto3 # AWS Python SDK

ddb = boto3.resource('dynamodb')  
table = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    # request
    print('request: {}'.format(json.dumps(event)))

    
    table.update_item( # update dynamodb table
        Key={'path': event['path']},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1}
    )


    # Response of lambda function
    resp = _lambda.invoke( # boto3 api - invoke lambda function
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'], # Name of an external function to invoke
        Payload=json.dumps(event), # JSON input for the lambda function
    )

    body = resp['Payload'].read() # store reponse
    
    print(f"hitcount.py:\n\nbody: {body}")

    # invoked lambda response
    print('downstream.response: {}'.format(body))
    return json.loads(body)
