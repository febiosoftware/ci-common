#! /bin/bash
set -x
SOURCE=$1
DIR=$(dirname "$SOURCE")
SOURCE=$(basename "$SOURCE")
TARGET_NAME=$SOURCE
pushd "$DIR" || exit 1
OS=${OS:-Linux}
PACKAGE="${TARGET_NAME}-${GIT_TAG}-${OS}.tar.gz"
BUCKET_NAME=${BUCKET_NAME:-febio-packages}
REF_NAME=${REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}
PACKAGE_NAME=${PACKAGE_NAME:-febio}
tar -czf "$PACKAGE" "$SOURCE"
TARGET="s3://${BUCKET_NAME}/${PACKAGE_NAME}/${REF_NAME}/${OS}/${PACKAGE}"
aws s3 cp "$PACKAGE" "$TARGET"
popd || exit 1
