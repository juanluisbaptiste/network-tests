#!/bin/bash
TEST_COUNT=${TEST_COUNT:-1} \
THROTTLE_ENABLE=yes \
THROTTLE_UP_SPEED=1000 \
THROTTLE_DOWN_SPEED=2000 \
THROTTLE_RTT=1 \
DOWNLOAD_TEST_ENABLE=yes \
DOWNLOAD_TEST_COUNT=${TEST_COUNT} \
UPLOAD_TEST_ENABLE=yes \
UPLOAD_TEST_COUNT=${TEST_COUNT} \
UPLOAD_TEST_HOST=maeztro.synology.me \
UPLOAD_TEST_USER=jbaptiste \
UPLOAD_TEST_PASSWORD=l0wn01s3 \
UPLOAD_TEST_PASSIVE=yes \
SILENT_TEST=no \
PING_TEST_ENABLE=yes \
PING_TEST_COUNT=${TEST_COUNT} \
./docker-entrypoint.sh
