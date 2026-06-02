# Validation

## Required Checks
- [ ] Scripts run without errors using `freecadcmd -c ...`.
- [ ] Hinge `STEP` and `STL` files (`part_02`, `part_03`, `part_04`) are generated in `exports/` and are fully manifold.
- [ ] No intersecting solids during FreeCAD boolean combination without clearance.
- [ ] Thread clearances (`THREAD_CLEARANCE = 0.6`) are only applied to the male threads.

## FreeCAD MCP Visual Review
- [ ] Generate visual renders using the FreeCAD MCP tool to verify the printed part structure.
- [ ] Verify the threaded pin has a flat chopped side for horizontal printing orientation.
- [ ] Verify the blind female threaded socket in `part_02` has a clean floor with no floating disconnected sweeps.
- [ ] Use `assembly.py` or a dedicated assembly render script to visually verify:
  - The pin length doesn't crash into the blind hole floor.
  - The smooth shaft length lifts the pin head just clearing the top bracket.
  - Spacing and clearance (`FIT_CLEARANCE`) are correctly applied for the structural leg pegs and sockets.
  - The assembly orientates and places all bodies natively correctly.

## Merge Criteria
- Hinge parts successfully exported.
- FreeCAD validation screenshots explicitly confirm correct folding and spacing clearances.
- PR/Files are ready to review and aligned with the `plan.md`.
