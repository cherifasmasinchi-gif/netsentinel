from flask import Flask, render_template, redirect, url_for
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db.database import get_all_devices, init_db, save_devices, is_new_device, save_port_scan
from scanner.arp_scanner import scan
from scanner.port_scanner import scan_ports

app = Flask(__name__)

IP_RANGE = "192.168.1.0/24"


@app.route("/")
def index():
    devices = get_all_devices()
    return render_template("index.html", devices=devices)


@app.route("/scan", methods=["POST"])
def run_scan():
    init_db()
    found_devices = scan(IP_RANGE)

    for device in found_devices:
        if is_new_device(device["mac"]):
            print(f"⚠️  NEW DEVICE DETECTED: {device['ip']} ({device['mac']})")

        open_ports = scan_ports(device["ip"])

        high_risk_ports = [p for p in open_ports if p["risk_level"] == "HIGH"]
        if high_risk_ports:
            print(f"🚨 HIGH RISK on {device['ip']}: {[p['port'] for p in high_risk_ports]}")

        save_port_scan(device["mac"], open_ports)

    save_devices(found_devices)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

    