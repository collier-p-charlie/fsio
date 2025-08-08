# File System IO

| Badges     |                                                                                                                                                                                                 |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| License    | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)                                                                                     |
| PyPI       | [![PyPI version](https://badge.fury.io/py/fsio.svg)](https://badge.fury.io/py/fsio) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fsio.svg)](https://pypi.org/project/fsio/) |

| Version | Build Status                                                                                                                                                                                                                                                                                                                         |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Main    | [![GitHub Build main](https://github.com/collier-p-charlie/fsio/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/collier-p-charlie/fsio/actions) [![GitHub Build main](https://github.com/collier-p-charlie/fsio/actions/workflows/python-publish.yaml/badge.svg)](https://github.com/collier-p-charlie/fsio/actions) |


[File System IO]() or simply **FSIO** is a **Python** package containing useful _file system_ operations.


**Table of contents**

- [Installation](#installation)
- [Getting Started](#getting-started)
- [CLI](#cli)
- [Development](#development)


## Installation

Installing the _main_ package is as simple as downloading from **PyPI**.

```python
pip install 'fsio==$VERSION'
```

If you also require use of the **CLI**, then you can install _with extras_ as follows.

```python
pip install 'fsio[cli]==$VERSION'
```


## Getting Started

This package was designed for simplifying some _file system operations_.
Its original design was for detecting file types of a file, but it has been expanded beyond this.
The main code lives within the [core](src/fsio/core) directory. Here, for example, you will see the
[file_type](src/fsio/core/file_type.py) class which supports the `detect-file-type` commands within the **CLI**.
Moreover, we can use this within **Python** code provided we have the object in **BytesIO** form.
For example, suppose we have a `.parquet` file without an extension and we want to establish its type,
and confirm that it really is of type _parquet_. To do this, we could do something as follows.

```python
>>> from io import BytesIO
>>> from pathlib import Path
>>>
>>> from fsio.core import FileType
>>>
>>> path_to_file = Path('path/to/suspected/parquet')
>>>
>>> with path_to_file.open('rb') as f:
>>>     body = BytesIO(f.read())
>>>
>>> FileType.detect_file_type(body)
'parquet'
```

## CLI

If you optionally installed the `cli` subpackage, then you get extra functionality and are able to use most of the
functionality from the `core` package. For example, you can _detect the file type_ of a given _file_ using the command

```shell
fsio detect-file-type path/to/file.ext
```

This will return the type of the file to the **stdout**, for example `parquet`.
You can get more information about each command by using the `--help` flag on each command.
The **CLI** was designed using [typer](https://typer.tiangolo.com), from the creators of **FastAPI**.
A list of the following **CLI** commands which are available are below.

| Commands                     |                                            |
|------------------------------|--------------------------------------------|
| `fsio detect-file-type FILE` | Detect the _type_ of `FILE` given as input |
| `fsio supported-types`       | List the current supportoed file types     |


## Development

To contribute to this project, you can clone the repository and install the development dependencies.
This can be done using `uv sync --all-extras` (which uses the [uv.lock](uv.lock) file for consistency).
There is a [`pre-commit`](https://pre-commit.com/) hook which will run on each commit to ensure that the code is formatted correctly.
To install this, we need to run

```bash
uv sync --extra test
```

to install `pre-commit` and then run `pre-commit install` in terminal.
We can manually run the `pre-commit` hooks using the command

```bash
pre-commit run --all-files
```

### Branching

When creating a new branch, please use one of the following:

- `feature/*` for _new features_ (branch from and **PR** to `develop`);
- `bugfix/*` for _bug fixes_ (non-critical) (branch from and **PR** to `develop`);
- `hotfix/*` for _hotfixes_ (branch from and **PR** to `main`, syncing to `develop`); and
- `release/*` for _releases_ (branch from `develop` with **PR** to `main`, syncing to `develop`).

The `main` branch is the stable deployment, and `release` branches are used for preparing a new release.
