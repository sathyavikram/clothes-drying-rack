# Requirements

## Scope
Implement Phase 5 from the roadmap: Universal Drying Rod and Threaded Adapter Pin. These parts will be used for the horizontal drying rods across the clothes rack.

## Decisions
- **Stadium Profile**: 25mm width, 15mm height, 3mm wall thickness.
- **Square Transition**: The rod will transition from the stadium profile to a square profile matching the leg cross-section (`LEG_WIDTH` x `LEG_DEPTH` = 25x25mm) over a length of 20mm.
- **Adapter Pin**: 50mm overall length (25mm per side). Used to connect two female sockets.

## Constraints
- Max length for any printed segment is 220mm (based on the 175x175mm diagonal).
- Parts must use the standard timed threading geometry for seamless alignment.
- Must be printable without mandatory support (overhangs ≤ 45°).
- Complex sweeps and threads must be created at the origin and fused before repositioning, as per the tech-stack guide.

## Non-goals
- Generating the final, complete 100% rack assembly (handled in Phase 11). We will only add and position the Phase 5 parts into the current working `assembly.py` to validate their fit and clearances.
- Simulating bending/load stresses on the rods.

## Context
These parts must universally fit together and with the T-Bracket designed in Phase 4. The modularity allows us to build the entire top/middle rails out of repeating copies of `part_06_drying_rod.py` and `part_07_threaded_adapter_pin.py`.
