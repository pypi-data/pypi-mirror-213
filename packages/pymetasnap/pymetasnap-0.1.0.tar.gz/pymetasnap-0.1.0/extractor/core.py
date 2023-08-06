from pathlib import Path
from typing import Dict

import pandas as pd
import requests
from loguru import logger
from rich import print
from rich.progress import track

from extractor.render import Requirements

URLBASE = "https://pypi.org/pypi"


def get_raw_data(project: str) -> Dict[str, str]:
    """
    Retrieve raw metadata for a project from a given URL.

    Args:
        project: The name of the project.

    Returns:
        A dictionary containing the raw metadata of the project.
    """
    try:
        r = requests.get(
            f"{URLBASE}/{project}/json", headers={"Accept": "application/json"}
        )
    except Exception as e:
        logger.error(e)
    else:
        return r.json()["info"]


def filter_data(raw_data: Dict[str, str], version: str) -> Dict[str, str]:
    """
    Filter relevant metadata from raw data.

    Args:
        raw_data: The raw metadata of a project.
        version: The version of the project.

    Returns:
        A dictionary containing filtered metadata.
    """
    return {
        "name": raw_data["name"],
        "version": version or raw_data["version"],
        "license": raw_data["license"],
        "repository": raw_data["home_page"],
        "project_url": raw_data["project_url"],
        "version_url": f"{raw_data['project_url']}{version}/"
        if version
        else raw_data["release_url"],
    }


def generate_data(source_path: Path, output: Path, format: str) -> None:
    """
    Generate data based on the specified requirements format.

    Args:
        source_path: The path to the requirements file.
        output: The path to store the generated data.
        format: The format of the requirements file.

    Returns:
        None
    """
    print("Starting process")
    print(f"Retrieving: {source_path}")
    result = Requirements().render(source_path, format)
    pkgs_raw_metadata = []
    for pkg in track(result, description="Processing..."):
        filtered_data = filter_data(
            get_raw_data(pkg[0]), pkg[1] if len(pkg) > 1 else None
        )
        pkgs_raw_metadata.append(filtered_data)
    df = pd.DataFrame(pkgs_raw_metadata)
    print(f"Storing into: {output}")
    if str(output).endswith(".csv"):
        df.to_csv(output, index=False)
    elif str(output).endswith(".xlsx"):
        df.to_excel(output, index=False)
    else:
        logger.error("Not supported format.")
