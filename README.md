# AWS EKS Cluster with API Authentication

A Pulumi template for provisioning an EKS Kubernetes cluster using API authentication mode.

## Overview

This template provisions an EKS cluster with:
- API authentication mode (no aws-auth ConfigMap required)
- Single node group for system workloads
- Disabled CoreDNS addon for faster provisioning
- OIDC provider for IRSA (IAM Roles for Service Accounts)

## Prerequisites

- An AWS account with permissions to create EKS clusters
- AWS credentials configured via Pulumi ESC environment (`oidc/oidc`)
- Python 3.6 or later installed
- Pulumi CLI already installed and logged in
- `kubectl` installed for cluster access
- Optional: `k9s` for interactive cluster management

## Getting Started

1. Deploy the stack:
   ```bash
   pulumi up
   ```

2. The cluster will take approximately 10-15 minutes to provision.

3. Once complete, you can access the cluster using kubectl or k9s.

## Configuration

Stack configuration values:

- `aws:region` - The AWS region to deploy into (default: `us-west-2`)
- Stack environment: `oidc/oidc` - Provides AWS credentials via OIDC

View configuration with:
```bash
pulumi config
```

## Accessing the Cluster

### Using kubectl

The cluster uses API authentication mode, which requires AWS credentials with proper access entries. The cluster creator role (`pulumi-environments-oidc`) has admin access by default.

**Option 1: Run kubectl through ESC environment**
```bash
pulumi env run oidc/oidc -- kubectl get nodes
pulumi env run oidc/oidc -- kubectl get pods -A
```

**Option 2: Start a shell with ESC credentials**
```bash
pulumi env run oidc/oidc -- zsh
# Now run kubectl commands directly:
kubectl get nodes
kubectl get pods -A
```

**Option 3: Export kubeconfig and use ESC shell**
```bash
pulumi stack output kubeconfig --show-secrets > kubeconfig.yaml
pulumi env run oidc/oidc -- zsh
export KUBECONFIG=$(pwd)/kubeconfig.yaml
kubectl get nodes
```

### Using k9s

K9s provides an interactive terminal UI for managing Kubernetes clusters:

```bash
# Run k9s through ESC environment
pulumi env run oidc/oidc -- k9s

# Or from within an ESC shell
pulumi env run oidc/oidc -- zsh
k9s
```

## Outputs

Once deployed, the stack exports:

- `cluster_name` — the name of the EKS cluster
- `kubeconfig` — the kubeconfig for accessing the cluster
- `region` — the AWS region where the cluster is deployed

Retrieve outputs with:
```bash
pulumi stack output cluster_name
pulumi stack output kubeconfig --show-secrets
```

## Architecture

The cluster is provisioned with:
- **Authentication Mode**: API (uses EKS access entries, not aws-auth ConfigMap)
- **Node Group**: Single auto-scaling group (1-2 t3.small instances)
- **Networking**: Default VPC configuration managed by Pulumi EKS component
- **Add-ons**: VPC CNI, kube-proxy (CoreDNS disabled for faster provisioning)

## Key Configuration Choices

### API Authentication Mode
This cluster uses `authentication_mode: eks.AuthenticationMode.API` which:
- Eliminates the need for the aws-auth ConfigMap
- Uses EKS access entries for authorization
- Simplifies cluster bootstrapping
- Follows the pattern recommended in Pulumi workshops

### ESC Environment
The stack uses a Pulumi ESC environment (`oidc/oidc`) which:
- Provides AWS credentials via OIDC
- Grants the cluster creator admin access automatically
- Ensures consistent credentials between Pulumi and kubectl

## Troubleshooting

**"Error: You must be logged in to the server"**
- This means you're not using the ESC environment credentials
- Solution: Use `pulumi env run oidc/oidc -- kubectl ...`

**Cluster creation hangs or times out**
- EKS clusters typically take 10-15 minutes to provision
- Check CloudWatch logs and AWS Console for details

## Cleanup

Destroy all resources:
```bash
pulumi destroy
```

## Next Steps

- Add additional node groups with different instance types
- Configure cluster autoscaling
- Install add-ons (ingress controllers, monitoring, etc.)
- Deploy applications using Pulumi's Kubernetes provider

## Help and Community

- Pulumi Documentation: https://www.pulumi.com/docs/
- EKS Package: https://www.pulumi.com/registry/packages/eks/
- Community Slack: https://slack.pulumi.com/
- GitHub Issues: https://github.com/pulumi/pulumi/issues
