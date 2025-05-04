#!/bin/bash
apt update && DEBIAN_FRONTEND=noninteractive apt install -y iproute2 can-utils kmod 
modprobe vcan
if ! ip link show vcan0 > /dev/null 2>&1; then
    echo "Creating virtual CAN interface vcan0..."
    ip link add dev vcan0 type vcan
else
    echo "Virtual CAN interface vcan0 already exists."
fi

ip link set up vcan0
echo "[INFO] vcan0 is up. Waiting 3s before sending CAN message..."
sleep 3
cansend vcan0 123#0000CC00
echo "[INFO] CAN message sent to vcan0."
sleep 3
cansend vcan0 125#FFFF0000
