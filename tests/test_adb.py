from mobile_chaos_qa.adb import parse_devices, ready_devices, run_adb

SAMPLE = "List of devices attached\nemulator-5554\tdevice\nABC123\toffline\n"

def test_parse_connected_and_offline_devices():
    devices = parse_devices(SAMPLE)
    assert len(devices) == 2
    assert devices[1].status == "offline"

def test_only_ready_devices_can_run_tests():
    assert ready_devices(SAMPLE) == ["emulator-5554"]

def test_adb_wrapper_uses_timeout_and_checks_failures():
    recorded = {}
    def fake_runner(cmd, **kwargs):
        recorded.update(cmd=cmd, kwargs=kwargs)
        return type("Result", (), {"stdout": "ok"})()
    assert run_adb(["devices"], runner=fake_runner) == "ok"
    assert recorded["cmd"] == ["adb", "devices"]
    assert recorded["kwargs"]["check"] is True
    assert recorded["kwargs"]["timeout"] == 20
