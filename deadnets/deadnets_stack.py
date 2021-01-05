from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_certificatemanager as acm
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

        dns_zone = route53.HostedZone.from_lookup(self, 'web_dns_zone', domain_name='deadnets.io')

        acm_certificate = acm.Certificate(
            self,
            'web_certificate',
            domain_name='deadnets.io',
            validation=acm.CertificateValidation.from_dns(dns_zone)
        )

        viewer_certificate = cloudfront.ViewerCertificate().from_acm_certificate(certificate=acm_certificate)

        cloudfront_distribution = cloudfront.CloudFrontWebDistribution(
            self,
            'web_cloudfront',
            origin_configs=[
                cloudfront.SourceConfiguration(
                    behaviors=[
                        cloudfront.Behavior()
                    ],
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=web_bucket
                    )
                )
            ],
            viewer_certificate=viewer_certificate
        )

        dns_record = route53.ARecord(
            self,
            'web_dns_record',
            zone=dns_zone,
            record_name='deadnets.io',
            target=route53.RecordTarget.from_alias(
                alias_target=route53.IAliasRecordTarget(cloudfront_distribution)
            )
        )