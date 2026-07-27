from scanner.port_scanner import RISK_RULES


def test_telnet_is_high_risk():
    risk_level, reason = RISK_RULES[23]
    assert risk_level == "HIGH"


def test_https_is_low_risk():
    risk_level, reason = RISK_RULES[443]
    assert risk_level == "LOW"


def test_ftp_is_medium_risk():
    risk_level, reason = RISK_RULES[21]
    assert risk_level == "MEDIUM"


def test_rdp_is_high_risk():
    risk_level, reason = RISK_RULES[3389]
    assert risk_level =="HIGH"
    