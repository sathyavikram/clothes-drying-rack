# Plan — Phase 2: Leg Tube Segment + Tube Sleeve Connector + Assembly

## Task Group 1 — Parameter Definition
1. Add all Phase 2 thread and tube params to `params.py`: `TUBE_OD`, `TUBE_WALL`, `TUBE_ID`, `SEGMENT_BODY_LENGTH`, `SPIGOT_OD`, `SPIGOT_LENGTH`, `THREAD_NOM_RADIUS`, `THREAD_PITCH`, `THREAD_LENGTH`, `THREAD_CLEARANCE`, `GENERAL_CLEARANCE`, `SLEEVE_OD`, `SLEEVE_LENGTH`, `SLEEVE_BORE_DEPTH`.
2. Verify all derived values (`TUBE_ID`, thread root radius) are computed in `params.py` — no arithmetic in part files.

## Task Group 2 — Tube Segment Body (`part_01_leg_tube.py`)
1. Construct round hollow tube body: outer cylinder OD 25 mm × 220 mm, cut inner cylinder ID 19 mm × 220 mm.
2. Construct spigot stub at each end: solid cylinder OD 20 mm × 25 mm, centred on tube axis. Fuse each spigot to tube body.

## Task Group 3 — Male Threads on Tube Spigots
1. For each spigot: build helix path with `Part.makeHelix(THREAD_PITCH, THREAD_LENGTH, t_r_inner)`.
2. Build trapezoidal thread profile wire (4-point polygon per skill spec).
3. Sweep profile along helix with `makePipeShell`.
4. Build spigot core cylinder (`t_r_inner` radius × `THREAD_LENGTH`).
5. Add tip chamfer cone for self-guiding entry.
6. Combine via `Part.makeCompound([tube_body, spigot_core_1, t_core_1, t_sweep_1, spigot_core_2, t_core_2, t_sweep_2])` — do NOT fuse thread sweeps.
7. Call `removeSplitter()` on the non-thread portions only.

## Task Group 4 — Tube Sleeve Connector (`part_01b_tube_sleeve.py`)
1. Construct sleeve outer body: solid cylinder OD 34 mm × 60 mm.
2. For each end: bore a clearance hole (radius 10 mm, depth 25 mm) from that face.
3. For each bore: build female thread helix + profile + sweep at nominal dimensions (no clearance reduction).
4. Build thread cutter: `t_core.fuse(t_sweep).removeSplitter()`.
5. Cut each thread cutter from sleeve body: `body = body.cut(thread_cutter_1).cut(thread_cutter_2)`.
6. Call `removeSplitter()` on final body.

## Task Group 5 — Assembly
1. Create `assembly.py` for this phase to assemble the full leg from multiple `part_01_leg_tube.py` instances and `part_01b_tube_sleeve.py` connectors.
2. Join the segments using the threaded joints.

## Task Group 6 — Export & Validation
1. `part_01_leg_tube.py`: export STEP + STL in lying-flat orientation (tube axis horizontal, 45° diagonal note in comment). Print `shape.Volume` for sanity check.
2. `part_01b_tube_sleeve.py`: export STEP + STL in upright orientation (cylinder axis vertical). Print `shape.Volume`.
3. Export STEP and STL files from `assembly.py`.
4. Run each headlessly: `./run.sh part_01_leg_tube.py`, `./run.sh part_01b_tube_sleeve.py`, and `./run.sh assembly.py`. Confirm no traceback and export lines present.
5. Invoke `freecad-visual-validation` agent for each part and the assembly; confirm PASS on all views.
