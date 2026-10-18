"""ADB-driven Android lifecycle smoke tests with structured evidence."""
from __future__ import annotations
import json
import re
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from .adb import run_adb, ready_devices

@dataclass
class ScenarioResult:
    name: str
    passed: bool
    expected: str
    observed: str

def parse_state(output: str) -> dict:
    """Demo app emits: GAME_STATE:{json} as an Android logcat line."""
    matches = re.findall(r"GAME_STATE:(\{[^\r\n]*\})", output)
    if not matches:
        raise ValueError("No GAME_STATE evidence in logcat")
    return json.loads(matches[-1])

def assert_preserved(before: dict, after: dict) -> ScenarioResult:
    fields = ("level", "coins")
    for state in (before, after):
        if not isinstance(state, dict) or any(type(state.get(k)) is not int for k in fields):
            raise ValueError("State evidence requires integer level and coins")
    changed = [k for k in fields if before.get(k) != after.get(k)]
    return ScenarioResult("resume_preserves_progress", not changed, "unchanged level and coins", "changed: " + ", ".join(changed) if changed else "unchanged")

def run_resume_scenario(serial: str, package: str, activity: str, output: str | Path, *, adb=run_adb, pause=time.sleep, interruption="home"):
    """Requires installed demo APK. Captures before/after states and logcat."""
    if interruption not in ("home", "screen_lock"):
        raise ValueError("Unknown interruption")
    def execute(*args): return adb(["-s", serial, *args])
    execute("logcat", "-c")
    execute("shell", "am", "start", "-n", f"{package}/{activity}")
    pause(2)
    before_logs = execute("logcat", "-d", "-s", "MobileChaosDemo:I", "*:S")
    before = parse_state(before_logs)
    execute("logcat", "-c")
    if interruption == "screen_lock":
        execute("shell", "input", "keyevent", "KEYCODE_SLEEP")
        pause(2)
        execute("shell", "input", "keyevent", "KEYCODE_WAKEUP")
        execute("shell", "wm", "dismiss-keyguard")
    else:
        execute("shell", "input", "keyevent", "KEYCODE_HOME")
        pause(2)
    execute("shell", "am", "start", "-n", f"{package}/{activity}")
    pause(2)
    logs = execute("logcat", "-d", "-s", "MobileChaosDemo:I", "*:S")
    after = parse_state(logs)
    result = assert_preserved(before, after)
    if interruption == "screen_lock":
        result.name = "screen_lock_preserves_progress"
    path = Path(output)
    path.mkdir(parents=True, exist_ok=True)
    (path / "logcat.txt").write_text("=== BEFORE INTERRUPTION ===\n" + before_logs + "\n=== AFTER RELAUNCH ===\n" + logs, encoding="utf-8")
    (path / "result.json").write_text(json.dumps({"before":before,"after":after,"result":asdict(result)},indent=2),encoding="utf-8")
    return result
