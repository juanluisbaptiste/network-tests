#!/bin/bash

. /functions.sh
env > /.env

CRON_EXPRESSION="$(remove_quotes "${CRON_EXPRESSION}" )"
echo "Configuring automated tests to be run at: ${CRON_EXPRESSION}"

#TODO: Validate cron expressoin
if [ ! -z "${CRON_EXPRESSION}" ]; then
  cat << EOF >> /etc/cron.d/network-tests
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

${CRON_EXPRESSION}  root  /run_test.sh 2>&1 | logger
EOF
fi

/usr/local/bin/supervisord -c /etc/supervisord.d/supervisord.ini
