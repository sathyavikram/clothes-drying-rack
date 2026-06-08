# Plan — Phase 1: Project Skeleton

## Group 1 — params.py

- Create `params.py` at the project root.
- First line: `SCALE = 1.0`.
- Add `BUILD_PLATE_X/Y/Z = 175.0 * SCALE`.
- Convert all 79" variant dimensions from `specs/tech-stack.md` from inches to mm; multiply each by `SCALE`.
- Add structural constants: `LEG_WIDTH`, `LEG_DEPTH`, `LEG_WALL`.
- Add tolerance constants: `FIT_CLEARANCE = 0.4 * SCALE`, `TOLERANCE_PRESS = 0.2 * SCALE`.
- Add print constraints: `WALL_MIN_STRUCTURAL = 3.0 * SCALE`, `WALL_MIN_COSMETIC = 2.0 * SCALE`, `SEGMENT_MAX = 170.0 * SCALE`.
- Add timed threaded connection parameters and pitch constants for structural joinery.
- Add `PROJECT_DIR` and `EXPORT_DIR` path constants.
- Add a `__main__` block that prints every key value with its name and unit.

## Group 2 — Directory scaffolding

- Create `exports/` directory (with `.gitkeep`).
- Create `3d-print/` directory (with `.gitkeep`).
- Create `media/` directory (with `.gitkeep`).

## Group 3 — run.sh

- Create `run.sh` using the standard template from the project conventions.
- `chmod +x run.sh`.

## Group 4 — .gitignore

- Create `.gitignore` covering: `exports/`, `__pycache__/`, `*.pyc`, `*.pyo`, `*.FCBak`, `.DS_Store`.

## Group 5 — Smoke-test

- Run `python params.py` — confirm exit code 0 and all values print.
- Review printed dimensional values against `specs/tech-stack.md` for accuracy.
