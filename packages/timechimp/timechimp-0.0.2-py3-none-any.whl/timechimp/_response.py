"""Helper functions to work with the requests.models.Response"""

import logging
import pprint
from typing import Union
from json.decoder import JSONDecodeError

import requests

from timechimp.exceptions import APIError

logger = logging.getLogger(__name__)


def check_status(response: requests.models.Response) -> None:
    """Check the response status

    :args
        response: the request response

    :raises
        HTTPError depending on the response status code

    :returns
        None
    """
    if not response.ok:
        logger.error(f"Error status code detected for response text={response.text}")
        response.raise_for_status()


def to_json(response: requests.models.Response) -> Union[list, dict]:
    """ Convert a request response to json
    Log the response as text if cannot be decoded to json (useful for debugging)

    :args
        request: the request response to decode

    :raises
       JSONDecodeError: the response could not be decoded to json
       APIError: the API returned an error message

    :returns
        the response converted as a dict or list
    """
    try:
        response_json = response.json()
    except JSONDecodeError as e:
        logger.error(f"Error when trying to decode response={response.text}")
        raise e

    if "message" in response_json:
        raise APIError(pprint.pformat(response_json,
                                      indent=4,
                                      sort_dicts=True))

    return response_json
