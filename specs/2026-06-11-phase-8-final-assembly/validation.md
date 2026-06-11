# Validation

## Required Checks
- **Individual Part Check**: Render and inspect each `part_XX.step` from multiple angles.
- **Incremental Check**: As parts are added to `assembly.py`, run `check_interference` and visual renders to confirm fit.
- **Final Assembly Dimensions**: Check the bounding box dimensions of the final `assembly.step` to confirm it matches the intended minimum deployed state (~1300mm length).

## Manual Review
- Carefully review rendered images of joints (e.g., cross-sections of threaded connections).
- Review overall isometric render of the full assembly to ensure no missing components or strange visual gaps.

## Merge Criteria
- All 9 parts pass individual visual inspection.
- The full assembly exports cleanly to `.step` and `.stl` without OpenCASCADE boolean failures.
- No severe interferences exist in the final build (minus expected mathematical margin touches).
