# Requirements — Phase 1: Project Skeleton

## Scope

Phase 1 delivers the non-geometric foundation of the project: the parameter file, directory structure, shell runner, and ignore rules. No FreeCAD geometry is built in this phase.

## Deliverables

| File / Directory | Description |
|---|---|
| `params.py` | Single source of truth for all dimensions, tolerances, paths |
| `exports/` | Output directory for STEP and STL exports |
| `3d-print/` | Curated print-ready STL staging area |
| `media/` | Screenshots and renders |
| `run.sh` | Shell wrapper for headless and GUI FreeCAD commands |
| `.gitignore` | Ignores build artefacts |

## Decisions

- **SCALE = 1.0 is the first line** of `params.py` — never changes position.
- **All dimensions in millimetres** — inches are converted in `params.py` and never appear elsewhere.
- **Derived values computed in params.py** — e.g. `PEG_WIDTH = LEG_WIDTH - 2 * LEG_WALL`; part files do zero arithmetic on raw params.
- **Segment max = 170 mm** — any dimension exceeding this (given 175mm bed diagonal) triggers segmentation in later phases.
- **Tolerances**: Thread clearance = 0.6 mm, sliding fit clearance = 0.4 mm (`TOLERANCE_SLIDING`), press fit = 0.2 mm (`TOLERANCE_PRESS`).
- **Joints**: Timed cylindrical threaded peg features (standard alignment feature for all segmented structural parts).
- `exports/` is git-ignored.

## Dimensions (79" variant, converted to mm)

| Param name | Metric (mm) |
|---|---|
| `RACK_LENGTH_MIN` | 1298 mm |
| `RACK_LENGTH_MAX` | 2007 mm |
| `RACK_HEIGHT` | 1300 mm |
| `RACK_DEPTH` | 490 mm |
| `FOOT_SPREAD` | 699 mm |
| `FOLDED_LENGTH` | 1430 mm |
| `FOLDED_THICKNESS` | 102 mm |
| `LEG_WIDTH` | 25 mm |
| `LEG_DEPTH` | 25 mm |
| `LEG_WALL` | 3 mm |

## Context

- Build plate constraint: 175 × 175 × 175 mm
- FreeCAD path (headless): `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`
- FreeCAD path (GUI): `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD`
