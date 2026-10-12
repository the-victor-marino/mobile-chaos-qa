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
    changed = [k for k in fields if before.get(k) != after.get(k)]
    return ScenarioResult("resume_preserves_progress", not changed, "unchanged level and coins", "changed: " + ", ".join(changed) if changed else "unchanged")

def run_resume_scenario(serial: str, package: str, activity: str, output: str | Path, *, adb=run_adb, pause=time.sleep):
    """Requires installed demo APK. Captures before/after states and logcat."""
    def execute(*args): return adb(["-s", serial, *args])
    execute("logcat", "-c")
    execute("shell", "am", "start", "-n", f"{package}/{activity}")
    pause(2)
    execute("shell", "input", "keyevent", "KEYCODE_HOME")
    pause(2)
    execute("shell", "am", "start", "-n", f"{package}/{activity}")
    pause(2)
    logs = execute("logcat", "-d", "-s", "MobileChaosDemo:I", "*:S")
    matches = re.findall(r"GAME_STATE:(\{[^\r\n]*\})", logs)
    if len(matches) < 2:
        raise ValueError("Missing before/after state evidence. Check that the demo app is installed.")
    before, after = json.loads(matches[0]), json.loads(matches[-1])
    result = assert_preserved(before, after)
    path = Path(output)
    path.mkdir(parents=True, exist_ok=True)
    (path / "logcat.txt").write_text(logs, encoding="utf-8")
    (path / "result.json").write_text(json.dumps({"before":before,"after":after,"result":asdict(result)},indent=2),encoding="utf-8")
    return result
