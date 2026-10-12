# Mobile Chaos QA

**An Android game interruption and recovery testing toolkit.**

Mobile games must handle background/foreground transitions, device interruptions, network changes and unexpected app termination without corrupting the player's progress.

## Current MVP (foundation)

A testable Python ADB wrapper and parser distinguish **ready**, **offline** and other reported Android devices. Unit tests run without requiring a physical Android device.

**This foundation does not yet run lifecycle scenarios against an APK.** Actual lifecycle recovery checks need Android Emulator or a physical device plus a controlled test app.

## Run

```bash
python -m pip install -e ".[test]"
python -m pytest -q
adb devices
```

## Roadmap

1. Device setup and preflight checks.
2. Dedicated demo Android app with observable lifecycle state.
3. Background/resume and screen-lock interruption sequences.
4. Network drop/recovery sequences, safe cleanup and logs.
5. Evidence bundles, pass/fail assertions and CI strategy for emulator tests.

## Evidence

CI currently verifies the harness logic only; it does not claim real Android app or device test coverage.
