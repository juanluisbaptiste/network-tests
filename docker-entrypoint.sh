#!/bin/bash
env

DATE=$(date "+%F_%H-%M")

# Defaults
# Download test
DOWNLOAD_TEST_COUNT=${DOWNLOAD_TEST_COUNT:-1}
DOWNLOAD_TEST_LOCATION="${DOWNLOAD_TEST_LOCATION:-use}"
DOWNLOAD_TEST_OUTFILE="${DOWNLOAD_TEST_OUTFILE:-download-test-$DATE.out}"
DOWNLOAD_TEST_SILENT="${DOWNLOAD_TEST_SILENT:-no}"

# # Upload test
# UPLOAD_TEST_COUNT=1
# UPLOAD_TEST_FILE=
# UPLOAD_TEST_OUTFILE=
# UPLOAD_TEST_SILENT=no
# UPLOAD_TEST_HOST=
# UPLOAD_TEST_USER=
# UPLOAD_TEST_PASSWORD=
# UPLOAD_TEST_PASSIVE=no
#
# # Ping test
# PING_TEST_COUNT=1
# PING_TEST_FILE=
# PING_TEST_OUTFILE=
# PING_TEST_INTERFACE=Default
# PING_TEST_SILENT=no
#
# # Throttle settings
THROTTLE_ENABLE="${THROTTLE_ENABLE:-no}"
#THROTTLE_PROFILE=""
[[ ! -z ${THROTTLE_DOWN_SPEED} ]] && THROTTLE_DOWN_SPEED="--down ${THROTTLE_DOWN_SPEED}"
[[ ! -z ${THROTTLE_UP_SPEED} ]] && THROTTLE_UP_SPEED="--up ${THROTTLE_UP_SPEED}"
[[ ! -z ${THROTTLE_RTT} ]] && THROTTLE_RTT="--rtt ${THROTTLE_RTT}"

# If enabled, start throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  if [ ! -z ${THROTTLE_PROFILE} ]; then
    throttle --profile ${THROTTLE_PROFILE}
  else
    throttle ${THROTTLE_UP_SPEED} ${THROTTLE_DOWN_SPEED} ${THROTTLE_RTT}
    [[ $? -gt 0 ]] && echo "ERROR: Cannot setup throttle." && exit 1
  fi
fi

if [ "${DOWNLOAD_TEST_ENABLE}" == "yes"  ]; then
  download_test_params=" -c ${DOWNLOAD_TEST_COUNT} -l ${DOWNLOAD_TEST_LOCATION} -o `pwd`/${DOWNLOAD_TEST_OUTFILE}"

  if [ ! -z ${DOWNLOAD_TEST_URL} ]; then
    download_test_params+=" -u ${DOWNLOAD_TEST_URL}"
  fi
  if [ "${DOWNLOAD_TEST_SILENT}" == "yes" ]; then
    download_test_params+=" -s"
  fi

  # Run test
  download-tester ${download_test_params}
fi

# Stop throttle
if [ "${THROTTLE_ENABLE}" == "yes" ]; then
  throttle --stop
  [[ $? -gt 0 ]] && echo "ERROR: Cannot stop throttle." && exit 1
fi
