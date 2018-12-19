#!/bin/bash

DATE=$(date "+%F_%H-%M")

# Defaults
SILENT_TEST="${SILENT_TEST:-no}"

# Download test
DOWNLOAD_TEST_COUNT=${DOWNLOAD_TEST_COUNT:-1}
DOWNLOAD_TEST_LOCATION="${DOWNLOAD_TEST_LOCATION:-use}"
DOWNLOAD_TEST_OUTFILE="${DOWNLOAD_TEST_OUTFILE:-tests/download-test-$DATE.out}"
DOWNLOAD_TEST_SILENT="${SILENT_TEST}"

# # Upload test
UPLOAD_TEST_COUNT=${UPLOAD_TEST_COUNT:-1}
[[ -z ${UPLOAD_TEST_FILE} ]] && echo "ERROR: UPLOAD_TEST_FILE not set.\n" && exit 1
UPLOAD_TEST_OUTFILE="${UPLOAD_TEST_OUTFILE:-tests/upload-test-$DATE.out}"
UPLOAD_TEST_SILENT="${SILENT_TEST}"
[[ -z ${UPLOAD_TEST_HOST} ]] && echo "ERROR: UPLOAD_TEST_HOST not set.\n" && exit 1
[[ -z ${UPLOAD_TEST_USER} ]] && echo "ERROR: UPLOAD_TEST_USER not set.\n" && exit 1
[[ -z ${UPLOAD_TEST_PASSWORD} ]] && echo "ERROR: UPLOAD_TEST_PASSWORD not set.\n" && exit 1
UPLOAD_TEST_PASSIVE="${UPLOAD_TEST_PASSIVE:-no}"

# # Ping test
PING_TEST_ENABLE=no
# PING_TEST_COUNT=1
# PING_TEST_FILE=
# PING_TEST_OUTFILE=
# PING_TEST_INTERFACE=Default
# PING_TEST_SILENT=${SILENT_TEST}
#
# # Throttle settings
THROTTLE_ENABLE="${THROTTLE_ENABLE:-no}"
#THROTTLE_PROFILE=""

function enable_throttle() {
  [[ "${SILENT_TEST}" == "yes" ]] && silent=" &>/dev/null"

  # Setup throttle
  [[ ! -z ${THROTTLE_DOWN_SPEED} ]] && THROTTLE_DOWN_SPEED="--down ${THROTTLE_DOWN_SPEED}"
  [[ ! -z ${THROTTLE_UP_SPEED} ]] && THROTTLE_UP_SPEED="--up ${THROTTLE_UP_SPEED}"
  [[ ! -z ${THROTTLE_RTT} ]] && THROTTLE_RTT="--rtt ${THROTTLE_RTT}"

  if [ ! -z ${THROTTLE_PROFILE} ]; then
    eval "throttle --profile ${THROTTLE_PROFILE} ${silent}"
  else
    eval "throttle ${THROTTLE_UP_SPEED} ${THROTTLE_DOWN_SPEED} ${THROTTLE_RTT} ${silent}"
    [[ $? -gt 0 ]] && echo "ERROR: Cannot setup throttle." && exit 1
  fi
}

function do_download_test() {
  download_test_params=" -c ${DOWNLOAD_TEST_COUNT} \
                         -l ${DOWNLOAD_TEST_LOCATION} \
                         -o `pwd`/${DOWNLOAD_TEST_OUTFILE}"

  if [ ! -z ${DOWNLOAD_TEST_URL} ]; then
    download_test_params+=" -u ${DOWNLOAD_TEST_URL}"
  fi
  if [ "${DOWNLOAD_TEST_SILENT}" == "yes" ]; then
    download_test_params+=" -s"
  fi

  # Run test
  eval "download-tester ${download_test_params}"
}

function do_upload_test() {
  upload_test_params=" -c ${UPLOAD_TEST_COUNT} \
                       -f `pwd`/${UPLOAD_TEST_FILE} \
                       -o `pwd`/${UPLOAD_TEST_OUTFILE} \
                       -l ${UPLOAD_TEST_HOST} \
                       -u ${UPLOAD_TEST_USER}\
                       -p ${UPLOAD_TEST_PASSWORD}"

  if [ "${UPLOAD_TEST_PASSIVE}" == "yes" ]; then
    upload_test_params+=" -P yes"
  fi
  if [ "${UPLOAD_TEST_SILENT}" == "yes" ]; then
    upload_test_params+=" -s"
  fi

  # Run test
  eval "upload-tester ${upload_test_params}"
}

function do_ping_test() {
  echo "TODO !!"
}
