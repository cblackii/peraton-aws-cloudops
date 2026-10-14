import boto3
from datetime import datetime, timedelta, timezone
from decimal import Decimal


# -----------------------------------------
# Configuration
# -----------------------------------------

PROJECT_NAME = "Peraton AWS CloudOps"
REPORT_DAYS = 30


# -----------------------------------------
# AWS Cost Explorer Client
# -----------------------------------------

ce = boto3.client("ce", region_name="us-east-1")


# -----------------------------------------
# Reporting Period
# -----------------------------------------

end_date = datetime.now(timezone.utc).date()
start_date = end_date - timedelta(days=REPORT_DAYS)


# -----------------------------------------
# Retrieve AWS Costs
# -----------------------------------------

response = ce.get_cost_and_usage(
    TimePeriod={
        "Start": start_date.isoformat(),
        "End": end_date.isoformat()
    },
    Granularity="MONTHLY",
    Metrics=["UnblendedCost"],
    GroupBy=[
        {
            "Type": "DIMENSION",
            "Key": "SERVICE"
        }
    ]
)


# -----------------------------------------
# Process Cost Data
# -----------------------------------------

service_costs = {}

for period in response["ResultsByTime"]:
    for group in period["Groups"]:

        service = group["Keys"][0]

        amount = Decimal(
            group["Metrics"]["UnblendedCost"]["Amount"]
        )

        service_costs[service] = (
                service_costs.get(service, Decimal("0")) + amount
        )


# -----------------------------------------
# Generate FinOps Report
# -----------------------------------------

print("=" * 55)
print(f"{PROJECT_NAME.upper()} - FINOPS REPORT")
print("=" * 55)

print(f"Start Date: {start_date}")
print(f"End Date:   {end_date}")
print()

print("AWS SERVICE COST BREAKDOWN")
print("-" * 55)

total_cost = Decimal("0")

for service, cost in sorted(
        service_costs.items(),
        key=lambda item: item[1],
        reverse=True
):

    if cost > 0:
        print(f"{service:<40} ${cost:.2f}")
        total_cost += cost

print("-" * 55)
print(f"TOTAL AWS COST: ${total_cost:.2f}")

print()
print("FINOPS REPORT COMPLETE")