# Plan

## Task Group 1: Configuration
1. Update `params.py` to include thread parameters (pitch, minor/major diam) and tube diameters (outer/inner) if they don't already exist.
2. Verify `params.py` runs without errors.

## Task Group 2: Tube Geometry
1. Calculate the exact maximum length for diagonal placement: 
   - Formula: $L \le A\sqrt{2} - W$ (where A = build plate side, W = outer diameter)
   - Using 175 mm (for safe margin bounds) and a 25 mm OD: $175 \times 1.414 - 25 = 247.48 - 25 = 222.48$ mm.
   - Implement the main base geometry for a single straight hollow round tube segment using a safe dimension of **220 mm**.
2. Configure the ends to accommodate threaded joints. 

## Task Group 3: Threaded Clamp Geometry
1. Implement male/female threads for segment-to-segment joining using FreeCAD's advanced thread generation (e.g., makeHelix/makePipeShell).
2. Create the rounded clamp featuring female threads.

## Task Group 4: Assembly
1. Create `assembly.py` for this phase to assemble the full leg from multiple `part_01_leg_tube.py` instances.
2. Join the segments using the threaded joints.

## Task Group 5: Verification
1. Export STEP and STL files for the individual part and the assembly.
2. Run visual validation using the MCP tool.
