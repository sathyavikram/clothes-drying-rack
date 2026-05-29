import FreeCAD as App
import Part
import Import
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    sys.path.append(os.getcwd())
    pass

import params
import importlib
importlib.reload(params)

import part_01_leg_tube
import part_01b_tube_sleeve

CURRENT_DIR = os.getcwd()
EXPORT_BASE  = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP  = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "assembly.stl")

def clear_exports():
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for f in os.listdir(EXPORT_BASE):
        if f.endswith(".step") or f.endswith(".stl"):
            try:
                os.remove(os.path.join(EXPORT_BASE, f))
            except OSError:
                pass

def load_step(filename):
    shape = Part.Shape()
    shape.read(os.path.join(EXPORT_BASE, filename))
    return shape

def assemble_leg():
    # Number of segments to reach ~1300 mm (1320 mm actual)
    num_segments = 6
    num_sleeves  = num_segments - 1

    # Ensure parts exist
    part_01_leg_tube.construct_leg_tube()
    part_01b_tube_sleeve.construct_tube_sleeve()

    doc = App.newDocument("Assembly")
    
    tube_shape = load_step("part_01_leg_tube.step")
    # Invert the exact placement applied in part_01_leg_tube.py
    # P1: Translate Z by TUBE_OD/2, then rotate Y by 90
    P1 = App.Placement(App.Vector(0,0,params.TUBE_OD/2), App.Rotation(App.Vector(0,1,0), 90))
    # P2: Rotate Z by 45
    P2 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 45))
    P_orig = P2.multiply(P1)
    base_placement = P_orig.inverse()
    
    sleeve_shape = load_step("part_01b_tube_sleeve.step")

    shapes = []
    
    current_z = 0.0

    for i in range(num_segments):
        # We place a tube
        # Tube original center was at 0,0,0 and went along Z. It has top and bot spigots starting at -25 and +170
        t_feat = doc.addObject("Part::Feature", f"LegTube_{i}")
        if t_feat.ViewObject:
            t_feat.ViewObject.ShapeColor = (0.20, 0.40, 0.80)
        
        # The tube will now be back to exactly how its creation script initially made it (from Z=0 to +body_len)
        # Shift it up to current_z
        z_shift = App.Placement(App.Vector(0, 0, current_z), App.Rotation())
        
        t_feat.Placement = z_shift.multiply(base_placement)
        t_feat.Shape = tube_shape
        shapes.append(t_feat.Shape.copy().transformGeometry(t_feat.Placement.toMatrix()))
        
        current_z += params.SEGMENT_BODY_LENGTH
        
        if i < num_sleeves:
            # We place a sleeve
            # Sleeve origin is at bottom face. Sleeve is 60 mm long.
            # Its bottom face must sit exactly at current_z + params.SPIGOT_LENGTH - params.SLEEVE_LENGTH
            # Wait, the sleeve takes the top spigot (25mm) and the next tube's bottom spigot (25mm)
            # The top spigot of the previous tube is from `current_z` to `current_z + 25`.
            # A sleeve is 60mm long. The bottom bore is 25mm deep. The top bore is 25mm deep. Central wall is 10mm.
            # So the sleeve's bottom face starts at `current_z` minus the bottom bore depth?
            # No, if the spigot goes 25mm into the sleeve's bottom bore, the sleeve's bottom face is at `current_z`.
            # Wait, let's see. The tube's body ends at `current_z`. The top spigot sticks out 25mm above it.
            # The sleeve's bottom face sits flush against the tube's body end.
            # So the sleeve's bottom face is at `current_z`.
            s_feat = doc.addObject("Part::Feature", f"TubeSleeve_{i}")
            if s_feat.ViewObject:
                s_feat.ViewObject.ShapeColor = (0.80, 0.40, 0.20)
            s_feat.Placement = App.Placement(App.Vector(0, 0, current_z), App.Rotation())
            s_feat.Shape = sleeve_shape
            shapes.append(s_feat.Shape.copy().transformGeometry(s_feat.Placement.toMatrix()))
            
            # Next tube starts at current_z + sleeve's length
            current_z += params.SLEEVE_LENGTH

    compound = Part.makeCompound(shapes)
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    if os.path.exists(EXPORT_STEP): os.remove(EXPORT_STEP)
    if os.path.exists(EXPORT_STL): os.remove(EXPORT_STL)
    
    compound.exportStep(EXPORT_STEP)
    compound.exportStl(EXPORT_STL)
    
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    print(f"Assembly full length: {current_z + params.SPIGOT_LENGTH}") # Top spigot of last tube
    
    return doc

def main():
    clear_exports()
    assemble_leg()

if __name__ == "__main__":
    main()
