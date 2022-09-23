#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.pipeline_stack import WorkShopPipelineStack

app = cdk.App()
WorkShopPipelineStack(app, "WorkShopPipelineStack")

app.synth()
