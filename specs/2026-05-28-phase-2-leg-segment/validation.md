# Validation — Phase 2: Leg Segment + Assembly

## Required Checks

### `part_01_leg_segment.py`
- [x] Headless build passes
   ```bash
   ./run.sh part_01_leg_segment.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

- [x] Export files exist: `exports/part_01_leg_segment.step` and `.stl`, non-zero bytes.

- [x] Volume sanity — segment body:
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

- [x] Geometry visible: threaded cylindrical peg present at one end, threaded socket interior forming a receiver at the other end.

### `assembly.py`
- [x] Headless build passes
   ```bash
   ./run.sh assembly
   ```
   - No Python traceback. STEP + STL export lines present.

- [x] Export files exist: `exports/assembly.step` and `.stl`, non-zero bytes.

- [x] Verify fit:
   - The leg segments screw tightly into the threaded socket of the adjacent segment and align their outer profile perfectly upon bottoming out.

## Visual Validation via FreeCAD MCP
- Invoke `freecad-visual-validation` agent for `part_01_leg_segment.py`.
  - Report must return PASS.
- Invoke `freecad-visual-validation` agent for `assembly.py`.
  - Report must return PASS.

## Manual Review
- Open each part in FreeCAD GUI and confirm:
  - Segment: hollow interior visible, one rectangular peg stub, bottom serves as open socket, no zero-volume faces.
  - Assembly: pegs and socket bores align correctly with the set clearance.

## Merge Criteria
- All Required Checks pass for parts and assembly.
- All `freecad-visual-validation` runs return PASS.
- `params.py` contains all Phase 2 params.
- Part file does not contain raw numbers.
- Print orientation comment present in part file.
