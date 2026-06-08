# Requirements

## Scope
- Design the X-Frame Center Hinge brackets into 3 separate parts: Bottom bracket (`part_02_xframe_hinge_bottom.py`), Top bracket (`part_03_xframe_hinge_top.py`), and a Threaded Locking Pivot Pin (`part_04_xframe_hinge_pin.py`).
- Create a cross-pivot pairing at the midpoint of the X-frame to allow the legs to scissor and fold flat.
- Provide a fully 3D printable, multi-part threaded pivot mechanism (no external metal hardware).

## Decisions
- **Three-Part Sandwich Design:** The hinge bracket is split into top and bottom mating layers holding the two crossing leg segments inside for maximum structural support, moving away from a weak print-in-place joint.
- **Printed Threaded Pin:** A custom threaded pivot pin connects the top bracket to the bottom bracket. To prevent snapping under shear loads, the pin is printed lying perfectly flat on the print bed so its layer lines run along its length.
- **Parametric:** Must use dimensions established in `params.py` (e.g., `LEG_WIDTH`, `LEG_DEPTH`, `THREAD_CLEARANCE`). 
- **Tight Folding Resistance:** The X folding motion must be tight and have resistance, controlled by tightening the threaded pin assembly. The pivot uses an M16-equivalent threaded joint.

## Constraints
- Max part size must fit diagonally within a 175x175x175mm FDM printer (the hinge bracket falls well below this).
- Do not use metal or external bolts; must be 100% 3D printable plastic.
- Must export manifold geometry (0 non-manifold edges).

## Non-goals
- Do not make the pin permanently unremovable; it must be tool-free removable for maintenance/transport.
- Do not add external metal hardware; the design is 100% printable plastic.

## Context
- This phase implements Phase 3 from the roadmap.
- This hinge is central to the scissor action allowing the rack to be stored flat.
