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
- **Derived values computed in params.py** — e.g. `TUBE_ID = TUBE_OD - 2 * TUBE_WALL`; part files do zero arithmetic on raw params.
- **Segment max = 160 mm** — any dimension exceeding this triggers segmentation in later phases.
- **Tolerances**: sliding fit = 0.4 mm, press fit = 0.2 mm (from `specs/tech-stack.md`).
- **Dowels**: 3 mm diameter, 10 mm deep (standard alignment feature for all segmented parts).
- `exports/` is git-ignored; `.gitkeep` files are committed to preserve the directory.

## Dimensions (79" variant, converted from specs/tech-stack.md)

| Param name | Imperial | Metric (mm) |
|---|---|---|
| `RACK_LENGTH_MIN` | 51.1" | 1298 mm |
| `RACK_LENGTH_MAX` | 79.0" | 2007 mm |
| `RACK_HEIGHT` | 51.2" | 1300 mm |
| `RACK_DEPTH` | 19.3" | 490 mm |
| `FOOT_SPREAD` | 27.5" | 699 mm |
| `FOLDED_LENGTH` | 56.3" | 1430 mm |
| `FOLDED_THICKNESS` | 4.0" | 102 mm |
| `TUBE_OD` | ~1.0" est. | 25 mm |
| `TUBE_WALL` | ~0.08" est. | 2 mm |

> Tube OD and wall are estimates from reference images. If measured values differ, update only `params.py`.

## Context

- Reference: `specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`
- Build plate constraint: 175 × 175 × 175 mm
- FreeCAD path (headless): `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`
- FreeCAD path (GUI): `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD`
- No FreeCAD geometry is created in this phase; `params.py` must be importable by both plain `python3` and `freecadcmd`.
