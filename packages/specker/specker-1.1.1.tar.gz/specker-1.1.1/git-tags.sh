#!/usr/bin/env bash

set -e
set -o pipefail

HAVE_JQ=$(which jq || echo "")
HAVE_CURL=$(which curl || echo "")

if [ -z "${HAVE_JQ}" ]; then
	echo "Missing Required utility: 'jq'"
	exit 1
fi
if [ -z "${HAVE_CURL}" ]; then
	echo "Missing Required utility: 'curl'"
	exit 1
fi

HAVE_JQ=$(which jq || echo "")
HAVE_CURL=$(which curl || echo "")

if [ -z "${HAVE_JQ}" ]; then
	echo "Missing Required utility: 'jq'"
	exit 1
fi
if [ -z "${HAVE_CURL}" ]; then
	echo "Missing Required utility: 'curl'"
	exit 1
fi

cd ${THIS_DIR}
TAG_FLAGS=""

# Repo Name gathering
# Get the URL Encoded Repo name from the .git/config
get_repo() {
	res=$(grep "url = " ${THIS_DIR}/.git/config | sed -r 's/^.*\=\ (https:\/\/(.*\@)?|git\@)gitlab.com(\/|\:)(.*)\.git/\4/g' | sed -r 's|/|%2F|g')
	echo -n $res
}

# Gitlab Request Shortcut
# Make a Gitlab API Request
# Args:
#  - Method: GET/POST/DELETE/etc
#  - URI: API Path to execute on; already contains /api/v4; Include leading slash
#  - Data: If data needs passed, place it here
gitlab_request() {
	METHOD="$1"
	URI="$2"
	DATA="$3"
	if [ -z "$METHOD" ]; then
		METHOD="GET"
	fi
	if [ -n "${DATA}" ]; then
		SEND="-d \"${DATA}\""
	else
		SEND=""
	fi
	if [ -n "${DEBUG}" ]; then
		echo "curl --fail -H \"Authorization: Bearer ${JOB_TOKEN}\" -X ${METHOD} \"https://gitlab.com/api/v4${URI}\" $SEND" >&2
	fi
	res=$(curl --fail -H "Authorization: Bearer ${JOB_TOKEN}" -X ${METHOD} "https://gitlab.com/api/v4${URI}" $SEND)
	echo -n $res
}

# Tag Maker
# Will force create the tag and overwrite the old if the tag already exists
# Args:
#  - Tag: The Tag to create
make_tag() {
	TAG=$1
	repo_enc=$(get_repo)

	gitlab_request "GET" "/projects/${repo_enc}/repository/tags" > /tmp/tags.json
	HAVE_TAG=$(jq -r '.[].name' /tmp/tags.json | grep "${TAG}" || echo "")
	if [ -n "${HAVE_TAG}" ]; then
		tag_enc=$(echo ${TAG} | sed -r 's|/|%2F|g')
		echo "Tag: ${TAG} already exists, this isn't ideal, but we're going to overwrite it"
		gitlab_request "DELETE" "/projects/${repo_enc}/repository/tags/${tag_enc}"
	fi
	commit=$(git log -n 1 --format=raw | grep "commit " | awk '{print $2;}')
	gitlab_request "POST" "/projects/${repo_enc}/repository/tags?tag_name=${TAG}&ref=${commit}"
	echo ""
}

RELEASE_VER=$(echo ${PROJECT_VERSION} | sed -r 's/\.[0-9]{1,}$//g')

# Create a tag for the major.minor version
echo "Creating Release Tag for: ${RELEASE_VER}"
TAG_NAME="tags/release/${RELEASE_VER}"
make_tag $TAG_NAME

# Create a tag for the individual version always
echo "Creating Version Tag for: ${PROJECT_VERSION}"
TAG_NAME="tags/versions/${PROJECT_VERSION}"
make_tag $TAG_NAME