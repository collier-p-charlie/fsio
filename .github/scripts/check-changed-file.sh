#!/bin/bash

BRANCH_NAME=$1  # {{ github.base_ref }}
shift
FILES_TO_CHECK="$@"

FILES_NOT_CHANGED=()
FILES_CHANGED=$(git diff --name-only origin/$BRANCH_NAME...HEAD)

for file in $FILES_TO_CHECK; do
  IS_PRESENT=$(echo $FILES_CHANGED | grep "^$file$")  # either empty or the file
  if [[ -z $IS_PRESENT ]]; then  # if empty no match
    FILES_NOT_CHANGED+=($file)
  fi
done

if [[ ${#FILES_NOT_CHANGED[@]} > 0 ]]; then
  echo "The following files which require updates were not updated: $FILES_NOT_CHANGED"
  exit 1
fi

echo "All files which require updates were updated"
