# Validation — Phase 2: Leg Tube Segment + Tube Sleeve Connector

## Required Checks

### `part_01_leg_tube.py`
1. **Headless build passes**
   ```bash
   ./run.sh part_01_leg_tube.py
   ```
   - No Python traceback. STEP + STL export lines present. `FreeCAD terminated.` last.

2. **Export files exist**: `exports/part_01_leg_tube.step` and `.stl`, non-zero bytes.

3. **Volume sanity** — tube body only (excluding thread compound):
   - Hollow cylinder: `π × (12.5² − 9.5²) × 170 ≈ 34 200 mm³` (approximate; compound adds thread volume on top)
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
   - Solid cylinder minus two bores: `π × 17² × 60 − 2 × π × 10² × 25 ≈ 54 700 − 15 700 ≈ 39 000 mm³`
   - Printed `shape.Volume` must be non-zero and in the right order of magnitude.

4. **Thread engagement check**: female thread bores visible at each end; thread helices visible in GUI cross-section.

## Visual Validation via FreeCAD MCP
- Invoke `freecad-visual-validation` agent for `part_01_leg_tube.step`.
  - Required views: Front, Top, Right, Isometric.
  - Must show: hollow tube body, two spigot stubs, thread helix on each stub, tip chamfers.
  - Report must return **PASS**.
- Invoke `freecad-visual-validation` agent for `part_01b_tube_sleeve.step`.
  - Required views: Front, Top, Isometric, cross-section (if supported).
  - Must show: barrel body, two open bores at ends with thread helices cut in.
  - Report must return **PASS**.

## Manual Review
- Open each part in FreeCAD GUI and confirm:
  - Tube: hollow interior visible, two spigot stubs, thread helix on each, no zero-volume faces.
  - Sleeve: two bored ends with female threads, solid mid-wall, no open faces.
- Visually confirm thread pitch and profile match between male spigot and female bore (same pitch = 4 mm).

## Merge Criteria
- All Required Checks pass for both parts.
- Both `freecad-visual-validation` runs return PASS.
- `params.py` contains all Phase 2 thread and tube params.
- Neither part file contains raw numbers.
- Print orientation comment present in both part files.
- `CHANGELOG.md` updated before merge.
