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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_02_xframe_hinge_bottom.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_02_xframe_hinge_bottom.stl")

def construct_hinge_bottom():
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
    
    z_A = 0.0
    hub_A = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0,0,z_A), App.Vector(0,0,1))
    body_A = Part.makeBox(LEG_W, ARM_L, LEG_D, App.Vector(-LEG_W/2, -ARM_EXT, z_A))
    
    # Male Peg at +Y
    peg_A = Part.makeBox(PEG_W, PEG_L, PEG_D, App.Vector(-PEG_W/2, ARM_EXT, z_A + (LEG_D - PEG_D)/2))
    
    # Female Socket Cut at -Y
    sock_cut_A = Part.makeBox(INNER_W, PEG_L + 0.1, INNER_D, App.Vector(-INNER_W/2, -ARM_EXT - 0.1, z_A + (LEG_D - INNER_D)/2))
    
    # Stop Peg
    stop_peg_A = Part.makeCylinder(3.6, 4.0, App.Vector(14.0 * params.SCALE, 0, HUB_H), App.Vector(0,0,1))
    
    arm_a = hub_A.fuse(body_A).fuse(peg_A).fuse(stop_peg_A)
    arm_a = arm_a.cut(sock_cut_A)
    arm_a = arm_a.removeSplitter()
    
    # ─── Thread Cutter (Female) ──────────────────────────────
    t_pitch   = 4.0 * params.SCALE
    t_radius  = 8.0 * params.SCALE          # nominal — NO clearance reduction
    t_r_inner = t_radius - (t_pitch * 0.45)
    
    # Do not cut all the way through Z=0. Leave 3mm of solid bed adhesion material at the bottom.
    start_z = 3.0 * params.SCALE
    t_length  = HUB_H - start_z + 1.0 # Exceed top slightly

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(0,0,0,1))
    t_core  = Part.makeCylinder(t_r_inner, t_length + 2.0, App.Vector(0, 0, start_z - 1.0))

    thread_cutter = t_core.fuse(t_sweep).removeSplitter()
    
    # ─── FIX: Trim the bottom of the cutter so it's perfectly flat at Z = start_z ───
    # The sweep profile extends downwards by t_pitch * 0.35 from its origin trajectory.
    # Because t_core only goes down to start_z - 1.0, and the sweep reaches below that,
    # it leaves floating unconnected artifacts when making a blind hole cutter.
    # Chopping EVERYTHING below start_z from the cutter tool ensures a perfectly flat floor inside the hole.
    bottom_trimmer = Part.makeBox(100.0, 100.0, 100.0, App.Vector(-50.0, -50.0, -100.0 + start_z))
    thread_cutter_trimmed = thread_cutter.cut(bottom_trimmer).removeSplitter()
    
    # Additional clearance at the top to avoid pinching
    thread_chamfer = Part.makeCone(t_radius+1.0, t_radius-1.0, 2.0, App.Vector(0,0,HUB_H-2.0))
    thread_cutter_final = thread_cutter_trimmed.fuse(thread_chamfer).removeSplitter()

    # Cut thread into arm
    shape = arm_a.cut(thread_cutter_final)
    shape = shape.removeSplitter()

    # Print orientation: Largest flat face is on the build plate (Z=0)
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape

def main():
    doc = App.newDocument("XFrameHingeBottom")
    shape = construct_hinge_bottom()
    feature = doc.addObject("Part::Feature", "HingeBottom")
    feature.Shape = shape

if __name__ == "__main__":
    main()
