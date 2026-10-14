# AWS CloudOps Engineering Lab

### CloudFormation | AWS Lambda | IAM | CloudWatch | Python | Boto3 | FinOps

A hands-on AWS Cloud Operations engineering project demonstrating
infrastructure automation, operational monitoring, incident response,
and cloud cost optimization.

## Project Overview

This project simulates operational responsibilities commonly performed
by AWS Cloud Engineers supporting production cloud environments.

The lab demonstrates:

- Infrastructure provisioning using AWS CloudFormation
- Least-privilege IAM execution roles
- Serverless application deployment using AWS Lambda
- Centralized application logging with Amazon CloudWatch
- Automated operational health reporting using Python and Boto3
- CloudWatch alarm configuration and incident detection
- Controlled application failure simulation and recovery
- AWS cost analysis using Cost Explorer
- FinOps investigation of EBS storage and AWS KMS

## Architecture

```text
                 AWS CloudFormation
                         |
                         v
               Infrastructure Stack
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      IAM Role       AWS Lambda     CloudWatch
          |              |              |
          |              +--------------+
          |                     |
          |                     v
          |               Application Logs
          |                     |
          |                     v
          |               Error Monitoring
          |                     |
          |                     v
          |               CloudWatch Alarm
          |
          +---- Least-Privilege Permissions


             Python / Boto3 Automation
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Health Reporting        FinOps Reporting
             |                       |
             v                       v
        AWS Lambda              Cost Explorer
        CloudWatch              EC2 / EBS
        Logs / Alarms           KMS / S3
```

## Technology Stack

| Category | Technology |
|---|---|
| Cloud Provider | Amazon Web Services |
| Infrastructure as Code | AWS CloudFormation |
| Serverless Compute | AWS Lambda |
| Programming | Python 3.12 |
| AWS SDK | Boto3 |
| Identity and Access | AWS IAM |
| Monitoring | Amazon CloudWatch |
| Cost Management | AWS Cost Explorer |
| Encryption | AWS KMS |
| Storage | Amazon EBS and Amazon S3 |
| Version Control | Git and GitHub |

## Repository Structure

```text
peraton-aws-cloudops/
├── cloudformation/
│   └── infrastructure.yaml
├── lambda/
│   └── app.py
├── scripts/
│   ├── cloudops_health.py
│   └── cloudops_cost.py
├── monitoring/
├── tests/
├── evidence/
│   └── finops-assessment.md
├── .gitignore
└── README.md
```

## Infrastructure Deployment

Infrastructure is deployed using AWS CloudFormation.

The stack provisions:

- CloudWatch log group with a seven-day retention policy
- IAM execution role for AWS Lambda
- Python-based Lambda function
- CloudWatch alarm monitoring Lambda execution errors

CloudFormation change sets are used to review infrastructure
changes before deployment.

### Validate Template

```bash
aws cloudformation validate-template \
  --template-body file://cloudformation/infrastructure.yaml \
  --region us-west-2
```

### Review Infrastructure

```bash
aws cloudformation describe-stack-resources \
  --stack-name peraton-cloudops-dev \
  --region us-west-2
```

## Application Monitoring

The Lambda application supports two operational scenarios.

### Healthy Execution

```json
{}
```

Expected application response:

```json
{
  "status": "healthy",
  "message": "Peraton AWS CloudOps Lambda operational"
}
```

### Failure Simulation

```json
{
  "simulate_failure": true
}
```

The failure scenario deliberately raises a Python RuntimeError.

CloudWatch captures:

- Application invocation logs
- Error messages
- Python stack traces
- Lambda execution metrics

A CloudWatch alarm monitors the Lambda Errors metric.

## Incident Response Validation

The project includes a controlled failure-and-recovery exercise.

### Incident Workflow

1. Invoke the Lambda function with a simulated failure.
2. Confirm the Lambda invocation reports an execution error.
3. Inspect CloudWatch application logs.
4. Identify the Python exception and stack trace.
5. Verify the CloudWatch error alarm transitions to ALARM.
6. Invoke the Lambda function with a healthy payload.
7. Verify the application responds successfully.
8. Confirm the alarm returns to OK after its evaluation period.

This demonstrates application troubleshooting and operational
recovery validation.

## Python Operational Automation

### CloudOps Health Report

```bash
python scripts/cloudops_health.py
```

The report retrieves:

- Lambda runtime and configuration
- Lambda operational status
- CloudWatch invocation metrics
- CloudWatch error metrics
- CloudWatch alarm state
- CloudWatch log group configuration

### FinOps Cost Report

```bash
python scripts/cloudops_cost.py
```

The FinOps report retrieves AWS service-level spending
using the Cost Explorer API.

It generates:

- Reporting period
- AWS service cost breakdown
- Total AWS spending

AWS Cost Explorer data is queried using Boto3.

## FinOps Investigation

A cost investigation was conducted to identify infrastructure
spending and potential optimization opportunities.

### Cost Summary

Reporting period: September 14 – October 14, 2026.

| Service | Cost |
|---|---:|
| EC2 - Other | $2.17 |
| AWS Key Management Service | $1.93 |
| Amazon S3 | <$0.01 |
| Total | $4.11 |

### EBS Investigation

Two gp3 EBS volumes were identified:

- 20 GB attached to a stopped EC2 instance
- 8 GB attached to a stopped EC2 instance

The investigation confirmed that EBS storage charges continue
even when EC2 instances are stopped.

### KMS Investigation

Two customer-managed KMS keys were investigated.

The first key protects Terraform state for an existing
Auto-Scaling Web Tier project.

The second key is associated with a legacy Terraform
backend whose S3 bucket is currently empty.

The legacy key was flagged for dependency review before
any retirement decision.

No infrastructure resources were deleted or disabled.

### Detailed Assessment

See [FinOps Assessment](evidence/finops-assessment.md).

## Security Considerations

Security practices demonstrated include:

- IAM execution roles
- Least-privilege access principles
- CloudWatch operational logging
- AWS KMS encryption investigation
- Infrastructure change review
- Controlled failure simulation
- Resource dependency verification before optimization

## Engineering Outcomes

This project demonstrates the ability to:

1. Provision and update AWS infrastructure using CloudFormation.
2. Develop Python-based operational automation with Boto3.
3. Configure CloudWatch logging, metrics, and alarms.
4. Investigate application failures using centralized logs.
5. Validate application recovery after simulated incidents.
6. Analyze AWS costs and identify potential optimization opportunities.
7. Evaluate infrastructure dependencies before recommending changes.

## Future Enhancements

- GitLab CI/CD pipeline
- Automated CloudFormation validation
- Unit testing for Python automation
- CloudWatch dashboard
- Cost allocation tagging and reporting
- Additional operational runbooks
- Automated infrastructure teardown

## Author

**Charles Black II**

Cloud Security | Cloud Engineering | DevSecOps

GitHub: https://github.com/cblackii
