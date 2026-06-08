# Plan

## 1. Parameters & Configuration
- Update `params.py` with bounding box dimensions and clearances for the threaded hinge bracket (e.g., `THREAD_CLEARANCE = 0.6 * SCALE`).
- Define the exact dimensions for the fully printed threaded pin mechanism.

## 2. Base Body & Leg Cutouts
- Create `part_02_xframe_hinge_bottom.py` (Bottom piece with a female threaded socket for the pin) and `part_03_xframe_hinge_top.py` (Top piece with a smooth through-hole).
- Design the core block arms to encompass both legs at the cross pivot point.
- Incorporate timed male threaded pegs and corresponding timed female threaded sockets along the arm segments for connecting natively to the Phase 2 threaded leg segments. Add a rotational slot array for the stop mechanisms.

## 3. Fully Printed Threaded Pivot Pin
- Create `part_04_xframe_hinge_pin.py`. Instead of a print-in-place mechanism, design an M16-equivalent threaded pin with a flat head.
- The pin must feature a chamfered threaded tip, a smooth shaft for the top arm to pivot on, and a slot for a coin or screwdriver.
- Crucial: Orient and slice a micro-flat spot on the pin so it can be printed horizontally lying down for maximal layer shear strength.
- Ensure the threaded clearance and the hole depth in the bottom bracket interact properly without bottoming out.

## 4. Exports & Assembly Hookup
- Ensure the individual scripts run via `freecadcmd -c ...` to export STEP and STL files securely.
- Update `assembly.py` and `export_all.py` to compile the 3 hinge pieces plus the leg parts, and map their precise Placements so the pin locks the arms together tightly.
