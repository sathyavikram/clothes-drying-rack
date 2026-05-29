import FreeCAD as App
import Part
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

CURRENT_DIR = os.getcwd()
EXPORT_BASE  = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_01_leg_tube.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_01_leg_tube.stl")

def make_male_thread(start_z):
    t_pitch   = params.THREAD_PITCH
    t_radius  = params.THREAD_NOM_RADIUS - params.THREAD_CLEARANCE
    t_r_inner = t_radius - (t_pitch * 0.45)
    t_length  = params.THREAD_LENGTH

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(0,0,0,1))
    
    t_core = Part.makeCylinder(t_r_inner, t_length, App.Vector(0, 0, start_z))
    
    # Thread tip chamfer (entry bevel) at the end of the thread
    # Assuming thread grows in +Z direction
    chamfer = Part.makeCone(
        t_radius + 2.0 * params.SCALE, t_r_inner,
        t_pitch / 2 + 1 * params.SCALE,
        App.Vector(0, 0, start_z + t_length - t_pitch / 2 - 1 * params.SCALE)
    )
    end_cutter = Part.makeCylinder(
        t_radius + 5.0 * params.SCALE, t_pitch + 2.0 * params.SCALE,
        App.Vector(0, 0, start_z + t_length - 1 * params.SCALE)
    )
    t_core = t_core.cut(end_cutter.cut(chamfer))
    t_sweep = t_sweep.cut(end_cutter.cut(chamfer))

    return t_core, t_sweep

def make_male_thread_inverted(start_z):
    # Builds the thread going in the -Z direction
    t_pitch   = params.THREAD_PITCH
    t_radius  = params.THREAD_NOM_RADIUS - params.THREAD_CLEARANCE
    t_r_inner = t_radius - (t_pitch * 0.45)
    t_length  = params.THREAD_LENGTH

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    # Rotate 180 around X to point it down
    t_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(1,0,0,0))
    
    t_core = Part.makeCylinder(t_r_inner, t_length, App.Vector(0, 0, start_z - t_length))
    
    chamfer = Part.makeCone(
        t_r_inner, t_radius + 2.0 * params.SCALE,
        t_pitch / 2 + 1 * params.SCALE,
        App.Vector(0, 0, start_z - t_length)
    )
    end_cutter = Part.makeCylinder(
        t_radius + 5.0 * params.SCALE, t_pitch + 2.0 * params.SCALE,
        App.Vector(0, 0, start_z - t_length - 1 * params.SCALE)
    )
    t_core = t_core.cut(end_cutter.cut(chamfer))
    t_sweep = t_sweep.cut(end_cutter.cut(chamfer))

    return t_core, t_sweep

def construct_leg_tube():
    # Build along Z-axis first for easier thread positioning
    body_len = params.SEGMENT_BODY_LENGTH
    
    outer_cyl = Part.makeCylinder(params.TUBE_OD / 2, body_len, App.Vector(0,0,0))
    inner_cyl = Part.makeCylinder(params.TUBE_ID / 2, body_len, App.Vector(0,0,0))
    tube_body = outer_cyl.cut(inner_cyl)
    
    sb_len = params.SPIGOT_LENGTH
    offset = sb_len - params.THREAD_LENGTH  # 5mm solid stub
    
    # Top spigot base
    stub_top = Part.makeCylinder(params.SPIGOT_OD / 2, offset, App.Vector(0,0,body_len))
    # Bottom spigot base
    stub_bot = Part.makeCylinder(params.SPIGOT_OD / 2, offset, App.Vector(0,0,-offset))
    
    tube_body = tube_body.fuse(stub_top).fuse(stub_bot).removeSplitter()
    
    tc_1, sw_1 = make_male_thread(body_len + offset)
    tc_2, sw_2 = make_male_thread_inverted(-offset)
    
    shape = Part.makeCompound([tube_body, tc_1, sw_1, tc_2, sw_2])
    
    # Print orientation: lying flat at 45° diagonal
    # Rotate around Y by 90 to lay flat, then around Z by 45 to fit diagonally
    shape.Placement = App.Placement(App.Vector(0,0,params.TUBE_OD/2), App.Rotation(App.Vector(0,1,0), 90)).multiply(shape.Placement)
    shape.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 45)).multiply(shape.Placement)

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    print(f"Volume: {tube_body.Volume}")
    return shape

def main():
    doc = App.newDocument("LegTube")
    shape = construct_leg_tube()
    feature = doc.addObject("Part::Feature", "LegTube")
    feature.Shape = shape

if __name__ == "__main__":
    main()
