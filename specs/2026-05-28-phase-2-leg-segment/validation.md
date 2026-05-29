# Validation — Phase 2: Leg Segment + Assembly

## Required Checks

### `part_01_leg_segment.py`
1. **Headless build passes**
   ```bash
   ./run.sh part_01_leg_segment.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/part_01_leg_segment.step` and `.stl`, non-zero bytes.

3. **Volume sanity** — segment body:
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

4. **Geometry visible**: rectangular peg stub present at one end, hollow interior forming a socket at the other end.

### `assembly.py`
1. **Headless build passes**
   ```bash
   ./run.sh assembly
   ```
   - No Python traceback. STEP + STL export lines present.

2. **Export files exist**: `exports/assembly.step` and `.stl`, non-zero bytes.

3. **Verify fit**:
   - The leg segments slide straight into the open socket of the adjacent segment and align without overlap or gaps.

## Visual Validation via FreeCAD MCP
- Invoke `freecad-visual-validation` agent for `part_01_leg_segment.py`.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `assembly.py`.
  - Report must return **PASS**.

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
