"""SOC2 compliance policy pack for AWS resources"""

from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ResourceValidationPolicy,
    ResourceValidationArgs,
)


def s3_encryption_required_validator(args: ResourceValidationArgs, report_violation):
    """Validates that S3 buckets have encryption enabled (SOC2 requirement)"""
    if args.resource_type == "aws:s3/bucket:Bucket":
        # Check if server side encryption is configured
        encryption_config = args.props.get("serverSideEncryptionConfiguration")

        if not encryption_config:
            report_violation(
                "SOC2 Violation: S3 buckets must have server-side encryption enabled. "
                "This is required for SOC2 CC6.1 (Logical and Physical Access Controls) compliance."
            )
        elif isinstance(encryption_config, dict) and not encryption_config.get("rules"):
            report_violation(
                "SOC2 Violation: S3 bucket encryption configuration is empty. "
                "Server-side encryption rules must be defined for SOC2 compliance."
            )


def s3_object_encryption_validator(args: ResourceValidationArgs, report_violation):
    """Validates that S3 bucket objects in unencrypted buckets are flagged"""
    if args.resource_type == "aws:s3/bucketObject:BucketObject":
        # This policy flags objects that might be in unencrypted buckets
        server_side_encryption = args.props.get("serverSideEncryption")

        if not server_side_encryption:
            report_violation(
                "SOC2 Violation: S3 objects should use server-side encryption. "
                "This ensures data at rest is encrypted per SOC2 CC6.1 requirements."
            )


PolicyPack(
    name="soc2-compliance",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        ResourceValidationPolicy(
            name="s3-encryption-required",
            description="S3 buckets must have server-side encryption enabled",
            validate=s3_encryption_required_validator,
        ),
        ResourceValidationPolicy(
            name="s3-object-encryption-required",
            description="S3 objects should use server-side encryption",
            validate=s3_object_encryption_validator,
        ),
    ],
)