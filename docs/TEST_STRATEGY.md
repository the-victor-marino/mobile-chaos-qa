# Mobile interruption and recovery test strategy

**Primary oracle:** background/foreground transitions must preserve level and currency. The Android demo app saves progress to SharedPreferences on lifecycle transitions; the runner checks emitted logcat evidence.

## Current coverage

- Unit: device enumeration, offline handling, ADB error propagation.
- Contract: logcat evidence parser, missing-evidence failure, state preservation.
- Device (manual execution): Android HOME -> relaunch, persistent progress comparison and logs.

## Follow-up scenarios

- Screen off/on, process death, configuration change, low-memory pressure.
- Network off/on with an app that really consumes a network API.
- Screenshot capture, app crash/ANR diagnostics and repeatability on multiple API levels.

**Limits:** no device test can be considered passed solely because mocked CLI tests succeed. Background/resume does not prove process death or network recovery.
