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
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices ORDER BY last_seen DESC")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]