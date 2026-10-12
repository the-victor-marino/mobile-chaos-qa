"""Safe, testable ADB wrapper. Requires an Android device for live commands."""
import subprocess
from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class DeviceResult:
    serial: str
    status: str

def parse_devices(output: str) -> list[DeviceResult]:
    """Parse 'adb devices' without treating offline devices as ready."""
    result = []
    for line in output.splitlines():
        if not line.strip() or line.startswith("List of devices"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            result.append(DeviceResult(parts[0], parts[1]))
    return result

def ready_devices(output: str) -> list[str]:
    return [item.serial for item in parse_devices(output) if item.status == "device"]

def run_adb(args: list[str], runner: Callable = subprocess.run) -> str:
    """Execute a bounded ADB command, capture output and propagate failures."""
    process = runner(["adb", *args], capture_output=True, text=True, timeout=20, check=True)
    return process.stdout
