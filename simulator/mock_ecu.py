import can
import isotp

class MockECU:
    def __init__(self, rx_id=0x7E0, tx_id=0x7E8, interface='socketcan', channel='vcan0'):
        self.txid=tx_id
        self.rxid=rx_id
        self.bus = can.Bus(interface=interface, channel=channel)

    def handle_uds_request(self, request):
        """Process UDS requests and return responses"""
        if request[0] == 0x22:  # ReadDataByIdentifier
            did = request[2:4]
            if did == b'\xF1\x90':  # VIN request
                return b'\x62\xF1\x90MYTESTVIN123'  # Positive response
            else:
                return b'\x7F\x22\x31'  # Negative response (DID not supported)
        elif request[0] == 0x11:  # ECUReset
            return b'\x51\x01'  # Hard reset response
        else:
            return b'\x7F\x11'  # Service not supported

    def run(self):
        """Main loop to listen and respond to requests"""
        while True:
            msg = self.bus.recv()
            print (f"Message received:\n Id: 0x{msg.arbitration_id:x}\n")
            if msg and msg.arbitration_id == self.rxid:
                response = self.handle_uds_request(msg.data)
                self.bus.send(can.Message(
                    arbitration_id=self.txid,
                    data=response
                ))

if __name__ == "__main__":
    ecu = MockECU(rx_id=0x7E0, tx_id=0x7E8)
    print("Mock ECU running (Ctrl+C to stop)")
    ecu.run()