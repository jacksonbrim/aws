from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
)

def WorkshopPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository(
            self, 'WorkshopRepo',
            repository_name="WorkshopRepo"
        )

        # Pipeline code will go here

