# Requirements — Phase 2: Leg Segment + Leg Connector + Assembly

## Scope

Produce two parts and an assembly script:
1. **`part_01_leg_segment.py`** — a rectangular hollow leg segment with solid rectangular male pegs at both ends.
2. **`part_01b_leg_connector.py`** — a rectangular connector block with female peg holes cut from each end; two leg segments slide into opposite sides to form a continuous leg.
3. **`assembly.py`** — script for assembling the full leg combining these segments.

These two parts and the assembly script use a tool-free, hardware-free resistance clearance fit (peg-and-hole).

## Decisions

### Leg Segment (`part_01_leg_segment.py`)
- **Cross-section**: Rectangular hollow segment.
- **Segment Outer Dimensions**: Width: 25 mm. Depth: 15 mm. **Wall Thickness**: 3 mm. 
- **Segment Inner Dimensions**: Width: 19 mm. Depth: 9 mm.
- **Segment length**: 170 mm body + 25 mm peg stub at each end = **220 mm total**.
  - Diagonal capacity on a 175mm plate: `175 × √2 ≈ 247 mm`. The 220 mm total length fits diagonally.
- **Peg stub**: Solid rectangular peg, Width: 19 mm, Depth: 9 mm (minus clearance), length 25 mm, concentric with segment axis, one at each end.
- **Print orientation**: Lying flat on the long face (segment axis horizontal). Fits 175 × 175 plate at 45° diagonal.

### Leg Connector (`part_01b_leg_connector.py`)
- **Dimensions**: Width: 25 mm. Depth: 15 mm. **Length**: 60 mm.
- **Wall between bores**: 10 mm solid mid-section.
- **Female bores** — one from each end:
  - Bore depth: 25 mm
  - Fits the peg stub with `FIT_CLEARANCE`.
- **Print orientation**: Standing upright (Z axis aligned) — no overhangs, no support needed.

## Variables in params.py

```python
LEG_WIDTH = 25.0 * SCALE
LEG_DEPTH = 15.0 * SCALE
LEG_WALL = 3.0 * SCALE

PEG_WIDTH = LEG_WIDTH - (2 * LEG_WALL)
PEG_DEPTH = LEG_DEPTH - (2 * LEG_WALL)
PEG_LENGTH = 25.0 * SCALE

SEGMENT_BODY_LENGTH = 170.0 * SCALE
CONNECTOR_LENGTH = 60.0 * SCALE

FIT_CLEARANCE = 0.4 * SCALE
```

## Constraints

- Each part must fit within 175 × 175 × 175 mm build plate.
  - Leg Segment (220 mm total with pegs): print diagonally at 45°.
  - Connector (60 mm): print upright, easily fits.
- No overhangs > 45° in either part's print orientation.
- All dimensions sourced from `params.py`; no raw numbers in part files.
- Each `construct_*()` deletes old STEP/STL before export and returns the shape.

## Non-goals

- No locking mechanism or anti-rotation feature in v1 (friction fit is sufficient).
- Modifying hinges or top rod connectors is out of scope.

## Context

At 170 mm body per segment, segments + connectors will form the full leg ~1300 mm. The rectangular connection is tool-free, re-usable, and prevents segment rotation.
