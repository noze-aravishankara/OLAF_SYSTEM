import threading
import logging
import serial
import json
import sys
import time

logging.basicConfig(level=logging.DEBUG)


class IDENTIFER:
    def __init__(self, port):
        self.port = port
        self.sn = None

        if self.test_for_version(9600):
            logging.debug("Version 1 detected.")
            # Process version 1 data here
        elif self.test_for_version(115200):
            logging.debug("Version 2 detected.")
            # Process version 2 data here
        else:
            logging.info("Failed to identify the device within the timeout.")

    def connection_check(self, baudrate):
        try:
            sensor = serial.Serial(port=self.port, baudrate=baudrate, timeout=0.5)
            return sensor
        except serial.SerialException as e:
            logging.warn(f'Could not connect to device at {self.port}.')
            return None
        except Exception as e:
            logging.info(f'Error: {e}')
            return None
    
    def test_for_version(self, baudrate):
        _sensor = self.connection_check(baudrate=baudrate)
        if _sensor is not None:
            logging.debug(f"Sensor connects at baudrate: {baudrate}")
            _ = self.get_data(_sensor)
            logging.debug(f'Data check with baudrate: {baudrate}: {_}')
        _sensor.close()
            
    def flush_line(self, sensor):
        sensor.flush()
        logging.debug("Flushed the line")

    def get_data(self, sensor):
        try:
            self.flush_line(sensor)
            # if sensor.in_waiting > 0:
            #     sensor.readline()

            _ = sensor.read_until("\n").decode().strip()
            return _
        except Exception as e:
            logging.info(f"Error reading values with error: {e}")
            return None
        
        
    def get_sn(self, sensor, baudrate):
        try:
            self.sensor.reset_input_buffer()  # Clear any existing data in input buffer
            _ = self.sensor.readline().decode().strip()
            if not _:
                logging.info("No data received within the timeout.")
                return False

            _ = _.replace("\n", "")
            _ = _.replace("\r", "")
            _ = _.replace('\x00', '')
            _ = json.loads(_)
            logging.debug(_)
            self.sn = _["sn"]
            logging.debug(f"Serial Number is {self.sn}")
            return True
        except json.decoder.JSONDecodeError as e:
            logging.info(f"Error deserializing with error: {e}")
            return False
        except Exception as e:
            logging.info(f"Error reading values with error: {e}")
            return False


class connect_to_v2_sensor:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate

        self.sensor = serial.Serial(port=self.port,baudrate=self.baudrate, timeout=0.5)

    def flush_serial(self):
        self.sensor.flush()
        logging.debug("C2V2: Flushed Serial Line")

    def read_sensor_data(self):
        _ = self.sensor.readline().decode().strip()
        logging.debug(f"C2V2: Sensor Data: {_}")

    def __del__(self):
        self.sensor.close()


if __name__ == "__main__":
    identifier = IDENTIFER('/dev/ttyUSB0')
    # if identifier.sn:
    #     print(f"Sensor Serial Number: {identifier.sn}")