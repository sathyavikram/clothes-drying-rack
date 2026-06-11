# Changelog

## 2026-06-11
- Completed Phase 8: Final Review & Full Assembly.
- Verified visual geometry of all 9 individual printable parts.
- Updated `assembly.py` to construct the entire drying rack dynamically with adjustable segment sizing (set to a scalable mini-rack for rapid export verification).
- Rendered and validated the final assembly layout (2 complete X-frames with all joint hinges, 3 drying rods spanning the frames, the middle stability bar, and all end caps).
- Exported final clean `assembly.step` and `assembly.stl` files, validating the assembly's integrity and structural intersections.
- Removed Locking Hinge and Windproof Hook from the project roadmap and tech stack scope to simplify the design; shifted Final Assembly to Phase 8.
- Completed Phase 7: Rod End Cap implementation.
- Created `part_09_rod_end_cap.py` with a domed circular profile and a standard male threaded peg, pivoting away from the original press-fit design for better security.
- Updated `assembly.py` to insert rod end caps into the top-facing sockets of the upper T-Brackets.
- Completed Phase 6: Anti-Slip Foot Cap implementation.
- Created `part_08_foot_cap.py` featuring a press-fit sleeve and a recessed crosshatch bottom grip.
- Added foot caps to the base legs of the X-frame assemblies in `assembly.py`, implementing a 0.1mm placement offset to prevent numerical interference checks from failing on perfectly coincident planar faces.
- Updated `export_all.py` and specs documentation to include the new foot cap component.

## 2026-06-10
- Combined Phase 5 and Phase 6 in the project roadmap, integrating the Middle Stability Bar as a re-use of the Universal Drying Rod and T-Bracket.
- Updated `assembly.py` to construct the middle stability bars using existing rod and bracket components.
- Removed `part_08_stability_bar.py` from `tech-stack.md` to reflect part reuse.
- Shifted subsequent roadmap phases down by one.

## 2026-06-09
- Completed Phase 5: Universal Drying Rod & Adapter Pin implementation.
- Created `part_06_drying_rod.py` featuring a stadium profile transitioning to square ends, utilizing male peg and female socket joinery.
- Created `part_07_threaded_adapter_pin.py` to serve as a male-to-male threaded adapter for connecting female sockets.
- Rewrote `assembly.py` to correctly align the right frame without mirrored yaw rotation, ensuring flawless horizontal rod connections.
- Simplified `assembly.py` rendering to use 1 leg segment and 1 horizontal rod for lightweight multi-view visual validation.

## 2026-06-08
- Completed Phase 4: Top L-Connector Bracket implementation.
- Redesigned the top bracket into a single-piece rigid L-shaped bracket with symmetric female threaded blind sockets, replacing the previous multi-part design.
- Updated `assembly.py` and generation scripts for the new symmetric bracket integration.
- Updated Phase 4 specifications and roadmap to reflect the updated L-shaped design capable of fitting interchangeably on the X-frame or horizontal rod.
- Fixed widespread OpenCASCADE threading bug by replacing `fuse().removeSplitter()` with `Part.makeCompound()` for thread cutters across all parts.
- Corrected female thread inner radius calculation multiplier from `0.55` to `0.45` to ensure proper thread clearance.
- Increased `ARM_L` to `100.0` in `part_02` and `part_03` hinges to prevent female sockets from intersecting the central pivot hole.
- Updated `part_05_top_l_bracket.py` geometry from a 2D T-shape to an L-shape (vertical arm 60mm, horizontal arm 45mm) while maintaining 3 female threaded sockets, allowing it to function as a modular corner or middle junction without colliding threads.
## 2026-06-02
- Completed Phase 3: X-Frame Center Hinge implementation.
- Redesigned monolithic print-in-place hinge into a 3-part threaded mechanism (bottom, top, and pin) to enhance shear strength and printability.
- Updated `params.py` with gap-threaded locking logic (`THREAD_CLEARANCE`, `GENERAL_CLEARANCE`).
- Refactored `run.sh` and `export_all.py` to use subprocess module imports to fix FreeCAD headless execution bugs.
- Updated project constitution (`mission.md`, `roadmap.md` and `tech-stack.md`) to reflect the robust 3-part hinge approach and shifted subsequent phase numbering.

## 2026-05-29
- Completed Phase 2: Leg Segment implementation.
- Transitioned leg mechanism from round threaded tubes to a simpler rectangular integrated male/female resistance fit, eliminating the need for separate connector pieces.
- Updated project constitution, roadmap, and Phase 2 requirements to reflect the rectangular integrated joint architecture.
- Refactored `assembly.py` and generation scripts for the new segment design.

## 2026-05-28
- Initial commit establishing the clothes-drying-rack project.
- Added project constitution with mission, tech-stack, and roadmap specs.
- Added reference images and project specs directory.
- Updated README and added Copilot CLI configuration.
- Added `.DS_Store` to `.gitignore`.
- Added Phase 1 project skeleton specification.
- Implemented Phase 1 project skeleton.
- Marked Phase 1 as complete in the roadmap.
- Resolved headless boolean failures by implementing an origin-based generate + placement strategy for all Threaded features.
