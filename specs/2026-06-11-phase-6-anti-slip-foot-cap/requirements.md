# Requirements

## Scope
Implement `part_08_foot_cap.py` as an anti-slip foot cap that slides over the rectangular segment body ends of the clothes drying rack.

## Decisions
- Overlap/Slide-over depth: 15mm
- Wall thickness: 2mm
- Base grip: Recessed grid/tread pattern to increase friction and improve stability.
- Fit: Use standard clearance for a press-fit over the leg (e.g. 0.2mm clearance).

## Constraints
- Must be a single manifold part fully printable without supports.
- Print orientation: Flat on the base.
- Must fit within clearance rules from `tech-stack.md`.

## Non-goals
- Articulated or flexible TPU feet (design is for standard rigid FDM like PLA/PETG).
- Simulation of physical load or friction.

## Context
Phase 6 from the roadmap. The foot cap provides stability for the deployed X-frame and prevents the plastic leg segments from sliding on smooth floors or scratching them.
