#!/usr/bin/env bash
set -eu

mosquitto -v -c /etc/mosquitto/mosquitto.conf &

python3 /root/src/a9-v720/src/a9_naxclow.py --server &

exec "$@"