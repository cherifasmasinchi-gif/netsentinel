import socket
from concurrent.futures import ThreadPoolExecutor

# A short list of common ports worth checking
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 8080]


def check_port(ip, port, timeout=1):
    """
    Tries to connect to a single port on a device.
    Returns the port number if open, otherwise None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))  # returns 0 if the port is open
            if result == 0:
                return port
    except Exception:
        pass
    return None


def scan_ports(ip):
    """
    Checks all COMMON_PORTS on a given IP address, using multiple
    threads at once for speed. Returns a list of open ports.
    """
    open_ports = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(lambda port: check_port(ip, port), COMMON_PORTS)

    for result in results:
        if result is not None:
            open_ports.append(result)

    return open_ports


if __name__ == "__main__":
    test_ip = "192.168.1.1"  # your router, as a test
    print(f"Scanning ports on {test_ip} ...")
    ports = scan_ports(test_ip)

    if ports:
        print(f"Open ports: {ports}")
    else:
        print("No common open ports found.")