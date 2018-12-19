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
