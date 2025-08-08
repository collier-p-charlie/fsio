# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

That is, given a version number `MAJOR.MINOR.PATCH`, increment the:

- **MAJOR** version when you make incompatible changes
- **MINOR** version when you add functionality in a backwards compatible manner
- **PATCH** version when you make backwards compatible bug fixes


## [1.3.3](https://github.com/collier-p-charlie/fsio/compare/1.3.2...1.3.3) 2025-08-08

### Amended
- Adding `uv` installation which was missing from `uv publish` steps.


## [1.3.2](https://github.com/collier-p-charlie/fsio/compare/1.3.1...1.3.2) 2025-08-07

### Amended
- Amended use of `uv` for more clarity in **GitHub** action.
- Adding [uv.lock](uv.lock) file and [.python_version](.python-version).


## [1.3.1](https://github.com/collier-p-charlie/fsio/compare/1.3.0...1.3.1) 2025-08-04 [Issue](https://github.com/collier-p-charlie/fsio/issues/22)

### Added
- Adding `ruff` linting/formatting to **GitHub actions**.
- Also added `pre-commit` for linting and `mypy` checks per commit locally.


## [1.3.0](https://github.com/collier-p-charlie/fsio/compare/1.2.0...1.3.0) 2025-07-07 [Issue](https://github.com/collier-p-charlie/fsio/issues/19)

### Added
- Method for detecting **avro**, **orc**, **xlsx**, **xml** files and **bz2**, **gz**, **zip** compressed files.

### Amended
- Moved the [.coveragerc]() settings to the [pyproject.toml](pyproject.toml).
- Updated the [README](README.md) for explanations of usage and how to install, alongside _badges_.


## [1.2.0](https://github.com/collier-p-charlie/fsio/compare/1.1.0...1.2.0) 2025-07-06 [Issue](https://github.com/collier-p-charlie/fsio/issues/16)

### Added
- Method `detect_file_type` to use current available methods to detect file type of given **BytesIO** object.

### Amended
- Layout of the _documentation_, adding a link back to the main **GitHub** _pages_ site.


## [1.1.0](https://github.com/collier-p-charlie/fsio/compare/1.0.0...1.1.0) 2025-07-06 [Issue](https://github.com/collier-p-charlie/fsio/issues/13)

### Added
- Method `detect_file_type` to use current available methods to detect file type of given **BytesIO** object.

### Amended
- Updated **PR** template.


## [1.0.0](https://github.com/collier-p-charlie/fsio/compare/0.0.3.dev2...1.0.0) 2025-07-05

### Amended
- **GitHub** action takes _version_ from `pyproject.toml` not tag on release.


## [0.0.3.dev2](https://github.com/collier-p-charlie/fsio/compare/0.0.3.dev1...0.0.3.dev2) 2025-07-05

### Amended
- **GitHub** action for documentation ordering; **git** issue before checkout.


## [0.0.3.dev1](https://github.com/collier-p-charlie/fsio/compare/0.0.2...0.0.3.dev1) 2025-07-05

### Added
- **mkdocs** for documentation website.
- **GitHub** action to deploy the documentation to **GitHub** _pages_.

### Amended
- Renaming `detect_type` class to `file_type`.


## [0.0.2](https://github.com/collier-p-charlie/fsio/compare/0.0.2.dev1...0.0.2) 2025-07-05

- All functionality working; testing **PyPI** upload.

### Added
- Unit testing using **Test PyPI** package from **dev** to **main**.


## [0.0.2.dev1](https://github.com/collier-p-charlie/fsio/compare/0.0.1...0.0.2.dev1) 2025-07-05

### Added
- Functionality to test for whether a `BytesIO` _file_ is of **PARQUET** type.
- Relevant **GitHub** workflows for publishing to **PyPI** and validation checks.


## [0.0.1]()
[2025-07-04]()

- Start of changelog.
