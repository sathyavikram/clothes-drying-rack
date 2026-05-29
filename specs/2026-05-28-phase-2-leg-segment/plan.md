# Plan — Phase 2: Leg Segment + Leg Connector + Assembly

## Task Group 1 — Parameter Definition
1. Add all Phase 2 segment parameters to `params.py`: `LEG_WIDTH`, `LEG_DEPTH`, `LEG_WALL`, `PEG_WIDTH`, `PEG_DEPTH`, `PEG_LENGTH`, `SEGMENT_BODY_LENGTH`, `CONNECTOR_LENGTH`, and `FIT_CLEARANCE`.
2. Verify all derived values (`PEG_WIDTH`, `PEG_DEPTH`) are computed in `params.py` — no arithmetic in part files.

## Task Group 2 — Leg Segment (`part_01_leg_segment.py`)
1. Construct rectangular hollow segment body: Width 25 mm, Depth 15 mm, Wall 3 mm, length 170 mm.
2. Construct solid rectangular peg at each end: Width 19 mm, Depth 9 mm, Length 25 mm.
3. Fuse pegs to the segment body.
4. Export in print orientation (lying flat).

## Task Group 3 — Leg Connector (`part_01b_leg_connector.py`)
1. Construct solid connector body: Width 25 mm, Depth 15 mm, length 60 mm.
2. Cut rectangular receiver bores into each end: Width `PEG_WIDTH + FIT_CLEARANCE`, Depth `PEG_DEPTH + FIT_CLEARANCE`, Length 25 mm.
3. Leave a 10 mm solid wall in the center.
4. Export in print orientation (standing upright).

## Task Group 4 — Assembly (`assembly.py`)
1. Create `assembly.py` for this phase to assemble the full leg from multiple `part_01_leg_segment.py` instances and `part_01b_leg_connector.py` connectors.
2. Position components end-to-end to verify clearance and alignments.
3. Assign discrete colors for visualization.

## Task Group 5 — Export & Validation
1. Export STEP + STL from all parts and assembly.
2. Run each headlessly using `export_all.py` / `run.sh export_all`.
3. Invoke `freecad-visual-validation` agent for each part and the assembly; confirm PASS on all views.
