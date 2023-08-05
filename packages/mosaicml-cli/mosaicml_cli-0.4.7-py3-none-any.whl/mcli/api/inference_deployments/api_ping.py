""" Ping a InferenceDeployment """
from __future__ import annotations

from http import HTTPStatus
from typing import Callable, Optional, Union, cast

import requests
import validators
from requests import Response

from mcli.api.exceptions import MAPIException
from mcli.api.inference_deployments import get_inference_deployments
from mcli.api.model.inference_deployment import InferenceDeployment

__all__ = ['ping']


def ping(
    deployment: Union[InferenceDeployment, str],
    *,
    timeout: Optional[float] = 10,
) -> dict:
    """Pings an inference deployment that has been launched in the MosaicML platform
    and returns the status of the deployment. The deployment must have a '/ping' endpoint
    defined.
    Arguments:
        deployment: The deployment to check the status of. Can be a InferenceDeployment object,
        the name of an deployment, or a string which is of the form https://<deployment dns>.
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised.
    Raises:
        HTTPError: If pinging the endpoint fails
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    validate_url = cast(Callable[[str], bool], validators.url)
    if isinstance(deployment, str) and not validate_url(deployment):
        # if a string is passed in that is not a url then lookup the deployment and get the name
        deployment_objs = get_inference_deployments(deployments=[deployment])
        if len(deployment_objs) == 0:
            raise MAPIException(HTTPStatus.NOT_FOUND, f'No inference deployment found with name {deployment}.')
        deployment = deployment_objs[0]
    base_url = deployment
    if isinstance(deployment, InferenceDeployment):
        base_url = f'https://{deployment.public_dns}'
    resp: Response = requests.get(url=f'{base_url}/ping', timeout=timeout)

    if resp.ok:
        return {"status": resp.status_code}
    else:
        resp.raise_for_status()
        return {}
