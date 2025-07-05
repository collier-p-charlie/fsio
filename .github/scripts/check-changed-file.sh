#!/bin/bash

BASE_REF=$1  # {{ github.base_ref }}
shift
FILES_TO_CHECK=$@

echo "DEBUG: FILES_TO_CHECK below"
echo $FILES_TO_CHECK

FILES_NOT_CHANGED=()
FILES_CHANGED=$(git diff --name-only origin/$BASE_REF...HEAD)

echo "DEBUG: FILES_CHANGED below"
echo $FILES_CHANGED

for file in $FILES_TO_CHECK; do
  IS_PRESENT=$(echo $FILES_CHANGED | grep $file)  # either empty or the file
  echo "FOR LOOP: $file"
  echo "IS_PRESENT = $IS_PRESENT"
  if [[ -z $IS_PRESENT ]]; then  # if empty no match
    echo "INNER IF CONDITION"
    FILES_NOT_CHANGED+=($file)
  fi
done

echo "DEBUG: Files not changed below"
echo $FILES_NOT_CHANGED

if [[ ${#FILES_NOT_CHANGED[@]} > 0 ]]; then
  echo "The following files which require updates were not updated: $FILES_NOT_CHANGED"
  exit 1
fi

echo "All files which require updates were updated"
