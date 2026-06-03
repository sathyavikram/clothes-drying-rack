# Validation

## Required Checks
- [ ] Export `part_05_top_bracket_rod_mount` as STEP and STL.
- [ ] Export `part_06_top_bracket_leg_mount` as STEP and STL.
- [ ] Export `part_07_top_bracket_pin` as STEP and STL.
- [ ] Ensure all generated STLs are manifold (zero non-manifold edges).

## Manual Review
- [ ] Visual inspection of the threaded joints connecting the bracket to the horizontal rod and X-frame leg.
- [ ] Verification that threaded timing results in perfectly flush profile alignment between the rectangular sections when fully tightened.

## Merge Criteria
- [ ] Using the **freecad-visual-validation agent**, validate both the fully open (deployed) state and the fully closed (flat) state.
- [ ] Visual validation must confirm there are zero geometric collisions during the fold, and the joint functions mechanically.
- [ ] Code passes basic tests (`python params.py` / `python export_all.py`).
