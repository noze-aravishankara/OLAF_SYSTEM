from serial.tools.list_ports import comports
from NOZE_SENSOR.IDENTIFIER import IDENTIFIER
import sys
import logging

logging.basicConfig(level=logging.INFO)


class scanner:
    def __init__(self):
        self.operating_system = self.get_os()

    def get_os(self):
        if sys.platform.startswith('win'):
            return "Windows"
        elif sys.platform.startswith('darwin'):
            return "Mac"
        elif sys.platform.startswith('linux'):
            return "Linux"
        else:
            return "Unknown"

    def gen_port_list(self):
        return [str(port) for port in comports()]

    def gen_port_dict(self):
        self.devices = {}
        self.ns_idx = 0
        self.mfc_idx = 0
        self.teensy_idx = 0

        self.port_list = self.gen_port_list()
        logging.debug(self.port_list)

        for port in self.port_list:
            _ = port.split()
            logging.debug(_)
            match _[2]:
                case 'CP2102':
                    logging.debug(f"Device at port {_[0]} is a Noze Sensor.")
                    ident = IDENTIFIER(_[0])
                    version = ident.get_version()
                    sn = ident.get_sn()
                    baudrate = ident.get_baudrate()
                    self.add_noze_device(_[0], baudrate, version, sn)
                case 'USB-RS485':
                    logging.debug(f"Device at port {_[0]} is an MFC.")
                    self.add_mfc_device(_[0], '435', 'N2')
                case 'USB':
                    logging.debug((f"Device at port {_[0]} is a teensy."))
                    self.add_teensy_device(_[0], 115200)
                case _:
                    logging.warn(f"Device at port {_[0]} is unknown.")

        return self.devices

    def add_noze_device(self, port, baudrate, version, sn):
        self.devices[f'NS-{self.ns_idx}'] = {'port': port, 'baudrate': baudrate, 'version': version, 'sn': sn}
        self.ns_idx = self.ns_idx + 1
        logging.info(f'Added Noze Sensor version {version} on port {port} with serial number {sn}')

    def add_mfc_device(self, port, sn, gas):
        self.devices[f'MFC-{self.mfc_idx}'] = {'port': port, 'baudrate': 115200, 'sn': sn, 'gas': gas}
        self.mfc_idx = self.mfc_idx + 1
        logging.info(f'Added a new MFC on port {port} with serial number {sn} with gas {gas}')

    def add_teensy_device(self, port, baudrate):
        self.devices[f'TEENSY-{self.teensy_idx}'] = {'port': port, 'baudrate': 115200}
        self.teensy_idx = self.teensy_idx + 1
        logging.info(f'Added a new Teensy on port {port}.')


if __name__ == "__main__":
    A = scanner()
    A.gen_port_dict()
    print(A.devices)