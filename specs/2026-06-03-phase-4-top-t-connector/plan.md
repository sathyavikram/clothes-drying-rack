# Plan

## Task Group 1: Prerequisites
1. Open and review `params.py` to ensure all necessary clearances and width/depth dimensions for the top rod and leg connection are available (e.g. `LEG_WIDTH`, `LEG_DEPTH`, `FIT_CLEARANCE`, `PEG_THREAD_RADIUS`).
2. Identify the pivot thickness requirements and thread pitch parameters from Phase 3 hinge to reuse for the top bracket.

## Task Group 2: Modellers
1. **Implement `part_05_top_bracket_rod_mount.py`**: Model the mount that attaches rigidly to the top drying rod. Needs a peg/socket for the rod and a female threaded bore for the pivot pin.
2. **Implement `part_06_top_bracket_leg_mount.py`**: Model the mount that attaches to the leg segment. Needs a peg/socket for the leg and a clearance bore for the pivot pin.
3. **Implement `part_07_top_bracket_pin.py`**: Model the male threaded locking pivot pin tailored to the thickness of parts 05 and 06.

## Task Group 3: Assembly & Validation
1. Use `test_render.py` or create a temporary assembly script to position the rod mount, leg mount, and pin together to simulate both fully folded and fully deployed states.
2. Ensure no mechanical binding occurs between the top rod line and the leg line during rotation.
