from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from extractor.core import generate_data
from extractor.utils import get_version_from_pyproject

app = typer.Typer()


class RequirementsFormat(str, Enum):
    pip_list = "pip_list"
    pip_freeze = "pip_freeze"


@app.command(name="version")
def version():
    return print(get_version_from_pyproject())


@app.command()
def main(
    source_path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            prompt=True,
            help="Requirements file path",
        ),
    ] = "",
    output: Annotated[
        Path,
        typer.Option(
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            prompt=True,
            help="Path to store the data",
        ),
    ] = "",
    format: Annotated[
        RequirementsFormat,
        typer.Option(prompt=True, help="Incoming requirements format."),
    ] = RequirementsFormat.pip_freeze,
):
    generate_data(source_path, output, format)


if __name__ == "__main__":
    app()
