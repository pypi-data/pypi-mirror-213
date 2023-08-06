"""OwlML datasets API."""
import time
from functools import partial
from typing import Any, Optional

from .api import OwlMLAPI
from .utils import pagination_iterator


def list_versions(dataset: Optional[str] = None) -> list[dict[str, Any]]:
    """List dataset versions."""

    def _list_versions_page(page: int, dataset: Optional[str] = None) -> dict[str, Any]:
        """Get a dataset versions page."""
        route = f"dataset-versions?page={page}"
        if dataset is not None:
            route += f"&dataset={dataset}"
        return OwlMLAPI.get(route)

    _list_version_partial = partial(_list_versions_page, dataset=dataset)
    return list(pagination_iterator(_list_version_partial))


def version_dataset(dataset: str, slug: Optional[str] = None) -> dict[str, Any]:
    """Version a dataset."""
    payload = dict(dataset=dataset)
    if slug is not None:
        payload["slug"] = slug
    version = OwlMLAPI.post("dataset-versions", payload)
    while version == {}:
        time.sleep(0.25)
        version = OwlMLAPI.post("dataset-versions", payload)
    return version
