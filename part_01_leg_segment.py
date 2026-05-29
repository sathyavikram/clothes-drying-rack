import FreeCAD as App
import Part
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE  = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_01_leg_segment.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_01_leg_segment.stl")


def construct_leg_segment():
    w = params.LEG_WIDTH
    d = params.LEG_DEPTH
    l = params.SEGMENT_BODY_LENGTH
    wall = params.LEG_WALL
    
    # Body (Hollow Rectangular)
    outer_box = Part.makeBox(w, d, l)
    outer_box.Placement.Base = App.Vector(-w/2, -d/2, -l/2)
    
    inner_w = w - 2*wall
    inner_d = d - 2*wall
    inner_box = Part.makeBox(inner_w, inner_d, l + 2*params.SCALE)
    inner_box.Placement.Base = App.Vector(-inner_w/2, -inner_d/2, -(l + 2*params.SCALE)/2)
    
    body = outer_box.cut(inner_box)
    
    # Pegs (Solid Rectangular at both ends)
    peg_w = params.PEG_WIDTH
    peg_d = params.PEG_DEPTH
    peg_l = params.PEG_LENGTH
    
    peg1 = Part.makeBox(peg_w, peg_d, peg_l)
    peg1.Placement.Base = App.Vector(-peg_w/2, -peg_d/2, l/2)
    
    peg2 = Part.makeBox(peg_w, peg_d, peg_l)
    peg2.Placement.Base = App.Vector(-peg_w/2, -peg_d/2, -l/2 - peg_l)
    
    # Chamfer peg ends for easy insertion
    # (To keep it simple and robust, standard pegs without chamfers for now, as it might fail on edge selection)
    
    shape = body.fuse(peg1).fuse(peg2).removeSplitter()
    
    # Print orientation: lying flat on the long face (horizontal).
    # Currently Z is the long axis. We rotate about X by 90 deg so it lies flat on XY plane
    shape.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90)

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape


def main():
    doc = App.newDocument("LegSegment")
    shape = construct_leg_segment()
    feature = doc.addObject("Part::Feature", "LegSegment")
    feature.Shape = shape


if __name__ == "__main__":
    main()
