from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route_53_targets
from pathlib import Path


class DeadnetsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_bucket = s3.Bucket(
            self,
            'web_bucket',
            versioned=False,
            public_read_access=True,
            bucket_name='deadnets.io',
            website_index_document='index.html',
            removal_policy=core.RemovalPolicy.DESTROY
        )

        web_assets = s3_deployment.BucketDeployment(
            self,
            'web_assets',
            sources=[s3_deployment.Source.asset(str(Path('deadnets/resources').absolute()))],
            destination_bucket=web_bucket
        )

        dns_record = route53.ARecord(
            self,
            'web_dns_record',
            zone=route53.HostedZone.from_lookup(self, 'web_dns_zone', domain_name='deadnets.io'),
            record_name='deadnets.io',
            target=route53.RecordTarget.from_alias(route_53_targets.BucketWebsiteTarget(web_bucket))
        )