#!/usr/bin/env python3

from aws_cdk import core
from deadnets.deadnets_stack import DeadnetsStack
import os

ENV = core.Environment(
    account=os.environ.get('CDK_DEFAULT_ACCOUNT'),
    region=os.environ.get('CDK_DEFAULT_REGION')
)


app = core.App()
DeadnetsStack(app, 'deadnets', env=ENV)

app.synth()
