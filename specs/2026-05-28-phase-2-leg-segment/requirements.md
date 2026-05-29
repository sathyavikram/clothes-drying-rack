# Requirements — Phase 2: Leg Segment + Assembly

## Scope

Produce one part and an assembly script:
1. **`part_01_leg_segment.py`** — a rectangular hollow leg segment with a solid rectangular male peg at one end, and an open hollow body serving as the female socket at the other.
2. **`assembly.py`** — script for assembling a stacked section of two leg segments.

These use a tool-free, hardware-free resistance clearance fit (peg-and-socket).

## Decisions

### Leg Segment (`part_01_leg_segment.py`)
- **Cross-section**: Rectangular hollow segment.
- **Segment Outer Dimensions**: Width: 25 mm. Depth: 15 mm. **Wall Thickness**: 3 mm. 
- **Segment Inner Dimensions**: Width: 19 mm. Depth: 9 mm.
- **Segment length**: 170 mm body + 25 mm peg stub at the top end = **195 mm total**.
  - Diagonal capacity on a 175mm plate: `175 × √2 ≈ 247 mm`. The 195 mm total length fits easily.
- **Peg stub**: Solid rectangular peg, Width: 19 mm, Depth: 9 mm (minus clearance), length 25 mm, aligned linearly at `$l/2`.
- **Bottom socket**: The open cavity extending from `$-l/2$` naturally accepts the peg of the segment below.
- **Print orientation**: Lying flat on the long face (segment axis horizontal). Fits 175 × 175 plate at 45° diagonal.

## Variables in params.py

```python
LEG_WIDTH = 25.0 * SCALE
LEG_DEPTH = 15.0 * SCALE
LEG_WALL = 3.0 * SCALE

PEG_WIDTH = LEG_WIDTH - (2 * LEG_WALL)
PEG_DEPTH = LEG_DEPTH - (2 * LEG_WALL)
PEG_LENGTH = 25.0 * SCALE

SEGMENT_BODY_LENGTH = 170.0 * SCALE

FIT_CLEARANCE = 0.4 * SCALE
```

## Constraints

- Each part must fit within 175 × 175 × 175 mm build plate.
  - Leg Segment (195 mm total with peg): print diagonally at 45°.
- No overhangs > 45° in the part's print orientation.
- All dimensions sourced from `params.py`; no raw numbers in part files.
- Each `construct_*()` deletes old STEP/STL before export and returns the shape.

## Non-goals

- No locking mechanism or anti-rotation feature in v1 (friction fit is sufficient).
- Modifying hinges or top rod connectors is out of scope.

## Context

At 170 mm body per segment, the segments will form the full leg ~1300 mm. The rectangular connection is tool-free, re-usable, and prevents segment rotation.
