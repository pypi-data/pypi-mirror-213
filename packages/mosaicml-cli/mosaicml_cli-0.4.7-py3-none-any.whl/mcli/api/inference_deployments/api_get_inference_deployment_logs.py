""" Get an inference deployment's logs from the MosaicML platform"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.api.runs.api_get_run_logs import _get_logs

QUERY_FUNCTION = 'getInferenceDeploymentLogs'
VARIABLE_DATA_NAME = 'getInferenceDeploymentLogsInput'
QUERY = f"""
subscription Subscription(${VARIABLE_DATA_NAME}: GetInferenceDeploymentLogsInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME})
}}"""


@overload
def get_inference_deployment_logs(
    deployment: Union[str, InferenceDeployment],
    *,
    restart: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
) -> Generator[str, None, None]:
    ...


@overload
def get_inference_deployment_logs(
    deployment: Union[str, InferenceDeployment],
    *,
    restart: Optional[int] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Generator[Future[str], None, None]:
    ...


def get_inference_deployment_logs(
    deployment: Union[str, InferenceDeployment],
    *,
    restart: Optional[int] = None,
    timeout: Optional[float] = None,
    future: bool = False,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Get the current logs for an active or completed inference deployment

    Get the current logs for an active or completed inference deployment in the MosaicML platform.
    This returns the full logs as a ``str``, as they exist at the time the request is
    made.

    Args:
        deployment (:obj:`str` | :class:`~mcli.api.model.inference_deployment.InferenceDeployment`): The
            inference deployment to get logs for. If a name is provided, the remaining required deployment details
            will be queried with :func:`~mcli.get_inference_deployments`.
        restart (``Optional[int]``): Which restart of a inference deployment to get logs for. Defaults to the most
            recent deployment restart.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`get_inference_deployment_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the log text, use ``return_value.result()`` with an optional
            ``timeout`` argument.

    Returns:
        If future is False:
            The full log text for a inference deployment at the time of the request as a :obj:`str`
        Otherwise:
            A :class:`~concurrent.futures.Future` for the log text
    """
    # Convert to strings
    deployment_name = deployment.name if isinstance(deployment, InferenceDeployment) else deployment

    filters: Dict[str, Any] = {'name': deployment_name}
    if restart:
        filters['restartCount'] = restart

    variables = {VARIABLE_DATA_NAME: filters}
    for message in _get_logs(QUERY, variables, QUERY_FUNCTION):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message
