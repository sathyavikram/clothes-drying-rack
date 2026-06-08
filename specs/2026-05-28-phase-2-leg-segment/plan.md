# Plan — Phase 2: Leg Segment + Assembly

## Task Group 1 — Parameter Definition
- Add all Phase 2 segment parameters to `params.py`: `LEG_WIDTH`, `LEG_DEPTH`, `LEG_WALL`, `PEG_WIDTH`, `PEG_DEPTH`, `PEG_LENGTH`, `SEGMENT_BODY_LENGTH`, and `FIT_CLEARANCE`.
- Verify all derived values (`PEG_WIDTH`, `PEG_DEPTH`) are computed in `params.py` — no arithmetic in part files.

## Task Group 2 — Leg Segment (`part_01_leg_segment.py`)
- Construct rectangular hollow segment body: Width 25 mm, Depth 15 mm, Wall 3 mm, length 170 mm.
- Construct solid threaded male peg at one end: matching thread radius and pitch to ensure full mechanical thread timing lock.
- Form corresponding threaded female hole receiver at the body's opposite end.
- Export in print orientation (lying flat).


## Task Group 3 — Assembly (`assembly.py`)
- Create `assembly.py` for this phase to assemble the full leg from multiple `part_01_leg_segment.py` instances .
- Position components end-to-end to verify clearance and alignments.
- Assign discrete colors for visualization.

## Task Group 4 — Export & Validation
- Export STEP + STL from all parts and assembly.
- Run each headlessly using `export_all.py` / `run.sh export_all`.
- Invoke `freecad-visual-validation` agent for each part and the assembly; confirm PASS on all views.
