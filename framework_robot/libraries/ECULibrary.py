import time
import logging
from robot.api import logger
from udsoncan.client import Client
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.services import *

class ECULibrary:
    def __init__(self):
        self.conn = None
        self.client = None
        self.logger = logging.getLogger(__name__)

    def connect_to_ecu(self, tx_id=0x7E0, rx_id=0x7E8, interface="can0"):
        """Connect to ECU via UDS (Robot Keyword)"""
        try:
            self.conn = PythonIsoTpConnection(interface, rxid=rx_id, txid=tx_id)
            self.client = Client(self.conn)
            self.client.connect()
            logger.info(f"Connected to ECU (TX: 0x{tx_id:X}, RX: 0x{rx_id:X})")
            return True
        except Exception as e:
            logger.error(f"ECU connection failed: {str(e)}")
            raise

    def read_ecu_data(self, did="F190"):
        """Read ECU data by identifier (Robot Keyword)"""
        try:
            response = self.client.read_data_by_identifier(int(did, 16))
            result = response.data.hex()
            logger.info(f"Read DID 0x{did}: {result}")
            return result
        except Exception as e:
            logger.error(f"Read failed: {str(e)}")
            raise

    def flash_ecu(self, binary_path, checksum=None):
        """Flash ECU firmware (Robot Keyword)"""
        try:
            with open(binary_path, "rb") as f:
                firmware = f.read()
            
            self.client.enter_programming_session()
            self.client.request_download(len(firmware))
            self.client.transfer_data(firmware)
            
            if checksum:
                self.verify_checksum(checksum)
            
            self.client.exit_programming_session()
            logger.info("ECU flashed successfully")
            return True
        except Exception as e:
            logger.error(f"Flashing failed: {str(e)}")
            self.client.reset()
            raise

    def reset_ecu(self, mode="hard"):
        """Reset ECU (Robot Keyword)"""
        reset_modes = {
            "hard": 0x01,
            "soft": 0x03
        }
        try:
            self.client.ecu_reset(reset_modes[mode])
            logger.info(f"ECU {mode} reset executed")
            return True
        except Exception as e:
            logger.error(f"Reset failed: {str(e)}")
            raise

    def measure_boot_time(self, timeout=5):
        """Measure ECU boot time (Robot Keyword)"""
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            try:
                self.read_ecu_data("F189")  # Read ECU version
                boot_time = time.monotonic() - start
                logger.info(f"ECU boot time: {boot_time:.2f}s")
                return boot_time
            except:
                time.sleep(0.1)
        raise TimeoutError("ECU did not boot in time")