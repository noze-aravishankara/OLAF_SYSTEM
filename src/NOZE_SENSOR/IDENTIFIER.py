import threading
import logging
import serial
import json
import sys
import time

logging.basicConfig(level=logging.INFO)


class IDENTIFIER:
    def __init__(self, port):
        self.port = port
        self.sn = None
        # self.test_baudrates = [9600, 115200]
        self.sn = self.connect_to_v2()
        if self.sn is None:
            logging.debug(f"This is not a V2 board. Trying with V1")
            self.sn = self.connect_to_v1()
            self.version = 'V1'
            self.baudrate = 9600
            logging.info(f"This is a V1 board with Serial Number: {self.sn}")
        else:
            logging.info(f"This is a V2 board with Serial Number: {self.sn}")
            self.version = 'V2'
            self.baudrate = 115200
            
    def get_baudrate(self):
        return self.baudrate

    def get_sn(self):
        return self.sn
    
    def get_version(self):
        return self.version
    
    def connect_to_v2(self):
        sn = None
        sensor = connect_to_v2_sensor(self.port)
        for i in range(3):
            try:
                _ = sensor.get_serial_number()
                if _ is not None:
                    logging.debug(f"Got serial number {_}")
                    sn = _
                    break
                else:
                    logging.debug(f"Trying for round {i}")
            except serial.SerialException as e:
                logging.debug(f'Serial error: {e}')
                break
        return sn
    
    def connect_to_v1(self):
        sn = None
        sensor = connect_to_v1_sensor(self.port)
        for i in range(3):
            try:
                _ = sensor.get_serial_number()
                if _ is not None:
                    logging.debug(f"Got Serial Number: {_}")
                    sn = _
                    break
                else:
                    logging.debug(f"Trying for round {i}")
            except serial.SerialException as e:
                logging.debug(f"Serial Connection Error: {e}")
                break
        return sn


class connect_to_v1_sensor:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate

        try:
            self.sensor = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        except serial.SerialException as e:
            logging.error(f"Serial Connection for 9600 went wrong: {e}")
        self.flush_serial()

    def flush_serial(self):
        self.sensor.flush()
        logging.debug("C1V1: Flushed Serial Line")

    def read_sensor_data(self):
        try:
            _ = ''
            #while len(_) < 200:
            _ = self.sensor.readline().decode("utf-8").strip()
            _ = _.replace("\n", "")
            _ = _.split("\t")
            #    time.sleep(0.5)

            logging.debug(f"C1v1: Sensor Data: {_}")
            # _ = _.replace("\n", "")
            # _ = _.replace("\r", "")
            # _ = _.replace('\x00', '')
            # _ = json.loads(_)
            
            return _
        
        except serial.SerialTimeoutException as e:
            logging.error(f"Timeout exception: {e}")
            return None
        
        except json.decoder.JSONDecodeError as e:
            logging.debug(f"Json Error: Could not read board: {e}")

    def get_serial_number(self):
        _ = self.read_sensor_data()
        if _ is not None:
            self.sn = _[-1]
            logging.debug(f'Sensor serial number is: {self.sn}')
            return self.sn
        else:
            return None
        
    def __del__(self):
        self.sensor.close()


class connect_to_v2_sensor:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate

        self.sensor = serial.Serial(port=self.port,baudrate=self.baudrate, timeout=0.5)
        self.flush_serial()

    def flush_serial(self):
        self.sensor.flush()
        logging.debug("C2V2: Flushed Serial Line")

    def read_sensor_data(self):
        try:
            _ = self.sensor.read_until("\n").decode().strip()
            logging.debug(f"C2V2: Sensor Data: {_}")
            _ = _.replace("\n", "")
            _ = _.replace("\r", "")
            _ = _.replace('\x00', '')
            _ = json.loads(_)
            
            return _
        
        except serial.SerialTimeoutException as e:
            logging.error(f"Timeout exception: {e}")
            return None
        
        except json.decoder.JSONDecodeError as e:
            logging.debug(f"Json Error: Could not read board: {e}")
        
    def get_serial_number(self):
        _ = self.read_sensor_data()
        if _ is not None:
            self.sn = _["sn"]
            logging.debug(f'Sensor serial number is: {self.sn}')
            return self.sn
        else:
            return None

    def __del__(self):
        self.sensor.close()



if __name__ == "__main__":
    id = IDENTIFIER('/dev/ttyUSB1')