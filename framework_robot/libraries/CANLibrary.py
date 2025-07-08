import can
import logging
from robot.api import logger
from functools import wraps

class CANLibrary:
    def __init__(self):
        self.bus = None
        self.logger = logging.getLogger(__name__)

    def connect_to_can(self, channel="can0", bustype="socketcan"):
        """Connect to CAN bus (Robot Keyword)"""
        try:
            self.bus = can.interface.Bus(channel=channel, bustype=bustype)
            logger.info(f"Connected to CAN bus {channel}")
            return True
        except can.CanError as e:
            logger.error(f"CAN connection failed: {str(e)}")
            raise

    def send_can_message(self, can_id, data, is_extended=False):
        """Send a CAN message (Robot Keyword)"""
        try:
            msg = can.Message(
                arbitration_id=int(can_id, 16) if isinstance(can_id, str) else can_id,
                data=list(bytes.fromhex(data)) if isinstance(data, str) else data,
                is_extended_id=is_extended
            )
            self.bus.send(msg)
            logger.info(f"Sent CAN ID: 0x{msg.arbitration_id:X}, Data: {msg.data.hex()}")
            return True
        except (ValueError, can.CanError) as e:
            logger.error(f"Failed to send CAN message: {str(e)}")
            raise

    def receive_can_message(self, timeout=1.0):
        """Receive a CAN message (Robot Keyword)"""
        try:
            msg = self.bus.recv(timeout=timeout)
            if msg:
                result = f"ID: 0x{msg.arbitration_id:X}, Data: {msg.data.hex()}"
                logger.info(f"Received: {result}")
                return result
            logger.warn("No message received")
            return None
        except can.CanError as e:
            logger.error(f"CAN receive error: {str(e)}")
            raise

    def inject_can_error(self, error_type="bit_flip", can_id=None):
        """Inject CAN errors (Robot Keyword)"""
        error_types = {
            "bit_flip": lambda: [0xFF, 0xFF, 0xFF],  # Stuffed bits
            "format": lambda: [0x00] * 16  # Overlength frame
        }
        if error_type not in error_types:
            raise ValueError(f"Invalid error type: {error_type}")
        
        error_data = error_types[error_type]()
        self.send_can_message(can_id or 0x000, error_data)
        logger.info(f"Injected {error_type} error")

    def log_can_traffic(self, duration=10, output_file="can_log.blf"):
        """Log CAN traffic to a file (Robot Keyword)"""
        try:
            with can.BLFWriter(output_file) as writer:
                for _ in range(int(duration * 10)):
                    msg = self.bus.recv(0.1)
                    if msg:
                        writer.on_message_received(msg)
            logger.info(f"Logged CAN traffic to {output_file}")
        except Exception as e:
            logger.error(f"Logging failed: {str(e)}")
            raise