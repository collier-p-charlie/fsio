#!/bin/bash

VERSION=$1
CHECK_CHANGELOG=$(grep "\[$VERSION\]" CHANGELOG.md)

if [[ -z $CHECK_CHANGELOG ]]; then
  echo "No CHANGELOG entry for latest version $VERSION"
  exit 1
fi
