#!/bin/bash

. ./functions.sh

#Default test results directory
mkdir -p tests

# If enabled, start throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  enable_throttle
fi

if [ "${DOWNLOAD_TEST_ENABLE}" == "yes"  ]; then
  do_download_test
fi

if [ "${UPLOAD_TEST_ENABLE}" == "yes"  ]; then
  [[ -z ${UPLOAD_TEST_FILE} ]] && echo "ERROR: UPLOAD_TEST_FILE not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_HOST} ]] && echo "ERROR: UPLOAD_TEST_HOST not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_USER} ]] && echo "ERROR: UPLOAD_TEST_USER not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_PASSWORD} ]] && echo "ERROR: UPLOAD_TEST_PASSWORD not set.\n" && exit 1
  do_upload_test
fi

if [ "${PING_TEST_ENABLE}" == "yes"  ]; then
  do_ping_test
fi

# Stop throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  throttle --stop
  [[ $? -gt 0 ]] && echo "ERROR: Cannot stop throttle." && exit 1
fi
