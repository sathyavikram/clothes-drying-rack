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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_07_top_bracket_pin.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_07_top_bracket_pin.stl")

def construct_bracket_pin():
    t_pitch   = 4.0 * params.SCALE
    t_radius  = 8.0 * params.SCALE - params.THREAD_CLEARANCE
    t_r_inner = t_radius - (t_pitch * 0.45)
    
    t_length  = 19.0 * params.SCALE
    smooth_radius = 8.0 * params.SCALE - params.GENERAL_CLEARANCE
    smooth_len = 27.0 * params.SCALE
    head_radius = 16.0 * params.SCALE
    head_len = 5.0 * params.SCALE
    
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Solid(Part.Wire(t_helix).makePipeShell([t_wire], True, True))
    t_core  = Part.makeCylinder(t_r_inner, t_length, App.Vector(0, 0, 0))
    
    thread_base = t_core.fuse(t_sweep).removeSplitter()
    
    chamfer_cut = Part.makeCone(
        t_radius + 2.0, 0,
        t_radius + 2.0,
        App.Vector(0, 0, - (t_radius + 2.0) + 1.5)
    )
    
    z_smooth = t_length
    shaft = Part.makeCylinder(smooth_radius, smooth_len, App.Vector(0, 0, z_smooth))
    
    z_head = z_smooth + smooth_len
    head = Part.makeCylinder(head_radius, head_len, App.Vector(0, 0, z_head))
    
    slot_w = 4.0 * params.SCALE
    slot_d = 2.0 * params.SCALE
    slot_cut = Part.makeBox(head_radius * 2 + 2, slot_w, slot_d + 1, App.Vector(-head_radius - 1, -slot_w/2, z_head + head_len - slot_d))
    
    head = head.cut(slot_cut).removeSplitter()
    
    pin = thread_base.fuse(shaft).fuse(head).removeSplitter()
    pin = pin.cut(chamfer_cut).removeSplitter()
    
    rot_flat = App.Placement(App.Vector(0,0,head_radius), App.Rotation(App.Vector(1,0,0), 90))
    pin.Placement = rot_flat
    
    flat_cut = Part.makeBox(100, 100, 10, App.Vector(-50, -100, -10 + 1.0))
    pin = pin.cut(flat_cut).removeSplitter()
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    pin.exportStep(EXPORT_STEP)
    pin.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return pin

def main():
    doc = App.newDocument("TopBracketPin")
    shape = construct_bracket_pin()
    feature = doc.addObject("Part::Feature", "Pin")
    feature.Shape = shape

if __name__ == "__main__":
    main()
