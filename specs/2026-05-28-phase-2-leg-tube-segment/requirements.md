# Requirements — Phase 2: Leg Tube Segment

## Scope

Produce a single printable leg tube segment (`part_01_leg_tube.py`) — a hollow square tube with dowel alignment holes at both ends. This segment is the repeatable building block for all four full-length legs of the drying rack.

## Decisions

- **Cross-section**: square (not round). Outer dimension 25 mm × 25 mm.
- **Wall thickness**: 2 mm → inner void 21 mm × 21 mm.
- **Segment length**: 220 mm — maximum safe length when printed at 45° diagonal on the 175 × 175 mm build plate.
  - Diagonal calculation: `175 × √2 − 25 ≈ 222 mm`; rounded down to 220 mm for clearance.
- **Dowel holes**: 3 mm diameter, 10 mm deep, centred on the tube axis at both ends (for segment-to-segment joining).
- **Print orientation**: lying flat on its largest face (25 mm × 220 mm), rotated 45° in the slicer to fit the build plate. The part file exports in this orientation with the rotation documented in a comment.

## Constraints

- Must fit within 175 × 175 × 175 mm build plate (via diagonal placement).
- No overhangs > 45° in the lying-flat orientation.
- Tube wall ≥ 3 mm is preferred for structural load; 2 mm is acceptable given the OCC-estimated tube OD of 25 mm from reference images. If a structural wall is needed, wall can be increased to 3 mm and tube OD adjusted accordingly.
- All dimensions sourced from `params.py`; part file contains no raw numbers.
- `construct_leg_tube()` must delete old STEP/STL before writing and must return the shape.

## Non-goals

- This phase does not model connector sockets, locking features, or the full leg assembly.
- No segmentation logic for the assembly (that is handled in Phase 12).
- No fillet or chamfer is required for v1; add only if it does not destabilise the boolean chain.

## Context

The full leg of the 79" variant is approximately 1300 mm tall. At 220 mm per segment, each full leg requires approximately 6 segments joined with 3 mm dowels and adhesive or press-fit. The segment geometry established here is reused verbatim for all four legs and potentially the stability bar (Phase 7).
