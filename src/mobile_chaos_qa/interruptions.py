"""Additional Android device interruption scenarios (requires demo APK)."""
from pathlib import Path
from .scenarios import run_resume_scenario

def run_screen_lock_scenario(serial: str, package: str, activity: str, output: str | Path, *, adb, pause):
    """Lock and unlock a device, then relaunch the app and inspect progression."""
    def execute(*args): return adb(["-s", serial, *args])
    # Validate launch first; use a dedicated lock/unlock cycle before the existing resume oracle.
    execute("shell", "am", "start", "-n", f"{package}/{activity}")
    pause(2)
    execute("shell", "input", "keyevent", "KEYCODE_POWER")
    pause(2)
    execute("shell", "input", "keyevent", "KEYCODE_WAKEUP")
    execute("shell", "wm", "dismiss-keyguard")
    pause(2)
    return run_resume_scenario(serial, package, activity, output, adb=adb, pause=pause)
