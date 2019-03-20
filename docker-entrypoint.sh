#!/bin/bash

. /functions.sh
env > /.env

CRON_EXPRESSION="$(remove_quotes ${CRON_EXPRESSION} )"
echo "CRON_EXPRESSION=${CRON_EXPRESSION}"
#TODO: Validate cron expressoin
if [ ! -z "${CRON_EXPRESSION}" ]; then
  cat << EOF >> /etc/cron.d/network-tests
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

${CRON_EXPRESSION}  root  echo TEST >> /tmp/test.txt
EOF
fi

/usr/local/bin/supervisord -c /etc/supervisord.d/cron.ini
