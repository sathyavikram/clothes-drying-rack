# Validation — Phase 1: Project Skeleton

## Merge criteria

Phase 1 is complete and ready to merge when **all** of the following pass.

---

### - [x] 1. Smoke-test: params.py runs clean

```bash
python params.py
```

- Exit code **0**
- No `SyntaxError`, `NameError`, or `ImportError`
- Every key parameter printed with name and unit

---

### - [x] 2. Manual review of printed values

Check each printed value:

| Check | Expected |
|---|---|
| `LEG_WIDTH` | 25.0 mm |
| `LEG_DEPTH` | 25.0 mm |
| `LEG_WALL` | 3.0 mm |
| `RACK_HEIGHT` | 1300.0 mm |
| `RACK_DEPTH` | 490.0 mm |
| `SEGMENT_BODY_LENGTH` | 170.0 mm |
| `TOLERANCE_SLIDING` | 0.4 mm |
| `TOLERANCE_PRESS` | 0.2 mm |
| `THREAD_CLEARANCE` | 0.6 mm |
| `GENERAL_CLEARANCE` | 0.4 mm |
| `BUILD_PLATE_X/Y/Z` | 175.0 mm each |
| `EXPORT_DIR` | Absolute path ending in `/exports` |

All values must be dimensionally consistent and match the specs.

---

### - [x] 3. Directory structure exists

```
exports/    ← present
3d-print/   ← present
media/      ← present
```

---

### - [x] 4. run.sh is executable

```bash
./run.sh
```

Prints usage text and exits — no `permission denied`.

---

### - [x] 5. .gitignore covers artefacts

`exports/`, `__pycache__/`, `*.pyc`, `*.pyo`, `*.FCBak`, `.DS_Store` are all present in `.gitignore`.

---

## What is explicitly NOT validated in Phase 1

- FreeCAD can import `params.py` (tested in Phase 2 when the first part script runs)
- Dimensional accuracy of geometry (no geometry exists yet)
- Visual validation (no shapes to render)
