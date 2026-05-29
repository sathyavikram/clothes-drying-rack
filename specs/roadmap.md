# Roadmap

Each phase is a small, independently buildable unit of work.
Build, validate, and commit before moving to the next phase.

---

## Phase 0 — Project Constitution ✅
- Create `specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`
- Review all reference images
- Lock dimensions and part list

---

## Phase 1 — Project Skeleton ✅
- Create `params.py` with all dimensions (inches → mm), `SCALE`, build-plate constants, tolerances, `PROJECT_DIR`, `EXPORT_DIR`
- Create `exports/`, `3d-print/`, `media/` directories
- Create `run.sh` (executable)
- Create `.gitignore`
- Smoke-test: `python params.py` prints all key values without error

---

## Phase 2 — Leg Tube Segment + Sleeve Connector (`part_01_leg_tube.py`, `part_01b_tube_sleeve.py`)
- Round hollow tube segment max length 220 mm (calculated as diagonal of 175x175mm bed minus tube OD, with margin)
- Male-threaded spigot stubs at both ends (e.g., M20 pitch-4, 20 mm engagement)
- Companion sleeve connector (rounded clamp, female-threaded ends) to join two segments tool-free
- Print orientation: tube lying flat at 45° diagonal; sleeve upright
- Export STEP + STL for each; visual validation pass on each

---

## Phase 3 — X-Frame Center Hinge Bracket (`part_02_xframe_hinge.py`)
- The cross-pivot block at the midpoint of the X-frame
- Pin/bolt hole through the crossing axis
- Flat faces matching tube profile
- Export STEP + STL; visual validation pass

---

## Phase 4 — Top T-Connector Bracket (`part_03_top_bracket.py`)
- L-shaped or T-shaped bracket at the top of the X-frame
- Accepts top rod and angled leg tube
- Bolt holes for assembly
- Export STEP + STL; visual validation pass

---

## Phase 5 — Main Top Drying Rod Segment (`part_04_main_rod.py`)
- Round hollow tube segment ≤ 220 mm for the uppermost horizontal rod
- Threaded spigot joinery at ends (matches leg tube thread spec)
- Export STEP + STL; visual validation pass

---

## Phase 6 — Secondary & Lower Drying Rods (`part_05_secondary_rod.py`, `part_06_side_arm_rod.py`)
- Secondary horizontal rod (mid-height, front face of rack)
- Short retractable side arm rod (right side, lower)
- Both segmented if > 220 mm; threaded spigot joinery
- Export STEP + STL each; visual validation pass

---

## Phase 7 — Middle Stability Bar (`part_07_stability_bar.py`)
- Short horizontal bar spanning between the two X-frame assemblies at mid-height
- Fits within build plate (no segmentation needed)
- Export STEP + STL; visual validation pass

---

## Phase 8 — Locking Hinge Body (`part_08_locking_hinge.py`)
- Flat rectangular plate with two pivot holes and a locking notch/detent
- Models the 6-locking-hinge design seen in reference images
- Export STEP + STL; visual validation pass

---

## Phase 9 — Anti-Slip Foot Cap (`part_09_foot_cap.py`)
- Hollow round cap that slides over the tube body end (ID = tube OD + 0.4 mm sliding tolerance)
- Textured or recessed base for grip
- Export STEP + STL; visual validation pass

---

## Phase 10 — Rod End Cap (`part_10_rod_end_cap.py`)
- Small cylindrical plug that caps the open ends of drying rods
- Press-fit OD = rod ID − 0.2 mm
- Export STEP + STL; visual validation pass

---

## Phase 11 — Windproof Hook (`part_11_windproof_hook.py`)
- Small J-hook accessory that clips onto the drying rod
- Clip opening matches rod OD + 0.4 mm tolerance
- Export STEP + STL; visual validation pass

---

## Phase 12 — Full Assembly (`assembly.py`)
- Clears `exports/`; regenerates all parts
- Loads every STEP file; positions all instances
- 2 X-frames (left & right), 3 rods, 1 stability bar, 6 hinges, 4 foot caps, sleeve connectors (as required per leg count)
- Exports `assembly.step` and `assembly.stl`
- Visual validation pass

---

## Phase 13 — Final Export & Validation
- Run `export_all.py` — confirm N/N parts exported
- Verify all STL files are non-manifold-free
- Confirm `assembly.step` opens cleanly in FreeCAD GUI
- Tag release commit

---

## Out of Scope (v1)
- Animated/articulated folding simulation
- 63" and 95" size variants (add in v2 via `SCALE` parameter override)
- Physical load/stress simulation
- Colour/texture rendering
