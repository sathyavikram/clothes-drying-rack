# Validation

## Required Checks
1. **Manifold Check**: Ensure the exported STL has zero non-manifold edges.
2. **Clearance Fit**: Verify a proper 0.2mm clearance fit with the leg segment in the assembly.
3. **Visual Inspection**: Visual validation of the bottom grip/tread pattern and overall geometry.

## Manual Review
- Check the exported STEP file in FreeCAD GUI to ensure boolean operations (like the grid cut) were successful without silent OpenCASCADE failures.
- Verify that the bottom base is perfectly flat for printing.

## Merge Criteria
- All 3 required checks pass.
- `part_08_foot_cap.py` generates cleanly when `python export_all.py` or the `run.sh` script is executed.
- `assembly.py` correctly positions the 4 foot caps.
