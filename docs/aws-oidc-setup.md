# AWS OIDC Setup for Pulumi Cloud

This document describes how to configure AWS OIDC (OpenID Connect) authentication for Pulumi Cloud deployments in the `adamgordonbell-org` organization.

## Overview

OIDC allows Pulumi Cloud to authenticate with AWS without storing long-term credentials. Instead, it uses short-lived tokens that are exchanged for AWS credentials during deployment.

## Architecture

```
Pulumi Cloud → OIDC Token → AWS STS → Temporary Credentials → AWS Services
```

## Setup Process

### 1. AWS IAM OIDC Provider Configuration

The OIDC provider `api.pulumi.com/oidc` already existed but needed to include our organization's audience.

**Add organization audience to OIDC provider:**
```bash
aws iam add-client-id-to-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::616138583583:oidc-provider/api.pulumi.com/oidc \
  --client-id aws:adamgordonbell-org
```

**Verify it was added:**
```bash
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::616138583583:oidc-provider/api.pulumi.com/oidc \
  --query 'ClientIDList' | grep adamgordonbell
```

### 2. IAM Role Configuration

We use the shared `pulumi-environments-oidc` role that multiple organizations use.

**Role ARN:** `arn:aws:iam::616138583583:role/pulumi-environments-oidc`

**Trust Policy:** The role was updated to include our organization in the audience list:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::616138583583:oidc-provider/api.pulumi.com/oidc"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "api.pulumi.com/oidc:aud": [
            "pulumi", "aws:pulumi",
            "upstarts", "aws:upstarts",
            "diana-pulumi-corp", "aws:initech-co",
            "adamgordonbell-org", "aws:adamgordonbell-org"
          ]
        }
      }
    }
  ]
}
```

**Permissions:** The role has `AdministratorAccess` policy attached for full AWS access.

### 3. Pulumi ESC Environment

**Environment Path:** `adamgordonbell-org/oidc/oidc`

**Configuration:**
```yaml
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          duration: 1h
          roleArn: arn:aws:iam::616138583583:role/pulumi-environments-oidc
          sessionName: pulumi-deploy
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

### 4. Pulumi Stack Configuration

**Stack Config File:** `Pulumi.CA-prod.yaml`
```yaml
config:
  aws:region: ca-central-1
environment:
  - oidc/oidc
```

## Key Components

### OIDC Token Flow
1. **Subject:** `pulumi:environments:org:adamgordonbell-org:env:oidc/oidc`
2. **Audience:** `aws:adamgordonbell-org`
3. **Provider:** `https://api.pulumi.com/oidc`

### Critical Configuration Points
- **OIDC Provider ClientIDList** must include `aws:adamgordonbell-org`
- **IAM Role Trust Policy** must accept the audience `aws:adamgordonbell-org`
- **ESC Environment** must reference the correct role ARN
- **Stack Configuration** must link to the ESC environment as `oidc/oidc`

## Troubleshooting

### Common Error: "Incorrect token audience"
This error occurs when the audience in the OIDC token doesn't match what's configured.

**Root Cause:** The OIDC provider's `ClientIDList` doesn't include your organization's audience.

**Solution:** Add your audience to the OIDC provider (Step 1 above).

### Authentication Flow
1. Pulumi Cloud generates OIDC token with audience `aws:adamgordonbell-org`
2. AWS STS validates the token against the OIDC provider's `ClientIDList`
3. If valid, STS checks the IAM role's trust policy
4. If trust policy allows the audience/subject, temporary credentials are issued
5. ESC environment variables are populated with these credentials

## Security Notes

- **Short-lived tokens:** Credentials expire after 1 hour (configurable)
- **Least privilege:** Consider creating organization-specific roles with minimal required permissions instead of using `AdministratorAccess`
- **Audit trail:** All AWS actions are logged with the role session name `pulumi-deploy`

## References

- [Pulumi ESC AWS OIDC Documentation](https://www.pulumi.com/docs/esc/providers/aws-oidc/)
- [AWS IAM OIDC Provider Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)