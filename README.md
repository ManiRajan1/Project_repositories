## Docker based HIL testing

This branch provides a demonstration of simulating a CAN network for a HIL simulation using Docker images. 

Many embedded simulations rely on network interfaces. The Linux kernel treats CAN like a network layer, and to simulate it virtually, we need to load the corresponding driver module — in this case, vcan.

**modprobe vcan**: This loads the vcan kernel module, enabling a virtual CAN interface — similar to configuring a restbus simulation in CANoe, but done via kernel-space in Linux. The lower layers of simulation are handled by vcan

**ip link add dev vcan0 type vcan**: Sets up the simulated CAN channel (vcan0).

**cansend, candump**: Equivalent to CANoe generator and trace windows for sending and capturing frames.

This is basically like creating a minimal, scriptable CAN simulation testbench using only open-source tools and no licensing restrictions.