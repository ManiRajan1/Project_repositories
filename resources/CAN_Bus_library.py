from can import Message, Bus, CanError
from robot.api.deco import keyword  # <-- Essential for Robot keywords
from functools import wraps
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_connection(func):
    """Decorator to validate CAN bus connection"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.bus:
            raise ConnectionError("CAN bus not connected. Call 'connect_to_can' first.")
        return func(self, *args, **kwargs)
    return wrapper

class CanBusLibrary:
    def __init__(self):
        self.bus = None

    @keyword  # <-- Makes this a Robot Framework keyword
    def connect_to_can(self, channel="can0"):
        """Connect to CAN interface (Robot Keyword)"""
        try:
            self.bus = Bus(channel=channel, bustype='socketcan')
            logger.info(f"Connected to CAN channel {channel}")
            return "CAN Connected"
        except CanError as e:
            logger.error(f"CAN connection failed: {str(e)}")
            raise

    @keyword("Send CAN Message")  # <-- Custom keyword name
    @validate_connection
    def send_can_message(self, can_id, data):
        """Sends a CAN message with given ID and data (hex string)"""
        try:
            msg = Message(
                arbitration_id=int(can_id, 16),
                data=list(bytes.fromhex(data))
            )
            self.bus.send(msg)
            logger.debug(f"Sent CAN ID: 0x{can_id}, Data: {data}")
            return "Message Sent"
        except ValueError as e:
            logger.error(f"Invalid CAN ID/data format: {str(e)}")
            raise

    @keyword("Receive CAN Message")  # <-- Custom keyword name
    @validate_connection
    def receive_can_message(self, timeout=1.0):
        """Receives a CAN message within timeout (seconds)"""
        msg = self.bus.recv(timeout=timeout)
        if msg:
            result = f"ID: {hex(msg.arbitration_id)}, Data: {msg.data.hex()}"
            logger.debug(f"Received: {result}")
            return result
        logger.info("No message received within timeout")
        return "No message received"