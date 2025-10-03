# Pulumi Neo Examples Repository

## Project Goals

This repository demonstrates the capabilities of **Pulumi Neo**, an infrastructure coding agent, through real-world infrastructure challenges. Each branch represents a distinct example scenario where Neo addresses a specific infrastructure problem or task.

## Ground Rules for Infrastructure Changes

When working with this project, follow these rules:

1. **All infrastructure changes MUST use Pulumi CLI** (`pulumi up`, `pulumi destroy`, etc.) - never modify infrastructure directly
2. **AWS CLI is for exploration only** - use it to inspect resources, but never to create, modify, or delete infrastructure
3. **Region lock: ca-central-1 only** - all infrastructure must remain in Canada Central region
4. **Stay in scope** - only touch infrastructure defined in this Pulumi program; never modify resources outside this project
5. **Debugging with Pulumi** - if you need to recreate infrastructure for debugging, use `pulumi destroy` followed by `pulumi up`

## How It Works

1. **Branch Structure**: Each branch contains infrastructure code with a specific problem or challenge
2. **Neo Integration**: Pulumi Neo receives a prompt describing the infrastructure task to address
3. **Automated Deployment**: GitHub Actions workflow handles validation and deployment:
   - PRs trigger `pulumi preview` to show proposed changes
   - Merges to `main` trigger `pulumi up` to apply changes
4. **Demonstration**: This workflow showcases Neo's ability to work with real infrastructure tasks in a safe, automated manner

## Example Branches

### `neo-one-encrypt-ebs`
**Challenge**: Unencrypted EBS volume
**Task**: Enable encryption on an existing EBS volume

### `neo-two-k8s-resize`
**Challenge**: Kubernetes capacity issues
**Task**: Resize Kubernetes cluster by adding a new node group

### `neo-three-unused-resources`
**Challenge**: Cost optimization - unused infrastructure
**Task**: Identify and remove unused resources:
- Application Load Balancer with no target groups/listeners
- Security group not referenced by any resource
- Unattached EBS volume orphaned from deleted workload
- Note: Cluster has active nginx deployment to demonstrate it's in use

## GitHub Actions Workflow

The repository uses a single workflow (`.github/workflows/infrastructure-preview.yml`) that:

- **On Pull Request**: Runs `pulumi preview` and comments the proposed changes on the PR
- **On Merge to Main**: Runs `pulumi up` to deploy infrastructure changes
- **Manual Trigger**: Supports workflow_dispatch for manual deployments

This ensures all infrastructure changes are reviewed before deployment, demonstrating safe IaC practices with AI agents.

## Stack Configuration

- **Stack**: `adamgordonbell-org/CA-prod`
- **Region**: `ca-central-1`
- **Provider**: AWS (EKS cluster with API authentication)

## Why This Matters

This repository serves as a portfolio of Pulumi Neo's capabilities:
- Solving security issues (encryption)
- Scaling infrastructure (node groups)
- Optimizing costs (removing unused resources)
- Working within standard DevOps workflows (GitOps, PR reviews, automated deployments)

Each example demonstrates Neo's ability to understand infrastructure context, make appropriate changes, and integrate with existing CI/CD pipelines.
