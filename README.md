[README (1).md](https://github.com/user-attachments/files/30427117/README.1.md)
# NetSentinel

A Python tool that scans your local network, discovers connected devices, identifies their manufacturer, checks for risky open ports, tracks changes over time, and displays everything on a simple web dashboard.

## Why this exists

Most home networks run "blind" — you don't really know what's connected, which ports are open, or whether a new/unknown device just joined. NetSentinel gives you visibility into your own network so you can catch things like:

- An unrecognized device connecting to your Wi-Fi
- A service exposing an insecure port (e.g. Telnet, RDP)
- Devices you forgot about that are still sitting on your network

**What NetSentinel is NOT:** it is not a firewall, antivirus, or intrusion prevention system. It does not stop attacks — it detects and reports. Think of it as a visibility and early-warning tool, not a full security suite.

> ⚠️ **Only scan networks and devices you own or have explicit permission to scan.**

## Features

- 🔍 **Device discovery** — ARP-based scan finds every live device on your LAN (IP, MAC)
- 🏷️ **Vendor lookup** — identifies each device's manufacturer from its MAC address
- 🔌 **Port scanning** — multi-threaded TCP scan of common ports, with banner grabbing
- ⚠️ **Risk scoring** — flags risky/insecure ports (e.g. Telnet, RDP = HIGH risk) with plain-English explanations
- 🕓 **History tracking** — SQLite-backed history detects new devices between scans
- 📊 **Web dashboard** — Flask UI with color-coded risk badges (🟢🟡🔴) and a "Scan Now" button
- 🔔 **Console alerts** — flags new devices and high-risk ports directly in the terminal when scanning
- ✅ **Tested** — core risk-scoring and device-detection logic covered by unit tests (pytest)

## Tech stack

- Python 3
- [Scapy](https://scapy.net/) — ARP scanning
- [mac-vendor-lookup](https://pypi.org/project/mac-vendor-lookup/) — manufacturer identification
- [Flask](https://flask.palletsprojects.com/) — web dashboard
- SQLite — device and port scan history
- `socket` + `concurrent.futures` (standard library) — multi-threaded port scanning
- `pytest` — unit testing

## Installation

```bash
git clone https://github.com/<your-username>/netsentinel.git
cd netsentinel

python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

> **Note (Windows):** you may need to allow local scripts to run once with:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

## Usage

**Run a scan from the command line:**
```bash
python scanner\arp_scanner.py
```
This discovers devices, looks up vendors, scans common ports, scores risk, flags new devices, and saves everything to `netsentinel.db`.

**Launch the web dashboard:**
```bash
python dashboard\app.py
```
Then open `http://127.0.0.1:5000` in your browser. Click **"🔄 Scan Now"** to trigger a fresh scan directly from the dashboard.

## Running tests

```bash
pytest
```

## Screenshots

*(Add a screenshot of the dashboard here, showing the device table with risk badges)*

## Roadmap / Status

- [x] Project setup
- [x] ARP-based device discovery
- [x] Vendor lookup
- [x] SQLite storage
- [x] New device detection
- [x] Port scanner + banner grabbing
- [x] Risk scoring
- [x] Flask dashboard with risk badges + scan button
- [x] Console alerts (new devices / high-risk ports)
- [x] Unit tests
- [ ] HTML/PDF report export (not implemented — scoped out to focus on core features)

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Disclaimer

NetSentinel is intended for auditing networks and devices you own or are authorized to test. The author is not responsible for misuse of this tool.
