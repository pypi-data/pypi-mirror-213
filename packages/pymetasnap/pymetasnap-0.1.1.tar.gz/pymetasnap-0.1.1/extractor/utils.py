import pandas as pd
import toml
from loguru import logger
from rich import print
from rich.progress import track

from extractor.core import filter_data, get_raw_data
from extractor.render import Requirements


def get_version_from_pyproject():
    with open("pyproject.toml") as f:
        pyproject_data = toml.load(f)
        version = (
            pyproject_data.get("tool", {}).get("poetry", {}).get("version")
        )  # noqa
    return version


def filter_requirements(requirements_file_data, installed_requirements_data):
    base_reqs = [req[0] for req in requirements_file_data]
    return [
        ireq for ireq in installed_requirements_data if ireq[0] in base_reqs
    ]  # noqa


def get_filtered_metadata(requirements_file, installed_requirements, output):
    handler = Requirements()
    print("Getting requirements list...")
    requirements_file_data = handler.render(requirements_file, "pip_freeze")
    print("Getting installed libraries list...")
    installed_requirements_data = handler.render(
        installed_requirements, "pip_freeze"
    )  # noqa

    result = filter_requirements(
        requirements_file_data, installed_requirements_data
    )  # noqa

    pkgs_raw_metadata = []
    for pkg in track(result, description="Processing..."):
        filtered_data = filter_data(get_raw_data(pkg[0]), pkg[1])
        pkgs_raw_metadata.append(filtered_data)
    df = pd.DataFrame(pkgs_raw_metadata)
    print(f"Storing into: {output}")
    if output.endswith(".csv"):
        df.to_csv(output, index=False)
    elif output.endswith(".xlsx"):
        df.to_excel(output, index=False)
    else:
        logger.error("Not supported format.")


if __name__ == "__main__":
    requirements_file = "./local/all.txt"
    installed_requirements = "./local/installed.txt"
    output = "./local/ece/metadata.xlsx"
    get_filtered_metadata(requirements_file, installed_requirements, output)
