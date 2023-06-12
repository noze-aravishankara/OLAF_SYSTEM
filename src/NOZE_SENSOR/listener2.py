import serial
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class Sensor:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=2)
            data = ser.readline().decode().strip()
            ser.close()
            return data
        except serial.SerialException:
            return None

    def get_serial_number(self):
        data = self.connect()

        if data and data.startswith("10000"):
            serial_number = data.split()[-1]
            logging.info("Sensor 1 detected. Serial number: %s", serial_number)
            return serial_number

        if data and data.startswith('{"sn":"') and data.endswith('"}'):
            serial_number = data.split('"sn":"')[1].split('","')[0]
            logging.info("Sensor 2 detected. Serial number: %s", serial_number)
            return serial_number

        logging.info("No compatible sensor detected.")
        return None


def auto_detect_sensor_serial_number():
    sensors = [
        Sensor("/dev/ttyUSB0", 9600),
        Sensor("/dev/ttyUSB1", 115200),
        Sensor("COM1", 9600),
        Sensor("COM2", 115200)
    ]

    for sensor in sensors:
        logging.info("Checking port: %s", sensor.port)
        serial_number = sensor.get_serial_number()
        if serial_number:
            return serial_number

    logging.info("No compatible sensor detected.")
    return None

# Auto-detect the sensor serial number
sensor_serial_number = auto_detect_sensor_serial_number()

if sensor_serial_number:
    logging.info("Sensor connected. Serial number: %s", sensor_serial_number)
else:
    logging.info("No compatible sensor connected.")
