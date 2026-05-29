# Validation — Phase 2: Leg Segment + Leg Connector + Assembly

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

4. **Geometry visible**: rectangular peg stubs present at both ends, hollow interior.

### `part_01b_leg_connector.py`
1. **Headless build passes**
   ```bash
   ./run.sh part_01b_leg_connector.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/part_01b_leg_connector.step` and `.stl`, non-zero bytes.

3. **Volume sanity** — connector body:
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

4. **Geometry visible**: rectangular female bores visible at each end, exact size to accommodate the pegs with clearance.

### `assembly.py`
1. **Headless build passes**
   ```bash
   ./run.sh assembly
   ```
   - No Python traceback. STEP + STL export lines present.

2. **Export files exist**: `exports/assembly.step` and `.stl`, non-zero bytes.

3. **Verify fit**:
   - The leg segments slide straight into the connector and align without overlap or gaps.

## Visual Validation via FreeCAD MCP
- Invoke `freecad-visual-validation` agent for `part_01_leg_segment.py`.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `part_01b_leg_connector.py`.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `assembly.py`.
  - Report must return **PASS**.

## Manual Review
- Open each part in FreeCAD GUI and confirm:
  - Segment: hollow interior visible, two rectangular peg stubs, no zero-volume faces.
  - Connector: two bored ends, solid mid-wall, no open faces.
  - Assembly: pegs and bores align correctly with the set clearance.

## Merge Criteria
- All Required Checks pass for parts and assembly.
- All `freecad-visual-validation` runs return PASS.
- `params.py` contains all Phase 2 params.
- Neither part file contains raw numbers.
- Print orientation comment present in both part files.
