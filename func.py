import io
import json
import logging

from fdk import response

logger = logging.getLogger(__name__)


def handler(ctx, data: io.BytesIO = None):
    name = "World"
    try:
        body = json.loads(data.getvalue())
        name = body.get("name", name)
    except (json.JSONDecodeError, ValueError) as ex:
        logger.warning('error parsing json payload: %s', ex)

    logger.info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )
