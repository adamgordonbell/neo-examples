"""Simple AWS infrastructure for compliance demo"""

import pulumi
from pulumi_aws import s3

# Create multiple S3 buckets for different purposes

# 1. Encrypted bucket for logs (compliant)
logs_bucket = s3.Bucket('logs-bucket',
    bucket='neo-logs-bucket-ca',
    server_side_encryption_configuration=s3.BucketServerSideEncryptionConfigurationArgs(
        rule=s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256"
            )
        )
    )
)

# 2. Encrypted bucket for backups (compliant)
backup_bucket = s3.Bucket('backup-bucket',
    bucket='neo-backup-bucket-ca',
    server_side_encryption_configuration=s3.BucketServerSideEncryptionConfigurationArgs(
        rule=s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256"
            )
        )
    )
)

# 3. Unencrypted bucket for temp data (non-compliant - intentional)
temp_bucket = s3.Bucket('temp-bucket',
    bucket='neo-temp-bucket-ca'
    # No encryption configuration - this will be flagged by SOC2 policies
)

# Create files in the encrypted buckets
log_file = s3.BucketObject('application-log',
    bucket=logs_bucket.id,
    key='logs/app.log',
    content='2024-09-25 10:00:00 INFO Application started successfully',
    content_type='text/plain'
)

backup_file = s3.BucketObject('database-backup',
    bucket=backup_bucket.id,
    key='backups/db-backup.sql',
    content='-- Database backup from 2024-09-25\nCREATE TABLE users (id INT, name VARCHAR(255));',
    content_type='text/plain'
)

# Create files in the unencrypted bucket (non-compliant)
temp_data = s3.BucketObject('temp-data',
    bucket=temp_bucket.id,
    key='temp/processing-data.json',
    content='{"user_data": {"email": "user@example.com", "api_key": "temp-key-123"}}',
    content_type='application/json'
)

config_file = s3.BucketObject('temp-config',
    bucket=temp_bucket.id,
    key='config/temp-settings.yaml',
    content='database:\n  host: prod-db.example.com\n  password: temp-password-456\napi_keys:\n  - service_a: key-789',
    content_type='text/yaml'
)

# Export bucket information
pulumi.export('logs_bucket_name', logs_bucket.id)
pulumi.export('backup_bucket_name', backup_bucket.id)
pulumi.export('temp_bucket_name', temp_bucket.id)
pulumi.export('logs_bucket_encrypted', True)
pulumi.export('backup_bucket_encrypted', True)
pulumi.export('temp_bucket_encrypted', False)
pulumi.export('region', 'ca-central-1')
