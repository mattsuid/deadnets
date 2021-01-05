from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
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
            bucket_name='deadnets.io',
            removal_policy=core.RemovalPolicy.DESTROY
        )

        origin_access_identity = cloudfront.OriginAccessIdentity(
            self,
            'origin_access_identity',
            comment='CloudFront read access'
        )

        web_bucket.grant_read(origin_access_identity)

        web_assets = s3_deployment.BucketDeployment(
            self,
            'web_assets',
            sources=[s3_deployment.Source.asset(str(Path('deadnets/resources').absolute()))],
            destination_bucket=web_bucket
        )

        dns_zone = route53.HostedZone.from_lookup(self, 'web_dns_zone', domain_name='deadnets.io')

        acm_certificate = acm.DnsValidatedCertificate(
            self,
            'web_certificate',
            hosted_zone=dns_zone,
            domain_name='deadnets.io',
            subject_alternative_names=['deadnets.io', 'www.deadnets.io']
        )

        cloudfront_distribution = cloudfront.CloudFrontWebDistribution(
            self,
            'web_cloudfront_distribution',
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=web_bucket,
                        origin_access_identity=origin_access_identity
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True
                        )
                    ],
                )
            ],
            error_configurations=[
                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=404,
                    response_page_path="/404.html"
                )
            ],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                certificate=acm_certificate,
                aliases=['deadnets.io']
            )
        )

        dns_record = route53.ARecord(
            self,
            'DNSAliasForCloudFront',
            zone=dns_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(cloudfront_distribution)
            ),
            record_name='deadnets.io',
        )