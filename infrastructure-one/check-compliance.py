#!/usr/bin/env python3
"""
SOC2 Compliance Check Script

This script simulates what a policy pack would flag in our infrastructure.
It analyzes the Pulumi program to identify SOC2 compliance violations.
"""

import re
import json
from typing import List, Dict, Any

class ComplianceViolation:
    def __init__(self, resource_name: str, resource_type: str, violation: str, soc2_control: str):
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.violation = violation
        self.soc2_control = soc2_control

def analyze_pulumi_code(file_path: str) -> List[ComplianceViolation]:
    """Analyze the Pulumi code for SOC2 compliance violations"""
    violations = []

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for unencrypted S3 buckets
        if 'server_side_encryption_configuration=None' in content:
            violations.append(ComplianceViolation(
                resource_name="demo-bucket",
                resource_type="aws:s3/bucket:Bucket",
                violation="S3 bucket does not have server-side encryption enabled",
                soc2_control="CC6.1 - Logical and Physical Access Controls"
            ))

        # Check for BucketObject resources without encryption
        bucket_objects = re.findall(r's3\.BucketObject\(\s*[\'"]([^\'\"]*)[\'"]', content)
        for obj_name in bucket_objects:
            violations.append(ComplianceViolation(
                resource_name=obj_name,
                resource_type="aws:s3/bucketObject:BucketObject",
                violation="S3 object stored in unencrypted bucket",
                soc2_control="CC6.1 - Logical and Physical Access Controls"
            ))

    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
        return []

    return violations

def print_compliance_report(violations: List[ComplianceViolation]):
    """Print a formatted compliance report"""
    if not violations:
        print("✅ No SOC2 compliance violations found!")
        return

    print(f"🚨 Found {len(violations)} SOC2 Compliance Violations:\n")

    for i, violation in enumerate(violations, 1):
        print(f"{i}. Resource: {violation.resource_name}")
        print(f"   Type: {violation.resource_type}")
        print(f"   Violation: {violation.violation}")
        print(f"   SOC2 Control: {violation.soc2_control}")
        print()

    print("Recommendation:")
    print("- Enable server-side encryption for all S3 buckets")
    print("- Use KMS keys for encryption management")
    print("- Ensure all data at rest is encrypted per SOC2 requirements")

def main():
    print("SOC2 Compliance Check")
    print("=" * 40)

    violations = analyze_pulumi_code("__main__.py")
    print_compliance_report(violations)

    print("\nTo fix these violations:")
    print("1. Remove 'server_side_encryption_configuration=None' from S3 bucket")
    print("2. Add proper encryption configuration")
    print("3. Run 'pulumi preview' to validate changes")

if __name__ == "__main__":
    main()