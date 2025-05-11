import can
import time
import json
import os
import threading
import signal
import sys

# Graceful shutdown flag
running = True

def handle_exit(sig, frame):
    global running
    print("\n[ECU2] Received interrupt signal. Shutting down gracefully.")
    running = False

signal.signal(signal.SIGINT, handle_exit)

# Load CAN signal definitions
json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'common', 'can_defs', 'signal_map.json')
with open(json_path, 'r') as f:
    signal_data = json.load(f)

# Filter only ECU2
ECU_NAME = "ECU2"
own_can_id = None
own_data = []
filter_ids = []

for signal in signal_data["signals"]:
    if signal["ECU_name"] == ECU_NAME:
        own_can_id = int(signal["can_id"], 16)
        filter_ids = [int(x, 16) for x in signal["Received_can_IDs"]]

if own_can_id is None:
    print("[ECU2] ECU2 not found in signal_map.json")
    sys.exit(1)

# Add CRC placeholder function
def compute_fake_crc(data):
    return sum(data) % 256  # Simple placeholder

# Setup CAN bus
bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=500000)
data_to_send = [0x07,0x00,0x00]
crc = compute_fake_crc(data_to_send)
data_to_send.append(crc)

# Enable if you donot want to see loopback
# bus.set_filters([{"can_id": fid, "can_mask": 0x7FF} for fid in filter_ids])

# Sender Thread
def sender_thread():
    while running:
        msg = can.Message(arbitration_id=own_can_id, data=data_to_send, is_extended_id=False)
        try:
            bus.send(msg)
            print(f"[ECU2][SEND] ID=0x{own_can_id:X}, Data={data_to_send}")
        except can.CanError as e:
            print(f"[ECU2][ERROR] Send failed: {e}")
        time.sleep(2)

# Receiver Thread
def receiver_thread():
    while running:
        try:
            msg = bus.recv(timeout=5)
            if msg is not None and msg.arbitration_id in filter_ids:
                print(f"[ECU2][RECV] ID=0x{msg.arbitration_id:X}, Data={list(msg.data)}")
            if msg is not None and msg.arbitration_id == own_can_id:
                print (f"[ECU2][LOOPBACK] ID=0x{msg.arbitration_id:X}, Data={list(msg.data)}")
        except can.CanError as e:
            print(f"[ECU2][ERROR] Receive failed: {e}")

# Start threads
sender = threading.Thread(target=sender_thread)
receiver = threading.Thread(target=receiver_thread)

print(f"[ECU2] Starting ECU2 CAN simulator with ID 0x{own_can_id:X}")
print(f"[ECU2] Listening to: {[hex(i) for i in filter_ids]}")
print(f"[ECU2] Sending every 2 seconds... Press Ctrl+C to stop.\n")

sender.start()
receiver.start()

# Wait for threads
try:
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    pass

sender.join()
receiver.join()
print("[ECU2] Simulator stopped.")
