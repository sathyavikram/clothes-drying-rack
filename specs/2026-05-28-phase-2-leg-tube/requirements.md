# Requirements — Phase 2: Leg Tube Segment + Tube Sleeve Connector + Assembly

## Scope

Produce two parts and an assembly script:
1. **`part_01_leg_tube.py`** — a round hollow tube segment with male-threaded spigot stubs at both ends.
2. **`part_01b_tube_sleeve.py`** — a short barrel connector with female threads bored from each end; two tube segments screw in from opposite sides to form a continuous leg.
3. **`assembly.py`** — script for assembling the full leg combining these segments.

These two parts and the assembly script replace the dowel-pin joining strategy with a tool-free, hardware-free threaded connection.

## Decisions

### Tube segment (`part_01_leg_tube.py`)
- **Cross-section**: round (hollow cylinder).
- **Tube OD**: 25 mm. **Wall**: 3 mm. **Tube ID**: 19 mm.
- **Segment length**: 220 mm body + 25 mm spigot stub at each end = **270 mm total** (fits on build plate diagonally; see constraint below).
  - Diagonal capacity: `175 × √2 − 25 ≈ 222 mm`. Body is 220 mm; diagonal is for body only. Spigots print at the same diameter as body, no extra footprint.
  - Alternatively, segment body can be shortened to 170 mm to keep total length ≤ 220 mm on diagonal. Use `SEGMENT_BODY_LENGTH = 170 mm` as default; total with two spigots = **220 mm**.
- **Spigot stub**: solid cylinder, OD 20 mm, length 25 mm, concentric with tube axis, one at each end.
- **Male thread** on each spigot:
  - Nominal radius: `THREAD_NOM_RADIUS = 10.0 mm`
  - Pitch: `THREAD_PITCH = 4.0 mm` (coarse — FDM structural)
  - Thread length: `THREAD_LENGTH = 20 mm`
  - Applied clearance: `t_radius = THREAD_NOM_RADIUS − THREAD_CLEARANCE` (0.6 mm) = **9.4 mm**
  - Root radius: `t_r_inner = t_radius − (THREAD_PITCH × 0.45)` = 9.4 − 1.8 = **7.6 mm**
  - Tip chamfer added for self-guiding entry.
  - Use `Part.makeCompound([spigot_core, t_core, t_sweep])` — do NOT fuse the thread sweep.
- **Print orientation**: lying flat on the long face (tube axis horizontal). Fits 175 × 175 plate at 45° diagonal.

### Tube sleeve connector (`part_01b_tube_sleeve.py`)
- **OD**: 34 mm. **Length**: 60 mm.
- **Wall between bores**: 10 mm solid mid-section.
- **Female thread bores** — one from each end:
  - Bore radius (clearance hole): `THREAD_NOM_RADIUS = 10.0 mm` (nominal, no reduction)
  - Bore depth: 25 mm (5 mm entry + 20 mm thread engagement)
  - Pitch: 4.0 mm (matches male)
  - Root radius: `t_r_inner = 10.0 − (4.0 × 0.45) = 8.2 mm`
  - Female thread cutter: `t_core.fuse(t_sweep).removeSplitter()`, then `body.cut(thread_cutter)`
- **Print orientation**: standing upright (cylinder axis vertical) — no overhangs, no support needed.

## Thread parameters — add to `params.py`
```
THREAD_CLEARANCE       = 0.6 * SCALE
GENERAL_CLEARANCE      = 0.4 * SCALE
THREAD_NOM_RADIUS      = 10.0 * SCALE   # nominal 20 mm OD thread
THREAD_PITCH           = 4.0 * SCALE
THREAD_LENGTH          = 20.0 * SCALE
SPIGOT_OD              = 20.0 * SCALE
SPIGOT_LENGTH          = 25.0 * SCALE
TUBE_OD                = 25.0 * SCALE
TUBE_WALL              = 3.0 * SCALE
TUBE_ID                = 19.0 * SCALE   # = TUBE_OD − 2 × TUBE_WALL
SEGMENT_BODY_LENGTH    = 170.0 * SCALE
SLEEVE_OD              = 34.0 * SCALE
SLEEVE_LENGTH          = 60.0 * SCALE
SLEEVE_BORE_DEPTH      = 25.0 * SCALE
```

## Constraints

- Each part must fit within 175 × 175 × 175 mm build plate.
  - Tube segment (220 mm total with spigots): print diagonally at 45°.
  - Sleeve (60 mm): print upright, easily fits.
- No overhangs > 45° in either part's print orientation.
- All dimensions sourced from `params.py`; no raw numbers in part files.
- Each `construct_*()` deletes old STEP/STL before export and returns the shape.
- Male thread uses `makeCompound` (not fuse) to avoid OCC boolean hangs.
- Female thread uses `fuse().removeSplitter()` only for the cutter shape.

## Non-goals

- No locking mechanism or anti-rotation feature in v1.
- No fillet/chamfer on the tube body ends unless it aids print quality.
- Modifying hinges or top rod connectors is out of scope.

## Context

At 170 mm body per segment, segments + sleeves will form the full leg ~1300 mm. Each sleeve weighs ~10 g printed; the connection is tool-free and re-usable. The thread geometry (M20-pitch-4) is reused by the X-frame hinge bracket and top bracket in later phases.
