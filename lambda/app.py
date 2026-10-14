import json
import logging

# Configure application logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler for the Peraton CloudOps Lab.

    Supports:
    - Normal application health checks
    - Controlled failure simulation
    - CloudWatch application logging
    """

    logger.info("Peraton CloudOps application invoked")

    # -----------------------------------------
    # Controlled incident simulation
    # -----------------------------------------
    if event.get("simulate_failure") is True:
        logger.error("Simulated application failure detected")
        raise RuntimeError("Peraton CloudOps simulated failure")

    # -----------------------------------------
    # Healthy application response
    # -----------------------------------------
    response = {
        "status": "healthy",
        "message": "Peraton AWS CloudOps Lambda operational"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }