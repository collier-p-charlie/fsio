#!/bin/bash

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
SOURCE_BRANCH=${1:-$CURRENT_BRANCH}
TARGET_BRANCH=$2

if [[ ! $SOURCE_BRANCH =~ ^(feature|bugfix|hotfix|release)/.+$ ]]; then
  echo "Branch name $SOURCE_BRANCH must be of the form '^(feature|bugfix|hotfix|release)/*'"
  exit 1
fi

if [[ $TARGET_BRANCH ]]; then
  echo "Checking source branch $SOURCE_BRANCH against target branch $TARGET_BRANCH"

  if [[ $TARGET_BRANCH =~ develop ]]; then
    if [[ ! $SOURCE_BRANCH =~ ^(feature|bugfix)/.+$ ]]; then
      echo "Source branch must be of the form '^(feature|bugfix)/*' when targeting 'develop'" && exit 1
    fi
  elif [[ $TARGET_BRANCH =~ main ]]; then
    if [[ ! $SOURCE_BRANCH =~ ^(hotfix|release)/.+$ ]] && [[ ! $SOURCE_BRANCH == develop ]]; then
      echo "Source branch must be of the form '^(hotfix|release)/*' or be 'develop' when targeting 'main'" && exit 1
    fi
  else
    echo "Target branch must be either 'develop' or 'main'" && exit 1
  fi
fi

echo "Branch name $SOURCE_BRANCH is valid"
