# Plan

## Task Group 1: Prerequisites
- Open and review `params.py` to ensure all necessary clearances and width/depth dimensions for the top rod and leg connection are available (e.g. `LEG_WIDTH`, `LEG_DEPTH`, `FIT_CLEARANCE`, `PEG_THREAD_RADIUS`).
- Determine the required deployed leg angle from the design (e.g. 65 degrees from horizontal, or 25 degrees from vertical) to use as the built-in angle for the T-bracket stem.

## Task Group 2: Modellers
- **Implement `part_05_top_t_bracket.py`**: Model the rigid T-bracket. 
   - **Stem:** Angled at the deployed angle to attach to the X-frame leg. Needs standard timed threaded joinery.
   - **Crossbar:** Horizontal mount for the top drying rod. Needs standard timed threaded joinery.

## Task Group 3: Assembly & Validation
- Update `assembly.py` to load and position the T-bracket at the top of the B-arm leg using a mathematical rotation matrix derived from the 65° deployed angle.
- Run `./run.sh assembly` headlessly to verify the bracket appears correctly placed and no Python errors occur.
- Open `exports/assembly.step` in FreeCAD GUI (`./run.sh open assembly`) to visually confirm the crossbar is horizontal in the deployed configuration.
