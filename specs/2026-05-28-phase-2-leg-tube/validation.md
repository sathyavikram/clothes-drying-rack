# Validation

## Required Checks
- Terminal output shows no errors when running `./run.sh part_01_leg_tube.py`.
- Terminal output shows no errors when running `./run.sh assembly.py`.
- Both `.step` and `.stl` files are generated in `exports/` for both the part and the assembly.
- Manifold check passes for the exported STLs.

## Manual Review
- Visually inspect the generated STEP files to ensure thread profiles, round pipe geometry, and the assembly correctly aligns.
- Verify dimensional constraints (max 220 mm length per segment, overall leg assembly length meets required dimensions).

## Merge Criteria
- Visual validation report using `freecad-visual-validation` (or `mcp_freecad_execute_freecad_script`) must return PASS.
- Code conforms to FreeCAD Python Conventions outlined in `tech-stack.md` (e.g., clearing exports, reloading params).
