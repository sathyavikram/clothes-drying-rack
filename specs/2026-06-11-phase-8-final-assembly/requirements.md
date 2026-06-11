# Requirements

## Scope
- Conduct a rigorous final review of all 9 parts and build the complete clothes drying rack assembly.

## Decisions
- The assembly code will live entirely in `assembly.py`, directly constructing the complete rack without separated sub-assembly script files.
- The horizontal rods will be composed of 2 to 3 rod segments threaded together to visually and geometrically represent the segmented structure, saving rendering/export time over a full 5-6 segment rod.
- The rack will be constructed in its Minimum Deployed State (~51.1" footprint width).
- Visual validation will be extremely thorough, inspecting parts in different views and configurations before finalizing.

## Constraints
- Do not exceed memory limits or execution timeouts when exporting the final full assembly (which is why rods are shortened to 2-3 segments).

## Non-goals
- Articulated or animated kinematics.
- Simulating the fully extended 79" state.
- Physical stress testing.
