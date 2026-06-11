# Plan

## Task Group 1: Basic Sleeve Geometry
1. Define parameters for cap depth (15mm) and wall thickness (2mm).
2. Create the base hollow rectangular profile that slides over the leg segment (`LEG_WIDTH` x `LEG_DEPTH`).
3. Add clearance (`FIT_CLEARANCE` or similar press-fit tolerance) so it fits snugly over the leg.

## Task Group 2: Base Texture/Grip
1. Create a recessed grid/tread pattern on the solid bottom base.
2. Apply chamfers/fillets to the outer bottom edges to avoid sharp corners.
3. Combine the base and sleeve into a single solid part.

## Task Group 3: Assembly Integration and Testing
1. Add `part_08_foot_cap.py` to the build scripts.
2. Integrate the foot cap into `assembly.py` at the 4 leg ends.
3. Export STL and STEP files.
