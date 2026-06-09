# Plan

## 1. Parameters Update
1. Update `params.py` with stadium profile dimensions (25x15mm, 3mm wall).
2. Update `params.py` with square transition length (20mm) and adapter pin length (50mm, 25mm per side).

## 2. Threaded Adapter Pin (`part_07_threaded_adapter_pin.py`)
1. Create a script to generate a 50mm long male-to-male threaded pin.
2. The pin should have threads on both halves, matching `PEG_THREAD_RADIUS` and `PEG_THREAD_PITCH`, mirroring the existing leg peg design.
3. Export STEP and STL for validation.

## 3. Universal Drying Rod (`part_06_drying_rod.py`)
1. Construct the stadium profile (25x15mm outer, 19x9mm inner for 3mm wall).
2. Construct the square profile matching the leg cross-section (`LEG_WIDTH` x `LEG_DEPTH`).
3. Create a swept transition from the stadium profile to the square profile over 20mm.
4. Integrate the male threaded peg at one end and the female threaded socket at the other.
5. Ensure complex sweeps and threads are generated at the origin before placement.
6. Export STEP and STL for validation.

## 4. Assembly & Visual Validation
1. Add `part_06_drying_rod` and `part_07_threaded_adapter_pin` to `assembly.py` to confirm they fit seamlessly with the existing T-bracket and frame parts.
2. Execute the FreeCAD Visual Validation skill (`freecad-visual-validation`) to generate assembly and component renders.
3. Review the validation report and rendered images to ensure correct alignment and no interferences.
