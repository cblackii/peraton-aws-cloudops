#!/usr/bin/env python3

"""
Peraton AWS CloudOps Lab
Operational Health Monitoring with Python/Boto3

Services:
- AWS Lambda
- Amazon CloudWatch
- Amazon CloudWatch Logs

Region: us-west-2
"""

import boto3
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError, BotoCoreError


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AWS_REGION = "us-west-2"

LAMBDA_FUNCTION = "peraton-cloudops-dev"

LOG_GROUP = "/aws/cloudops/peraton-lab"

ALARM_NAME = "peraton-cloudops-lambda-errors"


# --------------------------------------------------
# AWS Clients
# --------------------------------------------------

session = boto3.Session(region_name=AWS_REGION)

lambda_client = session.client("lambda")
cloudwatch_client = session.client("cloudwatch")
logs_client = session.client("logs")


# --------------------------------------------------
# Lambda Health
# --------------------------------------------------

def check_lambda():

    print("\n========== LAMBDA HEALTH ==========")

    response = lambda_client.get_function_configuration(
        FunctionName=LAMBDA_FUNCTION
    )

    print(f"Function: {response['FunctionName']}")
    print(f"Runtime: {response['Runtime']}")
    print(f"State: {response['State']}")
    print(f"Memory: {response['MemorySize']} MB")
    print(f"Timeout: {response['Timeout']} seconds")
    print(f"Last Modified: {response['LastModified']}")

    return response["State"]


# --------------------------------------------------
# CloudWatch Metrics
# --------------------------------------------------

def check_metrics():

    print("\n========== CLOUDWATCH METRICS ==========")

    end_time = datetime.now(timezone.utc)

    start_time = end_time - timedelta(hours=1)

    for metric_name in ["Invocations", "Errors"]:

        response = cloudwatch_client.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName=metric_name,
            Dimensions=[
                {
                    "Name": "FunctionName",
                    "Value": LAMBDA_FUNCTION
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Sum"]
        )

        datapoints = response.get("Datapoints", [])

        total = sum(point["Sum"] for point in datapoints)

        print(f"{metric_name}: {int(total)}")


# --------------------------------------------------
# CloudWatch Alarm
# --------------------------------------------------

def check_alarm():

    print("\n========== CLOUDWATCH ALARM ==========")

    response = cloudwatch_client.describe_alarms(
        AlarmNames=[ALARM_NAME]
    )

    alarms = response.get("MetricAlarms", [])

    if not alarms:
        print("Alarm not found")
        return "NOT_FOUND"

    alarm = alarms[0]

    print(f"Alarm: {alarm['AlarmName']}")
    print(f"State: {alarm['StateValue']}")
    print(f"Threshold: {alarm['Threshold']}")
    print(f"Metric: {alarm['MetricName']}")

    return alarm["StateValue"]


# --------------------------------------------------
# CloudWatch Logs
# --------------------------------------------------

def check_logs():

    print("\n========== CLOUDWATCH LOGS ==========")

    response = logs_client.describe_log_groups(
        logGroupNamePrefix=LOG_GROUP
    )

    log_groups = [
        group
        for group in response.get("logGroups", [])
        if group["logGroupName"] == LOG_GROUP
    ]

    if not log_groups:
        print("Log group not found")
        return

    log_group = log_groups[0]

    print(f"Log Group: {log_group['logGroupName']}")
    print(f"Retention: {log_group.get('retentionInDays', 'Never')} days")
    print(f"Stored Bytes: {log_group.get('storedBytes', 0)}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\n======================================")
    print("PERATON AWS CLOUDOPS HEALTH REPORT")
    print("======================================")

    print(f"Region: {AWS_REGION}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

    try:

        lambda_state = check_lambda()

        check_metrics()

        alarm_state = check_alarm()

        check_logs()

        print("\n========== HEALTH SUMMARY ==========")

        if lambda_state == "Active" and alarm_state == "OK":
            print("Overall Status: HEALTHY")
        else:
            print("Overall Status: ATTENTION REQUIRED")

    except (ClientError, BotoCoreError) as error:

        print(f"\nAWS API Error: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()