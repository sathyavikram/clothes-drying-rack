# Requirements

## Scope
- Create a 3D-printable Rod End Cap (`part_09_rod_end_cap.py`) to finish the exposed ends of the horizontal drying rods.
- Integrate the newly designed part into the main assembly file.

## Decisions
- **Threaded Joinery**: In a shift from the initial roadmap design (press-fit), the end cap will use a standard male threaded peg to screw securely into the existing female rod sockets.
- **Visual Design**: The cap's external profile will match the stadium (pill) shape of the drying rod, but feature a slightly domed (convex) end face to provide a premium, polished aesthetic.

## Constraints
- The outer dimensions of the cap body must strictly match the stadium profile generated in `part_06_drying_rod.py`.
- The male thread must follow standard conventions defined in `params.py` (using `PEG_THREAD_RADIUS`, `PEG_THREAD_PITCH`, `THREAD_CLEARANCE`, and `PEG_LENGTH`).
- The domed face should be shallow enough to print easily without requiring internal supports.

## Non-goals
- We will not implement a flat or flush press-fit design.
- The end cap will not support load-bearing structural extensions.

## Context
- The user requested that the part feature a convex dome for aesthetics and be screwable into the existing female hole logic to guarantee a secure fit, abandoning the previous friction-fit concept.
