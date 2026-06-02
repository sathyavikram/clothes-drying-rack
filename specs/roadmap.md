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

## Phase 2 — Leg Segment (`part_01_leg_segment.py`) ✅
- Rectangular hollow segment max length 220 mm (calculated as diagonal of 175x175mm bed minus length of pegs)
- Integrated solid cylindrical threaded male peg at one end
- Integrated cylindrical threaded hole at the opposite end (acting as the female receiver socket)
- Threading geometry is timed so that when segments are fully tightened, their outer rectangular profiles perfectly align to form a continuous visual rod. 
- Print orientation: segment lying flat at 45° diagonal
- Export STEP + STL; visual validation pass

---

## Phase 3 — X-Frame Center Hinge ✅
- Replaced monolithic print-in-place block with a robust 3-part threaded mechanism:
  - `part_02_xframe_hinge_bottom.py`: Bottom hinge bracket featuring a female M16 equivalent thread.
  - `part_03_xframe_hinge_top.py`: Top hinge bracket featuring a clearance bore.
  - `part_04_xframe_hinge_pin.py`: Male threaded locking pivot pin printed flat to ensure strong horizontal layer orientation.
- Integrates seamlessly with X-frame rectangular leg segments (using the threaded cylinder joinery timed for profile alignment)
- Export STEP + STL; visual validation pass

---

## Phase 4 — Top T-Connector Bracket (`part_05_top_bracket.py`)
- L-shaped or T-shaped bracket at the top of the X-frame
- Accepts top rod and angled leg segment, incorporating a pivot to support the folding capability
- Threaded pivot mechanisms to follow similar 3-part approach as Phase 3 where required
- Export STEP + STL; visual validation pass

---

## Phase 5 — Main Top Drying Rod Segment (`part_06_main_rod.py`)
- Rectangular hollow segment ≤ 220 mm for the uppermost horizontal rod
- Male threaded peg / female threaded socket joinery to match legs
- Export STEP + STL; visual validation pass

---

## Phase 6 — Secondary & Lower Drying Rods (`part_07_secondary_rod.py`, `part_08_side_arm_rod.py`)
- Secondary horizontal rod (mid-height, front face of rack)
- Short retractable side arm rod (right side, lower)
- Both segmented if > 220 mm; male threaded peg / female threaded socket joinery to match legs
- Export STEP + STL each; visual validation pass

---

## Phase 7 — Middle Stability Bar (`part_09_stability_bar.py`)
- Short horizontal bar spanning between the two X-frame assemblies at mid-height
- Fits within build plate (no segmentation needed)
- Export STEP + STL; visual validation pass

---

## Phase 8 — Locking Hinge Body (`part_10_locking_hinge.py`)
- Flat rectangular plate with two pivot holes and a locking notch/detent
- Models the 6-locking-hinge design seen in reference images, strictly enabling the foldable mechanism so the rack can collapse flat
- Export STEP + STL; visual validation pass

---

## Phase 9 — Anti-Slip Foot Cap (`part_11_foot_cap.py`)
- Cap that slides over the rectangular segment body end
- Textured or recessed base for grip
- Export STEP + STL; visual validation pass

---

## Phase 10 — Rod End Cap (`part_12_rod_end_cap.py`)
- Small rectangular plug that caps the open ends of rectangular drying rods
- Press-fit with tight tolerance
- Export STEP + STL; visual validation pass

---

## Phase 11 — Windproof Hook (`part_13_windproof_hook.py`)
- Small J-hook accessory that clips onto the rectangular drying rod
- Clip opening matches rod dimensions + tolerance
- Export STEP + STL; visual validation pass

---

## Phase 12 — Full Assembly (`assembly.py`)
- Clears `exports/`; regenerates all parts
- Loads every STEP file; positions all instances
- 2 X-frames (left & right), 3 rods, 1 stability bar, 6 hinges, 4 foot caps
- Exports `assembly.step` and `assembly.stl`
- Visual validation pass

---

## Phase 13 — Final Export & Validation
- Run `export_all.py` — confirm N/N parts exported
- Select and render final assembly image
- Tag release commit

---

## Out of Scope (v1)
- Animated/articulated folding simulation
- Physical load/stress simulation
- Colour/texture rendering
