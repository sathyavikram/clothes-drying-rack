# Requirements

## Scope
- Replace the complex 3-part pivoting bracket with a single, rigid, 3D-printable T-shaped bracket (`part_05_top_t_bracket.py`).
- **Stem:** Connects rigidly to the X-frame leg.
- **Crossbar:** Connects rigidly to the upper horizontal rod.

## Decisions
- The bracket will be one solid piece.
- The stem will be permanently angled relative to the crossbar to match the deployed angle of the X-frame legs.
- By building the deployment angle into the bracket, the rectangular horizontal rods will sit perfectly flat and horizontal when the rack is deployed. When folded, the rods will tilt, which is acceptable for flat storage.
- Same threaded joinery used for leg segments will be used to attach the bracket to the legs and rods (using timed threads so outer rectangular profiles align seamlessly).

## Constraints
- Max footprint must fit within 175 × 175 × 175 mm bed diagonally (the part will be small and easily fit).
- The assembly must result in horizontal rods that are 0 degrees relative to the ground when the legs are fully deployed.

## Non-goals
- Color/texture rendering details.
- Hinge mechanics at the top corners (no longer needed).

## Context
See Phase 4 of `specs/roadmap.md`. The goal is to make the joint as strong and simple as possible while solving the rectangular rod twisting issue via a built-in angle.
