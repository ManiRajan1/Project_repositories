import can
import signal
import subprocess
import time

def handle_exit(sig,frame):
    global running
    print ("Communication shutting gracefully")
    running = False
    time.sleep(5)
    subprocess.run(["sudo","ip","link","delete","vcan0"])
    subprocess.run(["sudo","modprobe","-r","vcan"])



signal.signal(signal.SIGINT, handle_exit)

class MockECU:
    def __init__(self, rx_id=0x7E0, tx_id=0x7E8, interface='socketcan', channel='vcan0'):
        self.txid=tx_id
        self.rxid=rx_id
        self.bus = can.Bus(interface=interface, channel=channel)

    def handle_uds_request(self, request):
        """Process UDS requests and return responses"""
        if request[0] == 0x22:  # ReadDataByIdentifier
            did = bytes(request[1:4])
            if did == b'\xF1\x90':  # VIN request
                return b'\x62\xF1\x90\x43'  # Positive response
            else:
                return b'\x7F\x22\x31'  # Negative response (DID not supported)
        elif bytes(request[0:2]) == b'\x11\x01':  # ECUReset
            return b'\x51\x01'  # Hard reset response
        else:
            return b'\x7F\x11'  # Service not supported

    def run(self):
        """Main loop to listen and respond to requests"""
        msg = self.bus.recv(timeout=1)
        if msg:
            print (f"Message received with Id: 0x{msg.arbitration_id:x}")
            if msg.arbitration_id == self.rxid:
                response = self.handle_uds_request(msg.data)
                self.bus.send(can.Message(
                arbitration_id=self.txid,
                data=response
            ))

if __name__ == "__main__":
    running = True
    subprocess.run(["sudo","modprobe","vcan"])
    subprocess.run(["sudo","ip","link","add","dev","vcan0", "type", "vcan"])
    subprocess.run(["sudo","ip","link","set","up","vcan0"])
    ecu = MockECU(rx_id=0x7E0, tx_id=0x7E8)
    print("Mock ECU running (Ctrl+C to stop)")
    while (running):
        ecu.run()
