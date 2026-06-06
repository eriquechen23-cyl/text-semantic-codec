# CODEX.md

## Scope

This repository contains a text-first semantic communication prototype. Keep changes focused on making the semantic encode/transmit/decode/evaluate loop easier to run, inspect, and extend.

## Current Stage

Stage 01: interpretable text prototype.

## Rules For Future Work

- Every subdirectory must include a `CODEX.md` file explaining its purpose.
- Every completed stage must include a `report.html` under `reports/<stage-name>/`.
- During coding work, update the local `reports/REPORT.md` file at each major workflow checkpoint with the current project status, completed work, risks/blockers, verification results, and recommended next direction. This file is intentionally gitignored.
- Prefer small, testable modules over hidden behavior.
- Keep the prototype runnable without heavyweight model downloads unless a later report explicitly justifies the dependency.
