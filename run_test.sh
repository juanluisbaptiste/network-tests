#!/bin/bash

. /functions.sh
. /.env

#Default test results directory
mkdir -p ${TESTS_RESULTS_DIR}
rm -fr ${TMP_RESULTS_DIR}
mkdir -p ${TMP_RESULTS_DIR}

# If enabled, start throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  echo ""
  enable_throttle
  echo ""
fi

if [ "${DOWNLOAD_TEST_ENABLE}" == "yes"  ]; then
  echo -e "\n* Starting download tests...\n"
  do_download_test
  echo -e "\n* Done.\n"
fi

if [ "${UPLOAD_TEST_ENABLE}" == "yes"  ]; then
  [[ -z ${UPLOAD_TEST_FILE} ]] && echo "ERROR: UPLOAD_TEST_FILE not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_HOST} ]] && echo "ERROR: UPLOAD_TEST_HOST not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_USER} ]] && echo "ERROR: UPLOAD_TEST_USER not set.\n" && exit 1
  [[ -z ${UPLOAD_TEST_PASSWORD} ]] && echo "ERROR: UPLOAD_TEST_PASSWORD not set.\n" && exit 1
  echo -e "\n* Starting upload tests...\n"
  do_upload_test
  echo -e "\n* Done.\n"
fi

if [ "${PING_TEST_ENABLE}" == "yes"  ]; then
  echo -e "\n* Starting ping tests...\n"
  do_ping_test
  echo -e "\n* Done.\n"
fi

# Stop throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  throttle --stop
  [[ $? -gt 0 ]] && echo "ERROR: Cannot stop throttle." && exit 1
fi

if [ "${COMPRESS_RESULTS}" == "yes" ]; then
  compress_results
fi

if [ "${SEND_RESULTS_EMAIL}" == "yes" ]; then
  email_results
fi
