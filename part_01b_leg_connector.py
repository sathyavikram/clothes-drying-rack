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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_01b_leg_connector.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_01b_leg_connector.stl")

def construct_leg_connector():
    w = params.CONNECTOR_WIDTH
    d = params.CONNECTOR_DEPTH
    l = params.CONNECTOR_LENGTH
    
    # Base Box
    body = Part.makeBox(w, d, l)
    body.Placement.Base = App.Vector(-w/2, -d/2, -l/2)
    
    # Holes at both sides with friction fit clearance
    hole_w = params.PEG_WIDTH + params.FIT_CLEARANCE * 2
    hole_d = params.PEG_DEPTH + params.FIT_CLEARANCE * 2
    hole_l = params.CONNECTOR_BORE_DEPTH
    
    hole1 = Part.makeBox(hole_w, hole_d, hole_l + params.SCALE)
    hole1.Placement.Base = App.Vector(-hole_w/2, -hole_d/2, l/2 - hole_l)
    
    hole2 = Part.makeBox(hole_w, hole_d, hole_l + params.SCALE)
    hole2.Placement.Base = App.Vector(-hole_w/2, -hole_d/2, -l/2 - params.SCALE)
    
    shape = body.cut(hole1).cut(hole2).removeSplitter()
    
    # Print orientation: standing upright
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape


def main():
    doc = App.newDocument("LegConnector")
    shape = construct_leg_connector()
    feature = doc.addObject("Part::Feature", "LegConnector")
    feature.Shape = shape


if __name__ == "__main__":
    main()
