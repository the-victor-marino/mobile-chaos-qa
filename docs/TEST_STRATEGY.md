# Mobile interruption and recovery test strategy

**Primary oracle:** background/foreground transitions must preserve level and currency. The Android demo app saves progress to SharedPreferences on lifecycle transitions; the runner checks emitted logcat evidence.

## Current coverage

- Unit: device enumeration, offline handling, ADB error propagation.
- Contract: logcat evidence parser, missing-evidence failure, state preservation.
- Regression: reject incomplete/non-integer state; require fresh evidence after interruption; compare screen-lock state against a baseline captured before locking.
- Device (manual execution): Android HOME -> relaunch, persistent progress comparison and logs.

## Follow-up scenarios

- Screen off/on, process death, configuration change, low-memory pressure.
- Network off/on with an app that really consumes a network API.
- Screenshot capture, app crash/ANR diagnostics and repeatability on multiple API levels.

**Limits:** no device test can be considered passed solely because mocked CLI tests succeed. Background/resume does not prove process death or network recovery.

## Validation on 2026-10-18

- Local Python 3.14: 14 tests passed with mocked ADB; no emulator/device was available.
- APK CI compiles Java and Kotlin for JVM 17. A successful APK build proves compilation and packaging only, not installation or lifecycle behavior.
- The screen-lock helper is experimental and has only mocked regression coverage. Use a dedicated emulator with no secure PIN; physical-device lock policies can prevent dismissal.
- Still outstanding: install and run the APK, change the coin balance, exercise HOME/resume and screen lock, and retain real logcat/JSON evidence. Process death, rotation, crash/ANR and network scenarios remain unvalidated.
