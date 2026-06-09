# Requirements

## Scope
- Replace the complex 3-part pivoting bracket with a single, rigid, 3D-printable Universal T-shaped bracket (`part_05_top_l_bracket.py`) featuring 3 identical female sockets.
- **Top/Bottom Sockets:** Connect inline with X-frame leg segments (using male-to-male adapter pins if continuing upwards), or cap the leg at the top.
- **Side Socket:** Connects rigidly to the horizontal drying rod.

## Decisions
- The bracket will be one solid modular piece.
- The side socket will be permanently angled relative to the vertical leg axis to match the deployed angle of the X-frame legs.
- By building the deployment angle into the bracket, the stadium-shaped horizontal rods will sit perfectly flat and horizontal when the rack is deployed. When folded, the rods will tilt, which is acceptable for flat storage.
- All three ports use identical timed female threads. This creates a fully modular Universal T-bracket that can be used anywhere a horizontal rod needs to branch off a leg.

## Constraints
- Max footprint must fit within 175 × 175 × 175 mm bed diagonally (the part will be small and easily fit).
- The assembly must result in horizontal rods that are 0 degrees relative to the ground when the legs are fully deployed.

## Non-goals
- Color/texture rendering details.
- Hinge mechanics at the top corners (no longer needed).

## Context
See Phase 4 of `specs/roadmap.md`. The goal is to make the joint as strong and simple as possible while solving the rectangular rod twisting issue via a built-in angle.
