import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.database import init_db, is_new_device, save_devices

TEST_MAC = "aa:bb:cc:dd:ee:ff"


def test_new_device_is_detected():
    init_db()
    # Make sure this test MAC isn't already saved from a previous run
    result_before = is_new_device(TEST_MAC)
    assert result_before is True


def test_known_device_is_not_new():
    init_db()
    save_devices([{"ip": "192.168.1.99", "mac": TEST_MAC, "vendor": "Test Vendor"}])
    result_after = is_new_device(TEST_MAC)
    assert result_after is False