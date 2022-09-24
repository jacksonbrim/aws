from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)
from cdk_workshop.pipeline_stage import WorkshopPipelineStage

class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository( # AWS Repository to create Code Pipeline from
            self, 'WorkshopRepo',
            repository_name="WorkshopRepo"
        )

        pipeline = pipelines.CodePipeline( # Create a pipeline using the CodePipelineEngine
            self,
            "Pipeline",
            synth=pipelines.ShellStep( # synth is the build step that produces the CDK Cloud Assembly
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk", #Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt", # Instructs Codebuild to install required packages
                    "npx cdk synth",
                    ]
            ),
        )

        deploy = WorkshopPipelineStage(self, "Deploy") # Create Pipeline Stage
        deploy_stage = pipeline.add_stage(deploy) # Add stage to pipeline
        deploy_stage.add_post( # Add step to run after all of the stacks in the stage
            pipelines.ShellStep( # Add shell command
                "TestViewerEndpoint",
                env_from_cfn_outputs={
                    "ENDPOINT_URL": deploy.hc_viewer_url 
                },
                commands=["curl -Ssf $ENDPOINT_URL"], # The shell command to run
            )
        )
        deploy_stage.add_post( # add step to pipeline for after after stacks run
            pipelines.ShellStep( # Create shell command step
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={
                    "ENDPOINT_URL": deploy.hc_endpoint
                },
                commands=[ # Shell commands - urls to test against the api endpoint
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello",
                    "curl -Ssf $ENDPOINT_URL/test",
                    "curl -Ssf $ENDPOINT_URL/din/widdie/dub/buckets",
                ],
            )
        )
