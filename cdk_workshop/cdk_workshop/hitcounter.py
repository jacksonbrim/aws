from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
)

class HitCounter(Construct):

    def __init__(self, scope: Construct, id: str, downstream: _lamda.IFunction, **kwargs):    
        super().__init__(scope, id, **kwargs)

        # TODO
