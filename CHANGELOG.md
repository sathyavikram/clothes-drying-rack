# Changelog

## 2026-06-08
- Completed Phase 4: Top L-Connector Bracket implementation.
- Redesigned the top bracket into a single-piece rigid L-shaped bracket with symmetric female threaded blind sockets, replacing the previous multi-part design.
- Updated `assembly.py` and generation scripts for the new symmetric bracket integration.
- Updated Phase 4 specifications and roadmap to reflect the updated L-shaped design capable of fitting interchangeably on the X-frame or horizontal rod.
- Fixed widespread OpenCASCADE threading bug by replacing `fuse().removeSplitter()` with `Part.makeCompound()` for thread cutters across all parts.
- Corrected female thread inner radius calculation multiplier from `0.55` to `0.45` to ensure proper thread clearance.
- Increased `ARM_L` to `100.0` in `part_02` and `part_03` hinges to prevent female sockets from intersecting the central pivot hole.
- Updated `part_05_top_t_bracket.py` geometry from a 2D T-shape to an L-shape (vertical arm 60mm, horizontal arm 45mm) while maintaining 3 female threaded sockets, allowing it to function as a modular corner or middle junction without colliding threads.
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
