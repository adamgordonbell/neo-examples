# Neo Example 4: Security Policy Enforcement

## Objective
Demonstrate Pulumi Neo's ability to identify and fix policy violations related to overly permissive security group rules.

## Scenario
Security groups with SSH (port 22) or RDP (port 3389) open to the internet (0.0.0.0/0) represent a security risk and violate organizational compliance policies.

## Scope
**Current work**: Set up the scenario (steps 1-5) - create the problematic infrastructure and policies that will flag it.

**Neo's work** (not in scope for this setup): Fix the violations once the scenario is ready.

## Implementation Steps

### 1. Policy Pack Setup (TypeScript)
- Create `policies/` directory
- Initialize TypeScript policy pack with:
  - `package.json` - dependencies and metadata
  - `PulumiPolicy.yaml` - policy pack configuration
  - `index.ts` - policy implementation
- Policy checks:
  - Flag security groups with ingress rules allowing 0.0.0.0/0 on port 22 (SSH)
  - Flag security groups with ingress rules allowing 0.0.0.0/0 on port 3389 (RDP)
  - Set enforcement level to "mandatory"

### 2. Infrastructure Changes
Add to `__main__.py`:
- Security group with overly permissive SSH access (0.0.0.0/0:22)
- Could be for a bastion host or standalone
- Should be clearly fixable (restrict to specific CIDR or remove)

### 3. Local Testing
```bash
# Test policy locally
pulumi preview --policy-pack ./policies/

# Should see policy violation with clear message
```

### 4. Publish to Pulumi Cloud
```bash
# Publish policy pack
cd policies/
pulumi policy publish

# Enable for organization/stack via Pulumi Cloud UI or CLI
pulumi policy enable <org>/<policy-name> --policy-group=<stack>
```

### 5. Documentation Updates
- Update `CLAUDE.md` with neo-four-security-policies example
- Update main `README.md` if needed
- Create `docs/script.md` with scenario walkthrough

## Neo's Task
When given this branch, Neo should:
1. Run `pulumi preview` and encounter policy violations
2. Identify the problematic security group rules
3. Fix by either:
   - Restricting CIDR blocks to specific ranges
   - Removing unnecessary ingress rules
   - Replacing with more secure alternatives
4. Re-run preview to confirm policy compliance
5. Create PR with fixes

## Success Criteria
- Policy pack catches violations locally and in CI
- Policy violations have clear, actionable messages
- Neo can understand and fix the violations
- Fixed infrastructure passes policy checks
- Policy enforcement integrated into GitHub Actions workflow
