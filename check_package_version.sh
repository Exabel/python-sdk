#!/usr/bin/env bash

VERSION="v$(grep '^version = ' pyproject.toml | cut -d'"' -f2)"
GIT_TAG=$(git describe --tags)

echo "Verifying current git tag is the same as version set in pyproject.toml"
if [ $VERSION != $GIT_TAG ]; then
    echo "Current git tag does not match version set in pyproject.toml. Aborting build ..."
    echo "GIT_TAG: $GIT_TAG"
    echo "VERSION: $VERSION"
    exit 1;
fi
