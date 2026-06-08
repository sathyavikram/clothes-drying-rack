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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_04_xframe_hinge_pin.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_04_xframe_hinge_pin.stl")

def construct_hinge_pin():
    # Pin parameters
    t_pitch   = 4.0 * params.SCALE
    t_radius  = 8.0 * params.SCALE - params.THREAD_CLEARANCE
    t_r_inner = t_radius - (t_pitch * 0.55)
    
    # 25.0 Hub height. Make thread 19mm long so it has clearance from the 3mm floor.
    t_length  = 19.0 * params.SCALE
    
    smooth_radius = 8.0 * params.SCALE - params.GENERAL_CLEARANCE
    # 25.0 Hub height + 2.0mm clearance
    smooth_len = 27.0 * params.SCALE
    
    head_radius = 16.0 * params.SCALE
    head_len = 5.0 * params.SCALE
    
    # ─── Threaded shaft ──────────────────────────────────────
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 0.5 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.45)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.15)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.15)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.45)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Solid(Part.Wire(t_helix).makePipeShell([t_wire], True, True))
    t_core  = Part.makeCylinder(t_r_inner, t_length, App.Vector(0, 0, 0))
    
    thread_base = t_core.fuse(t_sweep)
    chamfer = Part.makeCone(
        t_radius + 2.0, t_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, -1)
    )
    # the thread starts at z=0 and goes to z=t_length.
    # tip is at z=0. The chamfer should cut the bottom.
    # Wait, the chamfer in the skill is at the tip. 
    # Let's orient the pin so the tip is at z=0, and head is at positive z.
    # Our helix starts at z=0 and goes up +25.
    
    # Let's put tip chamfer at Z=0
    chamfer_cut = Part.makeCone(
        t_radius + 2.0, 0,
        t_radius + 2.0,
        App.Vector(0, 0, - (t_radius + 2.0) + 1.5)
    )
    # So Z=0 is chopped off.
    
    # ─── Smooth Shaft ────────────────────────────────────────
    z_smooth = t_length
    shaft = Part.makeCylinder(smooth_radius, smooth_len, App.Vector(0, 0, z_smooth))
    
    # ─── Head ────────────────────────────────────────────────
    z_head = z_smooth + smooth_len
    head = Part.makeCylinder(head_radius, head_len, App.Vector(0, 0, z_head))
    head = head.makeFillet(1.5 * params.SCALE, head.Edges)
    # Add a flat head slot so a screwdriver or coin can turn it
    slot_w = 4.0 * params.SCALE
    slot_d = 2.0 * params.SCALE
    slot_cut = Part.makeBox(head_radius * 2 + 2, slot_w, slot_d + 1, App.Vector(-head_radius - 1, -slot_w/2, z_head + head_len - slot_d))
    
    head = head.cut(slot_cut)
    
    pin = thread_base.fuse(shaft).fuse(head)
    
    # Cut chamfer at the tip
    pin = pin.cut(chamfer_cut)
    
    # Print orientation: rotation is critical. We must rotate it 90 degrees around X
    # so the long axis is flat on the build plate (Z=0)
    # The pin is currently along the Z axis from 0 to ~55.
    # Rotating 90 around X will put it along the -Y axis.
    rot_flat = App.Placement(App.Vector(0,0,head_radius), App.Rotation(App.Vector(1,0,0), 90))
    pin.Placement = rot_flat
    
    # Slice a tiny flat bottom so it prints without supports and adheres well.
    # The pin center is now at Z=head_radius. The bottom is at Z=0.
    # Let's cut from Z=-10 to Z=1.0 to give it a 1mm flat.
    flat_cut = Part.makeBox(100, 100, 10, App.Vector(-50, -100, -10 + 1.0))
    pin = pin.cut(flat_cut)
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    pin.exportStep(EXPORT_STEP)
    pin.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return pin

def main():
    doc = App.newDocument("XFrameHingePin")
    shape = construct_hinge_pin()
    feature = doc.addObject("Part::Feature", "HingePin")
    feature.Shape = shape

if __name__ == "__main__":
    main()
