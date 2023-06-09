from serial.tools.list_ports import comports
import sys



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


    def display_available_port(self):
        idx = 1
        for port in comports():
            print(idx, ")", port)
            idx += 1

    def gen_port_list(self):
        for port in comports():
            print(port)
    
    


if __name__ == "__main__":
    A = scanner()
    A.gen_port_list()