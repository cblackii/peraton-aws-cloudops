import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Peraton CloudOps application invoked")

    response = {
        "status": "healthy",
        "message": "Peraton AWS CloudOps Lambda operational"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }