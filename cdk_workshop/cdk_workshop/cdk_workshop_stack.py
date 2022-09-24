from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkWorkshopStack(Stack):

    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_lambda = _lambda.Function( 
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'), # Where the code for the lambda is stored
            handler='hello.handler', # The name of the method called by this function
        )

        hello_with_counter = HitCounter( # 
            self, 'HelloHitCounter',
            downstream=my_lambda 
        )

        gateway = apigw.LambdaRestApi( # Defines an API Gateway REST API with AWS Lambda proxy integration
            self, 'Endpoint',
            handler=hello_with_counter._handler # The handler that handles the requests from the API
        )

        tv = TableViewer( # Table used to view the DynamoDB data
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='-hits', # Sort the table in descending order
        )

        self._hc_endpoint = CfnOutput( # URL called to update database table
            self, 'GatewayUrl',
            value=gateway.url
        )

        self._hc_viewer_url = CfnOutput( # URL that serves the TableViewer
            self, 'TableViewerUrl',
            value=tv.endpoint
        )
