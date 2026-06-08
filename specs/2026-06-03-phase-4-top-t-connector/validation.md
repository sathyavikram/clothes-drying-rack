# Validation

## Required Checks
- [x] Export `part_05_top_t_bracket` as STEP and STL.
- [x] Ensure the generated STL is manifold (zero non-manifold edges).

## Manual Review
- [x] Visual inspection of the threaded joints connecting the bracket to the horizontal rod and X-frame leg.
- [x] Verification that threaded timing results in perfectly flush profile alignment between the rectangular sections when fully tightened.
- [x] Verify that the angle between the stem and the crossbar perfectly matches the required deployed leg angle (65°).

## Merge Criteria
- [x] Visual validation confirmed the T-bracket is correctly positioned in the deployed assembly.
- [x] Code passes basic tests (`python params.py` / `./run.sh assembly`).
