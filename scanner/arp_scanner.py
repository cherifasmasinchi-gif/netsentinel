from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup

def scan(ip_range):
    """
    Sends ARP requests across the given IP range and returns
    a list of devices that responded, with their IP, MAC, and vendor.
    """
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered, unanswered = srp(packet, timeout=2, verbose=False)

    mac_lookup = MacLookup()

    devices = []
    for sent, received in answered:
        mac = received.hwsrc
        try:
            vendor = mac_lookup.lookup(mac)
        except Exception:
            vendor = "Unknown"

        devices.append({"ip": received.psrc, "mac": mac, "vendor": vendor})

    return devices


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from db.database import init_db, save_devices, is_new_device
    from scanner.port_scanner import scan_ports

    ip_range = "192.168.1.0/24"
    print(f"Scanning {ip_range} ...")
    found_devices = scan(ip_range)

    print(f"\nFound {len(found_devices)} device(s):\n")

    init_db()

    for device in found_devices:
        print(f"{device['ip']:<18}{device['mac']:<20}{device['vendor']}")
        if is_new_device(device["mac"]):
            print(f"   ⚠️  NEW DEVICE DETECTED!")

        open_ports = scan_ports(device["ip"])
        if open_ports:
            print(f"   Open ports: {open_ports}")
        else:
            print(f"   No common open ports found.")
        print()

    save_devices(found_devices)
    print("✅ Devices saved to database.")