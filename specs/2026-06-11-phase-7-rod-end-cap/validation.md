# Validation

## Required Checks
- `part_09_rod_end_cap.py` executes without geometry errors and successfully generates `part_09_rod_end_cap.step` and `.stl`.
- The `assembly.step` exports successfully containing the new rod end caps.
- Run `check_interference` on the `assembly.py` script. The rod end cap's male threads must clear the female rod threads without critical intersection volumes (standard acceptable numerical clearance for FreeCAD threads applies).

## Visual Review
- Use `render_freecad_script` or `section_freecad_model` to verify that the dome profile correctly renders on the cap's face.
- Verify through visual tools that the rod end cap mounts cleanly onto the exposed horizontal rods in the assembly, with outer profiles perfectly flush.

## Merge Criteria
- A fully populated Visual Validation Report must be printed in the chat confirming the successful execution of checks.
- Code is pushed to a feature branch ready for merge.
