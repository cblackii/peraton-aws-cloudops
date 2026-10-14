# AWS CloudOps FinOps Assessment

## Project
Peraton AWS CloudOps Lab

## Objective
Investigate AWS infrastructure costs, identify resource-level
cost drivers, and evaluate optimization opportunities without
disrupting existing workloads.

## Reporting Period
September 14, 2026 - October 14, 2026

## AWS Cost Summary

Total Unblended Cost: $4.11

| Service | Cost |
|---|---:|
| EC2 - Other | $2.17 |
| AWS Key Management Service | $1.93 |
| Amazon S3 | <$0.01 |
| Total | $4.11 |

## Finding 1: EBS Storage Costs

Cost Explorer identified EBS gp3 storage as the primary
EC2-Other expense.

Two EBS volumes were identified:

- 20 GB gp3 volume
- 8 GB gp3 volume

Both volumes are attached to stopped t3.micro instances.

### Assessment

Stopping EC2 instances does not eliminate EBS storage charges.

### Recommendation

Review whether the stopped instances and their associated
volumes are still required.

Do not delete volumes without verifying data retention
requirements and recovery dependencies.

## Finding 2: Customer-Managed KMS Keys

AWS Cost Explorer identified approximately $1.93 in KMS costs.

Investigation identified two customer-managed keys:

1. Auto-Scaling Web Tier Terraform state encryption
2. Legacy luitweek21 Terraform backend encryption

### Auto-Scaling Web Tier

The Terraform state file was confirmed to use SSE-KMS
with the project's customer-managed key.

Recommendation: Retain this key.

### Legacy Terraform Backend

The legacy S3 bucket is empty.

S3 versioning is enabled, but no historical object
versions or delete markers were returned.

The associated KMS key remains enabled.

Recommendation: Investigate dependencies and historical
usage before considering retirement.

No KMS keys were disabled or scheduled for deletion.

## Finding 3: Cost Attribution

Existing AWS resources should use consistent tags:

- Project
- Environment
- Owner
- CostCenter

Tags improve ownership tracking and can support cost
allocation when activated as AWS cost allocation tags.

## Optimization Opportunities

| Opportunity | Action | Risk |
|---|---|---|
| EBS storage | Review stopped-instance volumes | Medium |
| Legacy KMS key | Investigate retirement eligibility | High |
| Resource tagging | Standardize cost allocation tags | Low |
| Cost monitoring | Review Cost Explorer regularly | Low |

## Operational Outcome

Demonstrated the ability to:

- Analyze AWS spending using Cost Explorer
- Retrieve cost data using Python and Boto3
- Investigate EC2, EBS, KMS, and S3 dependencies
- Identify potential infrastructure waste
- Evaluate optimization risks
- Preserve critical Terraform state encryption

## Change Management

This assessment was performed using read-only AWS APIs.

No production resources were modified, disabled,
or deleted during the investigation.