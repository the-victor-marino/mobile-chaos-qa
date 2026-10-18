"""Run a controlled Android emulator/device recovery test."""
import argparse
import json
from .adb import run_adb, ready_devices
from .scenarios import run_resume_scenario

def main():
    parser = argparse.ArgumentParser(description="Run Mobile Chaos QA against the installed demo APK")
    parser.add_argument("--serial")
    parser.add_argument("--package", default="com.gameguard.mobilechaosdemo")
    parser.add_argument("--activity", default=".MainActivity")
    parser.add_argument("--output", default="reports/resume")
    args = parser.parse_args()
    devices = ready_devices(run_adb(["devices"]))
    serial = args.serial or (devices[0] if len(devices)==1 else None)
    if not serial or serial not in devices:
        parser.error("Specify a ready device with --serial (check 'adb devices')")
    result = run_resume_scenario(serial,args.package,args.activity,args.output)
    print(json.dumps(result.__dict__,indent=2))
    return 0 if result.passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
