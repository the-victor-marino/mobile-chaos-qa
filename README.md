# 🚧 WIP — WORK IN PROGRESS 🚧

> [!WARNING]
> **UNDER DEVELOPMENT — NOT PRODUCTION READY.**
> These projects are still being developed and have **not yet been fully reviewed or understood by their author**. Code, documentation, and test coverage remain subject to review. Passing automated checks do not establish production readiness.
>
> **EM DESENVOLVIMENTO:** o autor ainda não revisou nem compreendeu completamente este projeto. Este aviso deve permanecer até que essa revisão e compreensão estejam concluídas.

---

# Mobile Chaos QA

[![QA tests](https://github.com/the-victor-marino/mobile-chaos-qa/actions/workflows/tests.yml/badge.svg)](https://github.com/the-victor-marino/mobile-chaos-qa/actions/workflows/tests.yml)

**Find Android game progression defects caused by interruptions.**

## The problem

Mobile games are interrupted by HOME, app switching, screen-off, backgrounding and process lifecycle events. A player should not lose progress simply because they leave the app.

## Delivered

- Python ADB runner with device-ready checks and error handling
- Native Kotlin **Android demo app** storing game state locally
- App exposes level/coins through both its UI and structured logcat evidence
- Automated HOME -> relaunch scenario, checking preserved game state
- JSON and logcat artifact output
- Pytest suite for parsers, negative assertions and harness behavior

## Android Studio

1. Open the `android-demo/` directory as a project in Android Studio.
2. Configure an Android Virtual Device (recommended API 35).
3. Build/run the `app` module on the emulator.
4. In a terminal with Python and `adb` on PATH:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
adb devices
python -m mobile_chaos_qa.cli --output reports/resume
```

The test returns 0 if progression is preserved and 1 if state differs. Device logs and result JSON are placed in `reports/resume/`.

## Test strategy

See [test strategy](docs/TEST_STRATEGY.md) for test oracles, environment dependencies and remaining scenarios.

## Honest scope

GitHub Actions currently validates Python harness tests **without an Android emulator**. Live device QA requires the emulator or physical hardware. Network disruption, screen-off and process-death suites are documented next steps, not proven coverage.
