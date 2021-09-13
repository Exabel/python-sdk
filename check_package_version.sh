#!/usr/bin/env bash

VERSION="v$(<VERSION)"
GIT_TAG=$(git describe --tags)

echo "Verifying current git tag is the same as version set in VERSION"
if [ $VERSION != $GIT_TAG ]; then
    echo "Current git tag does not match version set in VERSION. Aborting build ..."
    echo "GIT_TAG: $GIT_TAG"
    echo "VERSION: $VERSION"
    exit 1;
fi
