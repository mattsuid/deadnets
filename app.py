#!/usr/bin/env python3

from aws_cdk import core

from deadnets.deadnets_stack import DeadnetsStack


app = core.App()
DeadnetsStack(app, "deadnets")

app.synth()
