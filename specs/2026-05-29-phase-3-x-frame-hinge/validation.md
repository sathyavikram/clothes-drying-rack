# Validation

## Required Checks
- [x] Scripts run without errors using `freecadcmd -c ...`.
- [x] Hinge `STEP` and `STL` files (`part_02`, `part_03`, `part_04`) are generated in `exports/` and are fully manifold.
- [x] No intersecting solids during FreeCAD boolean combination without clearance.
- [x] Thread clearances (`THREAD_CLEARANCE = 0.6`) are only applied to the male threads.

## FreeCAD MCP Visual Review
- [x] Generate visual renders using the FreeCAD MCP tool to verify the printed part structure.
- [x] Verify the threaded pin has a flat chopped side for horizontal printing orientation.
- [x] Verify the blind female threaded socket in `part_02` has a clean floor with no floating disconnected sweeps.
- [x] Use `assembly.py` or a dedicated assembly render script to visually verify:
  - The pin length doesn't crash into the blind hole floor.
  - The smooth shaft length lifts the pin head just clearing the top bracket.
  - Spacing and clearance (`FIT_CLEARANCE`) are correctly applied for the structural leg pegs and sockets.
  - The assembly orientates and places all bodies natively correctly.

## Merge Criteria
- [x] Hinge parts successfully exported.
- [x] FreeCAD validation screenshots explicitly confirm correct folding and spacing clearances.
- [x] PR/Files are ready to review and aligned with the `plan.md`.
