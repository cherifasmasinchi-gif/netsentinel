import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.database import init_db, is_new_device, save_devices, DB_PATH
import sqlite3

TEST_MAC = "aa:bb:cc:dd:ee:ff"


def _remove_test_device():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM devices WHERE mac = ?", (TEST_MAC,))
    conn.commit()
    conn.close()


def test_new_device_is_detected():
    init_db()
    _remove_test_device()  # ensure a clean slate before checking
    result_before = is_new_device(TEST_MAC)
    assert result_before is True


def test_known_device_is_not_new():
    init_db()
    save_devices([{"ip": "192.168.1.99", "mac": TEST_MAC, "vendor": "Test Vendor"}])
    result_after = is_new_device(TEST_MAC)
    assert result_after is False
    _remove_test_device()  # clean up after this test too

