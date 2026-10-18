"""Additional Android device interruption scenarios (requires demo APK)."""
from pathlib import Path
from .scenarios import run_resume_scenario

def run_screen_lock_scenario(serial: str, package: str, activity: str, output: str | Path, *, adb, pause):
    """Lock and unlock a device, then relaunch the app and inspect progression."""
    return run_resume_scenario(serial, package, activity, output, adb=adb, pause=pause, interruption="screen_lock")
