#!/bin/bash

BRANCH_NAME="$1"
echo "Checking branch name: $BRANCH_NAME"

if [[ ! $BRANCH_NAME =~ ^(feature|bugfix)/.+$ ]]; then
  echo "Branch name must start with 'feature/' or 'bugfix/'" && exit 1
fi

echo "Branch name is valid"
