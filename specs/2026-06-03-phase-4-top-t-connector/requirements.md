# Requirements

## Scope
- Replace the monolithic top static T-bracket in the roadmap with a 3-part fully 3D-printable, fully threaded folding joint.
- **Part 05 (Rod Mount):** Rigidly attaches to the upper horizontal rod. Contains the female structural threads for the pivot.
- **Part 06 (Leg Mount):** Rigidly attaches to the X-frame leg. Contains the clearance bore for the pivot.
- **Part 07 (Pivot Pin):** Connects parts 05 and 06 with male threads.

## Decisions
- The pivot logic (clearance holes, threaded pin) will mirror the logic validated in Phase 3 (X-Frame Center Hinge).
- Same threaded joinery used for leg segments will be used here to attach the brackets to the rods (using timed threads so outer rectangular profiles align seamlessly).
- The parts must be 100% 3D printable on an FDM printer without non-printable metal hardware. 

## Constraints
- Max footprint per part must fit within 175 × 175 × 175 mm bed diagonally (these parts will be small and easily fit).
- The assembly must allow the leg to fold parallel (or nearly parallel) to the top bar for flat storage.
- Must avoid mechanical binding when moving from 0 degrees (folded flat) to the deployed angle (typically ~45 degrees off vertical depending on leg spread).

## Non-goals
- Color/texture rendering details.
- Articulated structural simulation. We are only concerned with rigid-body clearance tests.

## Context
See Phase 4 of `specs/roadmap.md` and Phase 3 pin design patterns. The goal is to make the joint as strong as possible while allowing full collapsibility.
