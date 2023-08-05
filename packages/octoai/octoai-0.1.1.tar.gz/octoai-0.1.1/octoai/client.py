"""Client used to infer from endpoints."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import httpx
import yaml

import octoai
from octoai.errors import OctoAIClientError, OctoAIServerError
from octoai.utils import retry


class Client:
    """A class that allows inferences from existing endpoints.

    :param token: api token, defaults to None
    :type token: str, optional
    :param public_endpoints_url: str, url to fetch available public models,
        defaults to "https://api.octoai.cloud/v1/public-endpoints"
    :type public_endpoints_url: str
    :param config_path: path to '/.octoai/config.yaml'.  Installed in ~,
        defaults to None and will check home path
    :type config_path: Optional[str]

    Sets various headers. Gets auth token from environment if none is provided.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        public_endpoints_url: Optional[
            str
        ] = "https://api.octoai.cloud/v1/public-endpoints",
        config_path: Optional[str] = None,
    ) -> None:
        """Initialize the :class: `octoai.Client` with an auth token.

        :raises OctoAIServerError: server-side failures (unreachable, etc)
        :raises OctoAIClientError: client-side failures (throttling, unset token)
        """
        self._public_endpoints: Dict[str, str] = {}
        self._public_endpoints_url = public_endpoints_url

        token = token if token else os.environ.get("OCTOAI_TOKEN", None)

        if not token:
            # Default path is ~/.octoai/config.yaml for token, can be overridden
            path = Path(config_path) if config_path else Path.home()
            try:
                with open(
                    (path / Path(".octoai/config.yaml")), encoding="utf-8"
                ) as octoai_config_yaml:
                    config_dict = yaml.safe_load(octoai_config_yaml)
                token = config_dict.get("token")
            except FileNotFoundError:
                token = None

        if not token:
            logging.warning(
                "OCTOAI_TOKEN environment variable is not set. "
                + "You won't be able to reach OctoAI endpoints."
            )

        version = octoai.__version__  # type: ignore
        headers = {
            "Content-Type": "application/json",
            "user-agent": f"octoai-{version}",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._headers = headers
        # Set all timeouts to 900 seconds to account for cold starts, latency.
        timeout = httpx.Timeout(timeout=900.0)
        self._httpx_client = httpx.Client(timeout=timeout, headers=headers)

    def _initialize_public_endpoints(self) -> None:
        """Initialize self._public_endpoints with dict of names to urls."""
        response = httpx.get(url=self._public_endpoints_url, headers=self._headers)
        if response.status_code == 200:
            response_json = response.json()
            for model in response_json:
                self._public_endpoints[model["name"]] = model["endpoint"] + "/predict"
        else:
            self.error(response.status_code, response.text)

    def infer(self, endpoint_url: str, inputs: Mapping[str, Any]) -> Mapping[str, Any]:
        """Send a request to the given endpoint URL with inputs as request body.

        :param endpoint_url: target endpoint
        :type endpoint_url: str
        :param inputs: inputs for target endpoint
        :type inputs: Mapping[str, Any]

        :raises OctoAIServerError: server-side failures (unreachable, etc)
        :raises OctoAIClientError: client-side failures (throttling, unset token)

        :return: outputs from endpoint
        :rtype: Mapping[str, Any]
        """
        resp = retry(lambda: self._httpx_client.post(url=endpoint_url, json=inputs))
        if resp.status_code != 200:
            self.error(resp.status_code, resp.text)
        return resp.json()

    def error(self, status_code: int, text: str):
        """Raise error of correct type for status code including message.

        :param status_code: HTTP status_code
        :type status_code: int
        :param text: error message from API server
        :type text: str

        :raises OctoAIServerError: server-side failures (unreachable, etc)
        :raises OctoAIClientError: client-side failures (throttling, unset token)
        """
        if status_code >= 500:
            raise OctoAIServerError(f"Server error: {status_code} {text}")
        elif status_code == 429:
            raise OctoAIClientError(f"Throttling error: {status_code} {text}")
        else:
            raise OctoAIClientError(f"Error: {status_code} {text}")

    @property
    def public_endpoints(self) -> Dict[str, str]:
        """Return dict of public endpoint names as strs to endpoint urls as strs.

        :return: Dict of public endpoint name to URL.
        :rtype: Dict[str, str]
        """
        return self._public_endpoints
