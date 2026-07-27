import sqlite3
from datetime import datetime

DB_PATH = "netsentinel.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            mac TEXT NOT NULL UNIQUE,
            vendor TEXT,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_mac TEXT NOT NULL,
            port INTEGER NOT NULL,
            risk_level TEXT,
            reason TEXT,
            scanned_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_devices(devices):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    for device in devices:
        cursor.execute("SELECT id FROM devices WHERE mac = ?", (device["mac"],))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE devices
                SET ip = ?, vendor = ?, last_seen = ?
                WHERE mac = ?
            """, (device["ip"], device["vendor"], now, device["mac"]))
        else:
            cursor.execute("""
                INSERT INTO devices (ip, mac, vendor, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?)
            """, (device["ip"], device["mac"], device["vendor"], now, now))

    conn.commit()
    conn.close()


def get_all_devices():
    """
    Returns every device, along with its highest risk level found
    among its open ports (or 'NONE' if no risky ports are open).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices ORDER BY last_seen DESC")
    devices = [dict(row) for row in cursor.fetchall()]

    for device in devices:
        cursor.execute("""
            SELECT risk_level FROM ports WHERE device_mac = ?
        """, (device["mac"],))
        risk_levels = [row["risk_level"] for row in cursor.fetchall()]

        if "HIGH" in risk_levels:
            device["risk"] = "HIGH"
        elif "MEDIUM" in risk_levels:
            device["risk"] = "MEDIUM"
        elif risk_levels:
            device["risk"] = "LOW"
        else:
            device["risk"] = "NONE"

    conn.close()
    return devices

def is_new_device(mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM devices WHERE mac = ?", (mac,))
    existing = cursor.fetchone()

    conn.close()
    return existing is None
def save_port_scan(mac, open_ports):
    """
    Saves the open ports found for a device into the ports table.
    Clears out old entries for this device first, so we always
    reflect the most recent scan.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    # Remove old port records for this device before adding fresh ones
    cursor.execute("DELETE FROM ports WHERE device_mac = ?", (mac,))

    for p in open_ports:
        cursor.execute("""
            INSERT INTO ports (device_mac, port, risk_level, reason, scanned_at)
            VALUES (?, ?, ?, ?, ?)
        """, (mac, p["port"], p["risk_level"], p["reason"], now))

    conn.commit()
    conn.close()