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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_03_xframe_hinge_top.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_03_xframe_hinge_top.stl")

def construct_hinge_top():
    LEG_W = params.LEG_WIDTH
    LEG_D = params.LEG_DEPTH
    PEG_W = params.PEG_WIDTH
    PEG_D = params.PEG_DEPTH
    PEG_L = params.PEG_LENGTH
    INNER_W = LEG_W - 2*params.LEG_WALL
    INNER_D = LEG_D - 2*params.LEG_WALL
    
    HUB_R = 20.0 * params.SCALE
    HUB_H = 25.0 * params.SCALE
    ARM_L = 80.0 * params.SCALE
    ARM_EXT = ARM_L / 2.0
    
    z_B = 0.0 # Printed flat on Z=0
    hub_B = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0,0,z_B), App.Vector(0,0,1))
    body_B = Part.makeBox(LEG_W, ARM_L, LEG_D, App.Vector(-LEG_W/2, -ARM_EXT, z_B))
    
    # Male Peg at +Y
    peg_B = Part.makeBox(PEG_W, PEG_L, PEG_D, App.Vector(-PEG_W/2, ARM_EXT, z_B + (LEG_D - PEG_D)/2))
    
    # Female Socket Cut at -Y
    sock_cut_B = Part.makeBox(INNER_W, PEG_L + 0.1, INNER_D, App.Vector(-INNER_W/2, -ARM_EXT - 0.1, z_B + (LEG_D - INNER_D)/2))
    
    # Center Hole for Pin (clearance fit)
    hole_radius = 8.0 * params.SCALE + params.GENERAL_CLEARANCE
    hole_B = Part.makeCylinder(hole_radius, HUB_H + 2.0, App.Vector(0,0,z_B - 1.0), App.Vector(0,0,1))
    
    # Stop Slot (sweep from 0 to -65)
    # At Z=0, cutting into the bottom face by 4.5mm to receive the 4.0mm peg from the bottom bracket
    slot_tool = Part.makeCylinder(4.2, 4.5, App.Vector(14.0 * params.SCALE, 0, z_B - 0.1), App.Vector(0,0,1))
    slot_B = slot_tool.copy()
    for angle in range(0, -66, -2):
        c = slot_tool.copy()
        c.Placement.Rotation = App.Rotation(App.Vector(0,0,1), angle)
        slot_B = slot_B.fuse(c)
    
    arm_b = hub_B.fuse(body_B).fuse(peg_B)
    arm_b = arm_b.cut(sock_cut_B).cut(hole_B).cut(slot_B)
    arm_b = arm_b.removeSplitter()
    
    # Note: Exported in default orientation (bottom face flat on build plate)
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    arm_b.exportStep(EXPORT_STEP)
    arm_b.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return arm_b

def main():
    doc = App.newDocument("XFrameHingeTop")
    shape = construct_hinge_top()
    feature = doc.addObject("Part::Feature", "HingeTop")
    feature.Shape = shape

if __name__ == "__main__":
    main()
