# -*- encode: utf-8 -*-

import pathlib
from io import BytesIO
from typing import Annotated

import typer

from fsio.core.file_type import FileType

app = typer.Typer()


@app.command(
    help=(
        "Command to return the current supported file types for detection."
    )  # CLI help
)
def supported_types() -> None:
    """
    Function to return all supported file types that can be detected.

    Examples:
        ```shell
        $ fsio supported-types
        csv
        parquet
        ```
    """
    for file_type in FileType.supported_types():
        typer.secho(file_type)


Path = Annotated[pathlib.Path, typer.Argument(default=..., help="Path to the file to detect the type of")]

@app.command(
    help=(
        "Command to determine the file type of the provided file."
    )  # CLI help
)
def detect_file_type(
    file: Path
) -> None:
    """
    Function to detect the _file type_ of the provided file location.

    Args:
        file: The **Path** to the file we want to determine the _type_ for.

    Examples:
        ```shell
        $ fsio detect-file-type path/to/file
        parquet
        ```
    """
    if not file.exists():
        typer.echo(f"[ERROR] File not found: {file}")
        raise typer.Exit(code=1)

    with file.open("rb") as f:
        body = BytesIO(f.read())
        body.seek(0)

    file_type = FileType.detect_file_type(body)
    if file_type:
        typer.secho(file_type, fg=typer.colors.GREEN)
        raise typer.Exit(code=0)

    typer.secho("File type could not be detected", fg=typer.colors.RED)
