"""OwlML datasets API."""
import json
import warnings
from pathlib import Path
from typing import Any, Callable, Optional, Union

from farmhash import fingerprint64
from tqdm import tqdm

from .annotations import read_annotations
from .api import OwlMLAPI
from .images import _download_image, generate_image_id, list_local_images


def create_dataset(org: str, slug: str, labels: list[str]) -> dict[str, Any]:
    """Create a dataset."""
    payload = dict(org=org, slug=slug, labels=labels)
    return OwlMLAPI.post("datasets", payload)


def download_dataset(
    version: str, output_path: Union[str, Path] = "./"
) -> dict[str, Any]:
    """Download dataset version."""
    output_path = Path(output_path)
    version_response = OwlMLAPI.get(f"dataset-versions/{version}")
    if len(version_response["images"]) == 0:
        raise ValueError(f"No images in dataset version {version}.")
    image = next(iter(version_response["images"]))
    image_path = output_path / Path(image["image_id"] + image["extension"])
    dataset_path = image_path.parent.parent.parent
    annotations_path = dataset_path / "annotations" / f"{version}.json"
    annotations_path.parent.mkdir(parents=True, exist_ok=True)
    with open(annotations_path, "w") as f:
        f.write(json.dumps(version_response["annotations"]))
    for image in tqdm(version_response["images"]):
        image_path = output_path / Path(image["image_id"] + image["extension"])
        image_path.parent.mkdir(parents=True, exist_ok=True)
        _download_image(image["presigned_get"], image_path)


def generate_records(
    dataset_directory: Union[str, Path],
    version: str,
    holdout_evaluator: Optional[Callable[[int], bool]] = None,
) -> list[dict[str, Any]]:
    """Generate dataset records for training or evaluation."""
    dataset_directory = Path(dataset_directory)
    image_map = {generate_image_id(p): p for p in list_local_images(dataset_directory)}
    dataset = read_annotations(dataset_directory, version)
    records = []
    for item in dataset["items"]:
        item_id = item["id"]
        if holdout_evaluator and not holdout_evaluator(fingerprint64(item_id)):
            continue
        image_path = image_map.get(item_id)
        if image_path is None:
            warnings.warn(f"Image {item_id} not found.")
            continue
        label_ids = []
        for annotation in item["annotations"]:
            label_ids.append(annotation["label_id"])
        records.append(dict(image_path=image_path, label_ids=label_ids))
    return records
