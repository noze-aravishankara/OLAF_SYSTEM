from system_scanner.scanner import scanner


if __name__ == "__main__":
    A = scanner()
    A.gen_port_dict()
    print(A.devices)