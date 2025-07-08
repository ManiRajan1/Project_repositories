set -x

sudo ip link delete vcan0
sudo modprobe -r vcan
lsmod | grep vcan