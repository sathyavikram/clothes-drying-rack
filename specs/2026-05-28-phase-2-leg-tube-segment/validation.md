# Validation — Phase 2: Leg Tube Segment

## Required Checks

1. **Headless build passes**
   ```bash
   ./run.sh part_01_leg_tube.py
   ```
   - No Python traceback in output.
   - Output contains STEP and STL export confirmation lines.
   - Final line is `FreeCAD terminated.`

2. **Export files exist**
   - `exports/part_01_leg_tube.step` present and non-zero bytes.
   - `exports/part_01_leg_tube.stl` present and non-zero bytes.

3. **Geometry sanity** (print `shape.Volume` in the script)
   - Volume is non-zero and consistent with a hollow square tube:
     `expected ≈ (25² − 21²) × 220 = (625 − 441) × 220 = 40 480 mm³`

4. **Dowel hole alignment** — confirm two cylindrical voids are centred and open at both ends (visible in FreeCAD GUI or confirmed by visual validation).

5. **Visual validation via FreeCAD MCP**
   - Invoke `freecad-visual-validation` agent after export.
   - Required views: Front, Top, Right, Isometric.
   - Report must return **PASS** on all views.
   - Failure criteria: invisible geometry, zero-volume, missing dowel holes, corrupt mesh.

## Manual Review

- Open in FreeCAD GUI (`./run.sh open part_01_leg_tube`) and confirm:
  - Hollow interior is visible in cross-section.
  - Dowel holes are present at both ends.
  - Segment length reads ~220 mm along the long axis.
  - Wall thickness reads ~2 mm on all four sides.

## Merge Criteria

- All Required Checks pass.
- `freecad-visual-validation` agent returns PASS.
- `params.py` contains `TUBE_OD`, `TUBE_WALL`, `TUBE_ID`, `SEGMENT_LENGTH`, `DOWEL_DIA`, `DOWEL_DEPTH`.
- Part file has no hard-coded dimensions.
- Print orientation comment is present at the top of `part_01_leg_tube.py`.
- `CHANGELOG.md` updated before merge.
