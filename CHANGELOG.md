# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

That is, given a version number `MAJOR.MINOR.PATCH`, increment the:

- **MAJOR** version when you make incompatible changes
- **MINOR** version when you add functionality in a backwards compatible manner
- **PATCH** version when you make backwards compatible bug fixes


## [1.1.0] 
[2025-07-06]()
[Issue](https://github.com/collier-p-charlie/fsio/issues/13)

### Added
- Method `detect_file_type` to use current available methods to detect file type of given **BytesIO** object.

### Amended
- Updated **PR** template.


## [1.0.0] 
[2025-07-05]()

### Amended
- **GitHub** action takes _version_ from `pyproject.toml` not tag on release.


## [0.0.3.dev2] 
[2025-07-05]()

### Amended
- **GitHub** action for documentation ordering; **git** issue before checkout.


## [0.0.3.dev1] 
[2025-07-05]()

### Added
- **mkdocs** for documentation website.
- **GitHub** action to deploy the documentation to **GitHub** _pages_.

### Amended
- Renaming `detect_type` class to `file_type`.


## [0.0.2] 
[2025-07-05]()

- All functionality working; testing **PyPI** upload.

### Added
- Unit testing using **Test PyPI** package from **dev** to **main**.


## [0.0.2.dev1] 
[2025-07-05]()

### Added
- Functionality to test for whether a `BytesIO` _file_ is of **PARQUET** type.
- Relevant **GitHub** workflows for publishing to **PyPI** and validation checks.


## [0.0.1] 
[2025-07-04]()

- Start of changelog.
