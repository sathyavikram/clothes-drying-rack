# Tech Stack

## CAD Toolchain

| Layer | Tool |
|---|---|
| Parametric modelling | FreeCAD 0.21+ (Python scripting API) |
| Geometry kernel | OpenCASCADE (OCC) via `Part` workbench |
| Headless execution | `freecadcmd` (`/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`) |
| GUI inspection | FreeCAD GUI (`/Applications/FreeCAD.app/Contents/MacOS/FreeCAD`) |
| Export format — CAD | STEP (AP214) via `shape.exportStep()` |
| Export format — print | STL (binary) via `shape.exportStl()` |
| Parameters | `params.py` — single source of truth; all dimensions × `SCALE` |

## FreeCAD Python Conventions

- `SCALE = 1.0` is always the **first line** of `params.py`
- All dimensions are in **millimetres** (convert inches → mm in `params.py`)
- Primitives: `Part.makeBox`, `Part.makeCylinder`, `Part.makeSphere`, `Part.makeTorus`
- Boolean ops: `.fuse()`, `.cut()`, `.common()`; call `.removeSplitter()` after chains ≥ 3 operands
- Fillets: always wrapped in `try/except`
- Every `construct_*()` function deletes existing exports before writing, then returns the shape

## FDM Print Constraints

| Parameter | Value |
|---|---|
| Build plate | 175 × 175 × 175 mm (default) |
| Default nozzle | 0.4 mm |
| Default layer height | 0.2 mm |
| Inter-part tolerance | 0.4 mm (sliding fit), 0.2 mm (press fit) |
| Min wall thickness | 3.0 mm (structural), 2.0 mm (cosmetic) |
| Overhang rule | ≤ 45° without support |

Long structural members (legs, rods) exceed the build plate and **must** be segmented into ≤ 160 mm sub-parts with alignment dowel holes (3 mm dia, 10 mm deep) and flat mating faces.

## Dimensions — 79" Variant (canonical model)

All values converted to mm from the reference images:

| Dimension | Imperial | Metric (mm) |
|---|---|---|
| Total length (deployed) | 51.1"–79" | 1298–2007 mm |
| Total height | 51.2" | 1300 mm |
| Total depth (rod-to-rod) | 19.3" | 490 mm |
| Foot spread (deployed) | 27.5" | 699 mm |
| Folded length | 56.3" | 1430 mm |
| Folded thickness | 4" | 102 mm |
| Tube outer diameter | ~1.0" (est.) | 25 mm |
| Tube wall thickness | ~0.08" (est.) | 2 mm |

> Tube OD and wall are estimated from reference images; adjust in `params.py` if measured values differ.

## File & Folder Structure

```
clothes-drying-rack/
├── specs/                  ← project constitution (this folder)
├── params.py               ← all dimensions + SCALE + paths
├── part_01_leg_tube.py
├── part_02_xframe_hinge.py
├── part_03_top_bracket.py
├── part_04_main_rod.py
├── part_05_secondary_rod.py
├── part_06_side_arm_rod.py
├── part_07_stability_bar.py
├── part_08_locking_hinge.py
├── part_09_foot_cap.py
├── part_10_rod_end_cap.py
├── part_11_windproof_hook.py
├── assembly.py
├── export_all.py
├── run.sh
├── README.md
├── .gitignore
├── exports/
├── 3d-print/
└── media/
```
