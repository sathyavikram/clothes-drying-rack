# Plan

## 1. Parameters & Configuration
1. Update `params.py` with bounding box dimensions and clearances for the threaded hinge bracket (e.g., `THREAD_CLEARANCE = 0.6 * SCALE`).
2. Define the exact dimensions for the fully printed threaded pin mechanism.

## 2. Base Body & Leg Cutouts
1. Create `part_02_xframe_hinge_bottom.py` (Bottom piece with a female threaded socket) and `part_03_xframe_hinge_top.py` (Top piece with a smooth through-hole).
2. Design the core block arms to encompass both legs at the cross pivot point.
3. Apply boolean cuts using `LEG_WIDTH` and `LEG_DEPTH` (plus `FIT_CLEARANCE`) to form the sandwiching sockets. Add a rotational slot array for the stop mechanisms.

## 3. Fully Printed Threaded Pivot Pin
1. Create `part_04_xframe_hinge_pin.py`. Instead of a print-in-place mechanism, design an M16-equivalent threaded pin with a flat head.
2. The pin must feature a chamfered threaded tip, a smooth shaft for the top arm to pivot on, and a slot for a coin or screwdriver.
3. Crucial: Orient and slice a micro-flat spot on the pin so it can be printed horizontally lying down for maximal layer shear strength.
4. Ensure the threaded clearance and the hole depth in the bottom bracket interact properly without bottoming out.

## 4. Exports & Assembly Hookup
1. Ensure the individual scripts run via `freecadcmd -c ...` to export STEP and STL files securely.
2. Update `assembly.py` and `export_all.py` to compile the 3 hinge pieces plus the leg parts, and map their precise Placements so the pin locks the arms together tightly.
