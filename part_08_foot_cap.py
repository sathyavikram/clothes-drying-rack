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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_08_foot_cap.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_08_foot_cap.stl")

def construct_foot_cap():
    overlap_depth = 15.0 * params.SCALE
    wall = 2.0 * params.SCALE
    base_thickness = 4.0 * params.SCALE
    total_height = overlap_depth + base_thickness
    
    # Inner dimensions with press-fit clearance
    inner_w = params.LEG_WIDTH + 2 * params.TOLERANCE_PRESS
    inner_d = params.LEG_DEPTH + 2 * params.TOLERANCE_PRESS
    
    # Outer dimensions
    outer_w = inner_w + 2 * wall
    outer_d = inner_d + 2 * wall
    
    # Base Box
    body = Part.makeBox(outer_w, outer_d, total_height)
    body.Placement.Base = App.Vector(-outer_w/2, -outer_d/2, 0)
    
    # Fillet outer edges
    try:
        body = body.makeFillet(2.0 * params.SCALE, body.Edges)
    except Exception as e:
        print("Warning: outer fillet failed", e)
        pass
    
    # Inner cavity (to cut out)
    cavity = Part.makeBox(inner_w, inner_d, overlap_depth + 1.0) # +1.0 so it cuts completely through top
    cavity.Placement.Base = App.Vector(-inner_w/2, -inner_d/2, base_thickness)
    
    # Fillet inner cavity vertical edges to match leg segment's fillets
    try:
        cavity = cavity.makeFillet(2.0 * params.SCALE, cavity.Edges)
    except Exception as e:
        print("Warning: cavity fillet failed", e)
        pass
        
    body = body.cut(cavity)
    
    # Add a chamfer to the inner opening to guide the leg in
    try:
        chamfer = Part.makeBox(inner_w + 2.0, inner_d + 2.0, 1.0)
        chamfer.Placement.Base = App.Vector(-(inner_w+2.0)/2, -(inner_d+2.0)/2, total_height - 0.5)
        # Create a pyramidal frustum or just a simple chamfer box using a larger box at the very top.
        # OpenCASCADE chamfer is safer:
        # body = body.makeChamfer(1.0, ... edges) - can be brittle.
        # We will skip the inner chamfer to keep it simple and robust, the press fit tolerance is enough.
    except:
        pass
    
    # Tread pattern on bottom (Z = 0)
    # We will cut a grid of 2mm wide, 1.5mm deep grooves
    groove_width = 2.0 * params.SCALE
    groove_depth = 1.5 * params.SCALE
    
    grooves = []
    # X-direction grooves
    start_pos = -outer_w/2 + 5.0
    end_pos = outer_w/2 - 5.0
    num_grooves = 4
    step = (end_pos - start_pos) / (num_grooves - 1) if num_grooves > 1 else 0
    
    for i in range(num_grooves):
        pos = start_pos + i * step
        g = Part.makeBox(groove_width, outer_d - 4.0, groove_depth + 0.1)
        g.Placement.Base = App.Vector(pos - groove_width/2, -outer_d/2 + 2.0, -0.1) # -0.1 to guarantee cut
        grooves.append(g)
        
    # Y-direction grooves
    start_pos_y = -outer_d/2 + 5.0
    end_pos_y = outer_d/2 - 5.0
    step_y = (end_pos_y - start_pos_y) / (num_grooves - 1) if num_grooves > 1 else 0
    for i in range(num_grooves):
        pos = start_pos_y + i * step_y
        g = Part.makeBox(outer_w - 4.0, groove_width, groove_depth + 0.1)
        g.Placement.Base = App.Vector(-outer_w/2 + 2.0, pos - groove_width/2, -0.1)
        grooves.append(g)
        
    if grooves:
        cutter = Part.makeCompound(grooves)
        body = body.cut(cutter)
        
    # Print orientation: The cap prints flat on its base (Z=0).
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    body.exportStep(EXPORT_STEP)
    body.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return body

def main():
    doc = App.newDocument("FootCap")
    shape = construct_foot_cap()
    feature = doc.addObject("Part::Feature", "FootCap")
    feature.Shape = shape

if __name__ == "__main__":
    main()
