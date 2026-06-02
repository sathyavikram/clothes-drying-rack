# Plan — Phase 2: Leg Segment + Assembly

## Task Group 1 — Parameter Definition
1. Add all Phase 2 segment parameters to `params.py`: `LEG_WIDTH`, `LEG_DEPTH`, `LEG_WALL`, `PEG_WIDTH`, `PEG_DEPTH`, `PEG_LENGTH`, `SEGMENT_BODY_LENGTH`, and `FIT_CLEARANCE`.
2. Verify all derived values (`PEG_WIDTH`, `PEG_DEPTH`) are computed in `params.py` — no arithmetic in part files.

## Task Group 2 — Leg Segment (`part_01_leg_segment.py`)
1. Construct rectangular hollow segment body: Width 25 mm, Depth 15 mm, Wall 3 mm, length 170 mm.
2. Construct solid threaded male peg at one end: matching thread radius and pitch to ensure full mechanical thread timing lock.
3. Form corresponding threaded female hole receiver at the body's opposite end.
4. Export in print orientation (lying flat).


## Task Group 3 — Assembly (`assembly.py`)
1. Create `assembly.py` for this phase to assemble the full leg from multiple `part_01_leg_segment.py` instances .
2. Position components end-to-end to verify clearance and alignments.
3. Assign discrete colors for visualization.

## Task Group 4 — Export & Validation
1. Export STEP + STL from all parts and assembly.
2. Run each headlessly using `export_all.py` / `run.sh export_all`.
3. Invoke `freecad-visual-validation` agent for each part and the assembly; confirm PASS on all views.
