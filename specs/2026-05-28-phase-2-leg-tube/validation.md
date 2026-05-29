# Validation — Phase 2: Leg Tube Segment + Tube Sleeve Connector + Assembly

## Required Checks

### `part_01_leg_tube.py`
1. **Headless build passes**
   ```bash
   ./run.sh part_01_leg_tube.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/part_01_leg_tube.step` and `.stl`, non-zero bytes.

3. **Volume sanity** — tube body only:
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

4. **Thread geometry visible**: spigot stubs present at both ends with thread helix visible in GUI.

### `part_01b_tube_sleeve.py`
1. **Headless build passes**
   ```bash
   ./run.sh part_01b_tube_sleeve.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/part_01b_tube_sleeve.step` and `.stl`, non-zero bytes.

3. **Volume sanity** — sleeve body:
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

4. **Thread engagement check**: female thread bores visible at each end; thread helices visible in GUI cross-section.

### `assembly.py`
1. **Headless build passes**
   ```bash
   ./run.sh assembly
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/assembly.step` and `.stl`, non-zero bytes.

3. **Assembly length**:
   - The full leg assembly should closely match the 1300 mm total requirement.

## Visual Validation via FreeCAD MCP
- Invoke `freecad-visual-validation` agent for `part_01_leg_tube.step`.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `part_01b_tube_sleeve.step`.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `assembly.step`.
  - Report must return **PASS**.

## Manual Review
- Open each part in FreeCAD GUI and confirm:
  - Tube: hollow interior visible, two spigot stubs, thread helix on each, no zero-volume faces.
  - Sleeve: two bored ends with female threads, solid mid-wall, no open faces.
  - Assembly: threads match and align correctly.
- Verify dimensional constraints (max 220 mm length per segment, overall leg assembly length).

## Merge Criteria
- All Required Checks pass for parts and assembly.
- All `freecad-visual-validation` runs return PASS.
- `params.py` contains all Phase 2 thread and tube params.
- Neither part file contains raw numbers.
- Print orientation comment present in both part files.
