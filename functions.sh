#!/bin/bash

DATE=$(date "+%F_%H-%M")
MONTH=$(LC_ALL=es_CO.utf8 date +%B|sed -e "s/\b\(.\)/\u\1/g") #First letter upper case
YEAR=$(LC_ALL=es_CO.utf8 date +%Y)
# Defaults
SILENT_TEST="${SILENT_TEST:-no}"
DOWNLOAD_TEST_ENABLE="${DOWNLOAD_TEST_ENABLE:-no}"
UPLOAD_TEST_ENABLE="${UPLOAD_TEST_ENABLE:-no}"
PING_TEST_ENABLE="${PING_TEST_ENABLE:-no}"
THROTTLE_ENABLE="${THROTTLE_ENABLE:-no}"
SEND_RESULTS_EMAIL="${SEND_RESULTS_EMAIL:-no}"
TESTS_RESULTS_DIR="/test_results/"
TMP_RESULTS_DIR="/tmp/network-tests/"
COMPRESS_RESULTS="yes"
COMPRESSED_RESULTS_FILE="/${TESTS_RESULTS_DIR}/network-tests-${DATE}.zip"

# Download test
DOWNLOAD_TEST_COUNT=${DOWNLOAD_TEST_COUNT:-1}
DOWNLOAD_TEST_LOCATION="${DOWNLOAD_TEST_LOCATION:-use}"
DOWNLOAD_TEST_OUTFILE="${DOWNLOAD_TEST_OUTFILE:-download-test-$DATE.csv}"
DOWNLOAD_TEST_SILENT="${SILENT_TEST}"

# # Upload test
UPLOAD_TEST_COUNT=${UPLOAD_TEST_COUNT:-1}
UPLOAD_TEST_OUTFILE="${UPLOAD_TEST_OUTFILE:-upload-test-$DATE.csv}"
UPLOAD_TEST_FILE="${UPLOAD_TEST_FILE:-${TESTS_RESULTS_DIR}/test10Mb.db}"
UPLOAD_TEST_SILENT="${SILENT_TEST}"
UPLOAD_TEST_PASSIVE="${UPLOAD_TEST_PASSIVE:-no}"

# # Ping test
PING_TEST_COUNT=${PING_TEST_COUNT:-1}
PING_TEST_FILE="/opt/network-tests-0.1.4/ping/hosts.txt"
PING_TEST_OUTFILE="${PING_TEST_OUTFILE:-ping-test-$DATE.csv}"
# PING_TEST_INTERFACE="${PING_TEST_INTERFACE:-Default}"
PING_TEST_SILENT=${SILENT_TEST}

TEMPLATE_FILE="${TEMPLATE_FILE:-/templates/network-tests_results}"
SMTP_SERVER="postfix"
SMTP_SUBJECT=${SMTP_SUBJECT:-"Network-tests: Performance Results for ${MONTH} of ${YEAR}"}

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
                         -o ${TMP_RESULTS_DIR}/${DOWNLOAD_TEST_OUTFILE}"

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
                       -f ${UPLOAD_TEST_FILE} \
                       -o ${TMP_RESULTS_DIR}/${UPLOAD_TEST_OUTFILE} \
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
  ping_test_params=" -c ${PING_TEST_COUNT} \
                       -f ${PING_TEST_FILE} \
                       -o ${TMP_RESULTS_DIR}/${PING_TEST_OUTFILE}"

  if [ ! -z ${PING_TEST_INTERFACE} ]; then
    ping_test_params+=" -I ${PING_TEST_INTERFACE}"
  fi

  if [ "${PING_TEST_SILENT}" == "yes" ]; then
    ping_test_params+=" -s"
  fi

  # Run test
  eval "ping-tester ${ping_test_params}"
}

function compress_results() {
  cd ${TMP_RESULTS_DIR}
  echo -e "\n*Compressing tests results...\n"
  zip -r ${COMPRESSED_RESULTS_FILE} *
  [ $? -gt 0 ] && echo -e "- ERROR: Could not compress test results.\n" && exit 1

  echo -e "\n* Done.\n"
}

function email_results() {
  echo "Sending results by email to: ${SMTP_TO}"
  if [ ! -f ${COMPRESSED_RESULTS_FILE} ]; then
    echo "ERROR: File to attach not found."
    sendEmail -f ${SMTP_FROM} -t ${SMTP_FROM} -u "Warning: Cannot find test results file !!" -s ${SMTP_SERVER} -o message-charset=utf8 -m "Could not find test results at: ${COMPRESSED_RESULTS_FILE} ."
    status=$?
    if [ ${status} -ne 0 ]; then
      echo "Could not send error email." >&2 && exit ${status}
    fi
    exit 1
  fi

  content=$(sed -e "s/\${SMTP_TO_NAME}/${SMTP_TO_NAME}/" -e "s/\${MONTH}/${MONTH}/" -e "s/\${YEAR}/${YEAR}/" ${TEMPLATE_FILE})
  status=$?
  if [ $status -ne 0 ]; then
    echo "Could not replace values in template file." >&2 && exit $status
  fi

  #Send email with file attachment
  sendEmail -f ${SMTP_FROM} -t ${SMTP_TO} -bcc ${SMTP_BCC} -u ${SMTP_SUBJECT} -s ${SMTP_SERVER} -a ${COMPRESSED_RESULTS_FILE} -m "${content}" -o message-charset=utf8
  status=$?
  if [ ${status} -ne 0 ]; then
    echo "Could not send email." >&2 && exit ${status}
  fi
}

function remove_quotes() {
  temp="${1%\"}"
  temp="${temp#\"}"
  echo "$temp"
}
