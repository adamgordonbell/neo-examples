# SOC2 Compliance Policy Pack

This policy pack enforces SOC2 compliance requirements for AWS resources.

## Policies Included

1. **s3-encryption-required**: Ensures all S3 buckets have server-side encryption enabled
2. **s3-object-encryption-required**: Ensures S3 objects use encryption

## Usage

```bash
pulumi preview --policy-pack policy-pack
```

## Violations Expected

When run against the infrastructure, this policy pack will flag:
- Unencrypted S3 bucket (SOC2 CC6.1 violation)
- Unencrypted S3 objects (SOC2 CC6.1 violation)

This demonstrates how policy packs can catch compliance violations during infrastructure deployment.