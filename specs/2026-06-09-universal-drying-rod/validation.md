# Validation

## Required Checks
- `params.py` runs without errors and outputs the newly added parameters.
- `python part_07_threaded_adapter_pin.py` successfully generates `part_07_threaded_adapter_pin.step` and `.stl` without OpenCASCADE boolean failures.
- `python part_06_drying_rod.py` successfully generates `part_06_drying_rod.step` and `.stl` without failures.
- `python assembly.py` runs cleanly with the new parts added, confirming spatial positioning.
- Both generated parts must be manifold (zero non-manifold edges in STL).

## Review & Visual Validation
- Run the `freecad-visual-validation` skill on `assembly.py` and the individual parts.
- Review the generated renders to confirm the swept transition smoothly goes from stadium to square without degenerate faces.
- Confirm the timed threading features are correctly oriented and placed at the ends.
- Confirm the assembly validation report shows no unintended collisions or misalignments.

## Merge Criteria
- FreeCAD Visual Validation passes with a clean report.
- Parts can theoretically be printed on the 175x175mm bed diagonally.
- Branch `phase-5-universal-drying-rod` is ready to be merged into `main`.
