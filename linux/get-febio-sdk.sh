#! /bin/bash
set -o verbose

set -x

OS="${OS}"
BUCKET="${BUCKET:-febio-packages}"
PACKAGE="${PACKAGE:-febio4-sdk}"
PACKAGE_NAME="${PACKAGE_NAME:-febio4}"
FEBIO_SDK_BRANCH="${FEBIO_SDK_BRANCH:-develop}"
FEBIO_VERSION="${FEBIO_VERSION:-v}"

PACKAGE_PREFIX="${PACKAGE_NAME}/${FEBIO_SDK_BRANCH}/${OS}/"
PACKAGE_SEARCH="${PACKAGE}-${FEBIO_VERSION}"

PACKAGE_URI=$(aws --output json s3api list-objects \
	--bucket "$BUCKET" \
	--prefix "$PACKAGE_PREFIX" \
	--query "reverse(sort_by(Contents,&LastModified)) && Contents[?contains(Key, '$PACKAGE_SEARCH')]" \
	| jq -r -e '. | max_by(.LastModified) | .Key')

STATUS=$?

if [[ ! -z "${PACKAGE_URI}" ]] && [[ $PACKAGE_URI != null ]]; then
	echo "SDK found at ${PACKAGE_URI}"
	ARCHIVE="${PACKAGE_URI##*/}"
	aws s3 cp "s3://$BUCKET/$PACKAGE_URI" .
	tar xzf "$ARCHIVE"
else
	echo "SDK not found at ${PACKAGE_PREFIX}${PACKAGE_SEARCH}*"; exit $STATUS
fi
