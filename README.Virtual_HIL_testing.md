## Virtual based HIL testing

This branch provides a demonstration of simulating a CAN network for a HIL simulation using Docker images. This is purely a virtual HIL simulation.

Many embedded simulations rely on network interfaces. The Linux kernel treats CAN like a network layer, and to simulate it virtually, we need to load the corresponding driver module — in this case, vcan.

**modprobe vcan**: This loads the vcan kernel module, enabling a virtual CAN interface — similar to configuring a restbus simulation in CANoe, but done via kernel-space in Linux. The lower layers of simulation are handled by vcan

**ip link add dev vcan0 type vcan**: Sets up the simulated CAN channel (vcan0).

**cansend, candump**: Equivalent to CANoe generator and trace windows for sending and capturing frames.

This is basically like creating a minimal, scriptable CAN simulation testbench using only open-source tools and no licensing restrictions.

The code repository of interest can be viewed by [Docker based HIL testing](https://github.com/ManiRajan1/Project_repositories/tree/Docker_based_HIL_testing)

In order to run the PoC, run the following commands on git bash

**Pre-requisities**
+ Docker-compose
+ Checks on bash
  ```bash
  sudo apt update
  sudo apt install can-utils
  sudo apt install iproute2   # in case it's missing
  ```
+ Once installed, run the check below
  ```bash
  sudo modprobe   # ✅ should work without extra installs
  sudo ip link add dev vcan0 type vcan
  sudo ip link set up vcan0
  candump vcan0   # starts logging
  cansend vcan0 123#0FF0F00F  # sends a frame
  ```
**Getting started**

Once the above checks are successful, you can clone and use the repo as below

``` bash
#!/bin/bash
git clone https://github.com/ManiRajan1/Project_repositories.git
cd Project_repositories/
git fetch origin Docker_based_HIL_testing:Docker_based_HIL_testing
git checkout Docker_based_HIL_testing
docker-compose up
``` 

*_Note : For ease of implementing this proof of concept (PoC), Docker containers are run in privileged mode. This allows direct access to the host's networking stack and kernel modules, enabling setup and communication over the virtual CAN interface (vcan0), which is managed by the Linux kernel_*
