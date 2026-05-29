# Plan — Phase 2: Leg Tube Segment

## Task Group 1 — Parameter Definition
1. Add `TUBE_OD`, `TUBE_WALL`, `TUBE_ID`, `SEGMENT_LENGTH`, `DOWEL_DIA`, `DOWEL_DEPTH` to `params.py`.
2. Confirm SEGMENT_LENGTH ≤ 220 mm (max safe diagonal on 175 × 175 build plate — see requirements).
3. Verify all derived params are computed in `params.py`; no arithmetic in the part file.

## Task Group 2 — Tube Body
1. Construct outer square box: `Part.makeBox(TUBE_OD, TUBE_OD, SEGMENT_LENGTH)`.
2. Construct inner square void: `Part.makeBox(TUBE_ID, TUBE_ID, SEGMENT_LENGTH)` centred in outer box.
3. Cut inner void from outer box to produce hollow square tube.

## Task Group 3 — Dowel Holes
1. Add two cylindrical cuts (dia `DOWEL_DIA`, depth `DOWEL_DEPTH`) at each end of the tube, centred on the tube axis.
2. Apply `removeSplitter()` after the boolean chain.
3. Wrap any `makeFillet()` call in `try/except`.

## Task Group 4 — Export & Validation
1. Export STEP and STL from `construct_leg_tube()`, deleting old files first.
2. Print orientation: lying flat on its largest face, rotated 45° diagonally to maximise length on build plate. Document orientation in a comment.
3. Run headlessly: `./run.sh part_01_leg_tube.py`; confirm no traceback and export lines present.
4. Invoke `freecad-visual-validation` agent; confirm PASS on all views.
