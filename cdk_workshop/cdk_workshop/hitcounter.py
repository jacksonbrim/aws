from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy
)

class HitCounter(Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):    
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY # Removes the database when calling "cdk destroy"
        )

        self._handler = _lambda.Function( 
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hitcount.handler', # the method to be run when this function is called (lambda/hitcount.py)
            code=_lambda.Code.from_asset('lambda'), # source code for the lambda function
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            }
        )

        # Grants read write permissions toe the handler function
        self._table.grant_read_write_data(self.handler)

        """
        CloudWatch logs showed that HitCountHandler (aka self._handler) was not authorized to perform
        lambda:InvokeFunction on the lambda function
        need to grant invoke permissions to self._handler
        """
        # Grants invoke permissions to the _handler 
        downstream.grant_invoke(self._handler)

