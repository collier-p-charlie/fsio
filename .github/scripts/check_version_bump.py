import sys

from packaging import version

CURRENT_VERSION = sys.argv[1]
DEVELOP_VERSION = sys.argv[2]

if version.parse(CURRENT_VERSION) <= version.parse(DEVELOP_VERSION):
    print(  # noqa: T201
        f"Error: new version {CURRENT_VERSION} is not greater than current develop version {DEVELOP_VERSION}"
    )
    sys.exit(1)
else:
    print(f"Version upgrade OK: {DEVELOP_VERSION} -> {CURRENT_VERSION}")  # noqa: T201
