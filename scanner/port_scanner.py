import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 8080]

# Risk info for common ports: (risk_level, reason)
RISK_RULES = {
    21:   ("MEDIUM", "FTP — often unencrypted file transfer"),
    22:   ("LOW", "SSH — encrypted remote login, generally safe if configured well"),
    23:   ("HIGH", "Telnet — unencrypted remote login, avoid if possible"),
    25:   ("LOW", "SMTP — mail transfer"),
    53:   ("LOW", "DNS — normal for routers/DNS servers"),
    80:   ("LOW", "HTTP — standard unencrypted web traffic"),
    110:  ("MEDIUM", "POP3 — often unencrypted email retrieval"),
    143:  ("MEDIUM", "IMAP — often unencrypted email access"),
    443:  ("LOW", "HTTPS — standard encrypted web traffic"),
    3389: ("HIGH", "RDP — remote desktop, common attack target if exposed"),
    8080: ("MEDIUM", "Alternate HTTP — often a dev/admin interface"),
}


def grab_banner(sock):
    """
    Tries to read a short banner message from an already-open socket.
    Returns the banner text, or an empty string if nothing was received.
    """
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner
    except Exception:
        return ""


def check_port(ip, port, timeout=1):
    """
    Tries to connect to a single port. If open, also attempts to grab
    a banner and looks up its risk info.
    Returns a dict if open, or None if closed.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                banner = grab_banner(sock)
                risk_level, reason = RISK_RULES.get(port, ("UNKNOWN", "No info available"))
                return {
                    "port": port,
                    "banner": banner,
                    "risk_level": risk_level,
                    "reason": reason,
                }
    except Exception:
        pass
    return None


def scan_ports(ip):
    """
    Checks all COMMON_PORTS on a given IP. Returns a list of dicts
    for every open port found (with banner + risk info).
    """
    open_ports = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(lambda port: check_port(ip, port), COMMON_PORTS)

    for result in results:
        if result is not None:
            open_ports.append(result)

    return open_ports


if __name__ == "__main__":
    test_ip = "192.168.1.1"
    print(f"Scanning ports on {test_ip} ...")
    ports = scan_ports(test_ip)

    if ports:
        for p in ports:
            print(f"Port {p['port']:<6} Risk: {p['risk_level']:<8} {p['reason']}")
            if p["banner"]:
                print(f"   Banner: {p['banner']}")
    else:
        print("No common open ports found.")