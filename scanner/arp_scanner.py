from scapy.all import ARP, Ether, srp

def scan(ip_range):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered, unanswered = srp(packet, timeout=2, verbose=False)

    devices = []
    for sent, received in answered:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


if __name__ == "__main__":
    ip_range = "192.168.1.0/24"
    print(f"Scanning {ip_range} ...")
    found_devices = scan(ip_range)

    print(f"\nFound {len(found_devices)} device(s):\n")
    print(f"{'IP Address':<20}{'MAC Address'}")
    print("-" * 40)
    for device in found_devices:
        print(f"{device['ip']:<20}{device['mac']}")

