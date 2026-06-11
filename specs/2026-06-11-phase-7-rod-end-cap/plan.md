# Plan

## Task Group 1: Part Creation (`part_09_rod_end_cap.py`)
1. Implement the base cap geometry matching the universal rod's stadium profile.
2. Add a slightly domed (convex) outer face for a polished visual finish.
3. Replace the originally planned press-fit plug with a standard timed male threaded peg.
4. Ensure the threading generates at the origin (`App.Vector(0,0,0)`) wrapped in `Part.Solid()` before positioning, per the tech stack conventions.
5. Setup the standard parametric export pipeline in the script.

## Task Group 2: Assembly Integration
1. Update `assembly.py` to position the new rod end caps at all exposed, open female sockets on the horizontal drying rods.
2. Ensure placement logic successfully handles the domed geometry and aligns the stadium profile seamlessly with the connected rod.
3. Update `export_all.py` to execute `part_09_rod_end_cap.py`.

## Task Group 3: Validation
1. Render individual part views via FreeCAD visual validation tools.
2. Re-export the full `assembly.step`.
3. Run `check_interference` on the assembly to confirm the threaded peg perfectly mates with the existing rod female sockets without unexpected overlapping.
