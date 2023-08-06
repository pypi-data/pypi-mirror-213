import sys
from typing import Dict, Tuple
from uuid import uuid4

from snowmate_common.messages_data.messages import MainMessage
from snowmate_common.utils.compressing import compress_data

MAX_DATA_SIZE = 50 * 1024
MESSAGE_GROUP_ID = "1"
AUTHORIZATION_HEADER = "Authorization"


class SQSFields:
    MESSAGE_BODY = "MessageBody"
    MESSAGE_GROUP_ID = "MessageGroupId"
    MESSAGE_DEDUPLICATION_ID = "MessageDeduplicationId"


class S3Fields:
    DATA = "data"


class Destinations:
    BASELINE = "baseline"
    REGRESSIONS = "regressions"


class Routes:
    LARGE = "large"
    ENQUEUE = "enqueue"


class RequestMethods:
    POST = "POST"
    PUT = "PUT"


def create_message(
    base_url: str, destination: str, message: MainMessage
) -> Tuple[str, str, Dict, Dict]:
    compressed_message = compress_data(bytes(message))
    if sys.getsizeof(compressed_message) >= MAX_DATA_SIZE:
        url = f"{base_url}/{destination}/{Routes.LARGE}"
        method = RequestMethods.PUT
        payload = {S3Fields.DATA: compressed_message}
    else:
        url = f"{base_url}/{destination}/{Routes.ENQUEUE}"
        method = RequestMethods.POST
        payload = {
            SQSFields.MESSAGE_BODY: compressed_message,
            SQSFields.MESSAGE_GROUP_ID: MESSAGE_GROUP_ID,
            SQSFields.MESSAGE_DEDUPLICATION_ID: str(uuid4()),
        }
    headers = {AUTHORIZATION_HEADER: f"Bearer {message.access_token}"}
    return method, url, headers, payload
