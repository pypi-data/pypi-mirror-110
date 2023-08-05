#!/bin/bash

# we first need to wait for PostgreSQL
# cf. https://stackoverflow.com/a/39028690 (thanks!)

RETRIES=5

until psql -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts…"
  sleep 1
done

ori_dir=${PWD}
cd /src/sat_pubsub/db

# PG should be OK, we now initialize the database. If it's already done, it will fail
# with exit code 3
psql -v ON_ERROR_STOP=1 pubsub < pubsub.sql 2>/dev/null
case $? in
    0) printf "database initialized\n" ;;
    3) printf "database already exists\n" ;;
    *) printf "can't initialize database, please check PostgreSQL container parameters\n" >&2
       exit 1
       ;;
esac

cd $ori_dir

exec /home/libervia/libervia_env/bin/twistd -n libervia-pubsub "$@"
