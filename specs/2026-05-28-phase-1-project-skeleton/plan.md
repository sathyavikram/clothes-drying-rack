# Plan — Phase 1: Project Skeleton

## Group 1 — params.py

1. Create `params.py` at the project root.
2. First line: `SCALE = 1.0`.
3. Add `BUILD_PLATE_X/Y/Z = 175.0 * SCALE`.
4. Convert all 79" variant dimensions from `specs/tech-stack.md` from inches to mm; multiply each by `SCALE`.
5. Add structural constants: `LEG_WIDTH`, `LEG_DEPTH`, `LEG_WALL`.
6. Add tolerance constants: `FIT_CLEARANCE = 0.4 * SCALE`, `TOLERANCE_PRESS = 0.2 * SCALE`.
7. Add print constraints: `WALL_MIN_STRUCTURAL = 3.0 * SCALE`, `WALL_MIN_COSMETIC = 2.0 * SCALE`, `SEGMENT_MAX = 170.0 * SCALE`.
8. Add timed threaded connection parameters and pitch constants for structural joinery.
9. Add `PROJECT_DIR` and `EXPORT_DIR` path constants.
10. Add a `__main__` block that prints every key value with its name and unit.

## Group 2 — Directory scaffolding

11. Create `exports/` directory (with `.gitkeep`).
12. Create `3d-print/` directory (with `.gitkeep`).
13. Create `media/` directory (with `.gitkeep`).

## Group 3 — run.sh

14. Create `run.sh` using the standard template from the project conventions.
15. `chmod +x run.sh`.

## Group 4 — .gitignore

16. Create `.gitignore` covering: `exports/`, `__pycache__/`, `*.pyc`, `*.pyo`, `*.FCBak`, `.DS_Store`.

## Group 5 — Smoke-test

17. Run `python params.py` — confirm exit code 0 and all values print.
18. Review printed dimensional values against `specs/tech-stack.md` for accuracy.
