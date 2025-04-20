#!/bin/bash
apt update && DEBIAN_FRONTEND=noninteractive apt install -y iproute2 can-utils
modprobe vcan
attempts=0
while ! ip link show vcan0 > /dev/null 2>&1 && [ $attempts -lt 5 ]; do
    echo "[INFO] Waiting for vcan0 to be available... attempt $((attempts+1))"
    sleep 1
    attempts=$((attempts + 1))
done

if ip link show vcan0 > /dev/null 2>&1; then
    echo "[INFO] vcan0 is available. Starting CAN logger (polling mode)."
    ip link set up vcan0 || true
    echo "[INFO] Listening for messages on vcan0..."
    while true; do
        candump vcan0 -L >> /logs/can_output.log
        sleep 1
    done
else
    echo "[ERROR] vcan0 not found after 5 attempts. Exiting."
    exit 1
fi