# Tech Stack

## CAD Tool

| Tool | Version | Role |
|---|---|---|
| FreeCAD | 0.21+ | Primary 3D modelling environment |
| FreeCAD Python API | 3.x (bundled) | Scripted part generation (`Part`, `Draft`, `Sketcher` workbenches) |

All geometry is authored as **Python scripts** (`*.py`) executed inside FreeCAD, producing parametric solid models. No GUI macro recording; scripts are source-controlled and reproducible.

## Filament & Print Settings

| Property | Value |
|---|---|
| Material | PETG |
| Rationale | Good layer adhesion, slight flex under load, heat- and moisture-resistant (suitable for a laundry environment) |
| Wall perimeters | ≥ 4 (for structural parts) |
| Infill | 40 %+ rectilinear for load-bearing parts |
| Layer height | 0.2 mm standard; 0.15 mm for hinge bores |
| Supports | Minimized by design orientation |

## Fit & Tolerance Conventions

| Fit type | Diametric clearance |
|---|---|
| Sliding fit (rod in channel) | + 0.4 mm |
| Rotating fit (hinge pin) | + 0.3 mm |
| Press / snap fit | − 0.1 mm to 0.0 mm |

*(Verify on a test coupon before printing full parts. Re-verify whenever printer is re-calibrated or filament brand changes.)*

## Batch Quality Control

Each print run must include a **QC test coupon** (small printed block with all fit bores) to confirm tolerances before committing to a full batch. Track pass/fail per printer per filament brand.

| Check | Acceptance criterion |
|---|---|
| Hinge pin fit | Rotates freely, no wobble > 0.5 mm |
| Rod slide fit | Smooth extension with one finger, no rattle |
| Press-fit joint | Requires mallet tap, no hand-press separation |
| Layer delamination | None visible at 10× magnification on load-bearing walls |

## Hardware BOM (anticipated)

| Item | Purpose |
|---|---|
| M6 × 40 mm bolts + nuts | Locking hinge pivot pins |
| M4 × 16 mm bolts + heat-set inserts | Rod bracket fasteners |
| Rubber furniture feet (20 mm dia.) | Anti-slip pads (over-moulded or press-fit into printed cup) |

## Export Formats

- **STL** — sent to slicer for printing
- **STEP** — interchange / archival (via FreeCAD `Import.export`)
