"""API class for OwlML."""
import os
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


def _get_required_env_var(env_var: str) -> str:
    """Get an environment variable or raise an error if it doesn't exist."""
    value = os.getenv(env_var)
    if value is None:
        raise ValueError(f"Missing required environment variable: {env_var}")
    return value


def raise_for_status(response: requests.Response) -> None:
    """Raise an error if the response status code is not 200."""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(
            f"{error}\nResponse body: {response.text}"
        ) from error


class OwlMLAPI:
    """API class for OwlML."""

    base_url: str = _get_required_env_var("OWLML_URL")
    api_url: str = os.path.join(base_url, "api")
    basic_auth: HTTPBasicAuth = HTTPBasicAuth(
        _get_required_env_var("OWLML_USERNAME"), _get_required_env_var("OWLML_PASSWORD")
    )

    @classmethod
    def get(cls, route: str) -> dict[str, Any]:
        """Make a GET request to the OwlML API."""
        response = requests.get(os.path.join(cls.api_url, route), auth=cls.basic_auth)
        raise_for_status(response)
        if response.status_code == 204:
            return {}
        return response.json()

    @classmethod
    def post(cls, route: str, payload: dict[str, Any] = dict()) -> dict[str, Any]:
        """Make a POST request to the OwlML API."""
        response = requests.post(
            os.path.join(cls.api_url, route), auth=cls.basic_auth, json=payload
        )
        raise_for_status(response)
        if response.status_code == 204:
            return {}
        return response.json()
