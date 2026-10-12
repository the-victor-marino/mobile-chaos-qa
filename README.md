# Mobile Chaos QA

**Android game lifecycle interruption and recovery testing.**

## Why it matters

Mobile games must recover correctly when the player backgrounds the app, locks the device, or experiences network disruptions.

## MVP scope

A Python/ADB test harness that checks connected-device readiness, captures evidence, and later drives a dedicated Android demo app. Real lifecycle test results require an emulator or device.

## Test strategy

This project documents assumptions, positive and negative scenarios, reproducible evidence, and explicit release criteria. The first implementation will be developed on a feature branch and reviewed before merging.

## Status

**In development — initial scaffold.** No passing-test or real-device claims until verified.

## Roadmap

1. Minimal working implementation
2. Automated positive, boundary, and adversarial tests
3. CI reports and reproducible failures
4. Portfolio-quality documentation and demos

## License

License to be chosen before distribution.
