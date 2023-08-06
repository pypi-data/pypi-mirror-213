"""Module for handling the different types of MarketPlace apps and their
capabilities.
.. currentmodule:: marketplace.app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""
from typing import Optional

from packaging.version import parse

from ..client import MarketPlaceClient
from .utils import camel_to_snake
from .v0 import MarketPlaceApp as _MarketPlaceApp_v0


def get_app(app_id, client: Optional[MarketPlaceClient] = None, **kwargs):
    """Get an app instance.
    Args:
        app_id (str): client id of the app
        **kwargs: keyword arguments for the app
    Returns:
        MarketPlaceApp: app instance
    """
    client = client or MarketPlaceClient()

    # Getting api version and list of capabilities for the application
    app_service_path = f"api/applications/{app_id}"
    app_info: dict = client.get(path=app_service_path).json()
    app_api_version = parse(app_info.get("api_version", "1.0.0"))

    capabilities = []
    for capability in app_info["capabilities"]:
        capabilities.append(camel_to_snake(capability["name"]))

    if app_api_version < parse("1.0.0"):
        return _MarketPlaceApp_v0(app_id, app_info, client, **kwargs)
    else:
        raise RuntimeError(f"App API version ({app_api_version}) not supported.")


__all__ = [
    "MarketPlaceApp",
]
