"""An AWS Python Pulumi program for SOC2 compliance demo"""

import pulumi
from pulumi_aws import s3

# Create an unencrypted S3 bucket (intentionally non-compliant for demo)
bucket = s3.Bucket('demo-bucket',
    bucket='neo-examples-demo-bucket',
    # Explicitly disable encryption to trigger SOC2 policy violations
    server_side_encryption_configuration=None
)

# Create a sample file to upload
sample_file = s3.BucketObject('sample-file',
    bucket=bucket.id,
    key='demo-data.txt',
    content='This is sample data that should be encrypted but is not.',
    content_type='text/plain'
)

# Create another object to demonstrate multiple files
config_file = s3.BucketObject('config-file',
    bucket=bucket.id,
    key='config/app-config.json',
    content='{"database": "prod-db", "api_key": "secret-key-123"}',
    content_type='application/json'
)

# Export bucket information
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
pulumi.export('sample_file_url', pulumi.Output.concat('s3://', bucket.id, '/', sample_file.key))
pulumi.export('region', 'ca-central-1')
