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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_06_top_bracket_leg_mount.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_06_top_bracket_leg_mount.stl")

def construct_leg_mount():
    LEG_W = params.LEG_WIDTH
    LEG_D = params.LEG_DEPTH
    
    HUB_R = 20.0 * params.SCALE
    HUB_H = 25.0 * params.SCALE
    ARM_EXT = 40.0 * params.SCALE
    
    z_B = 0.0 # Printed flat on Z=0
    hub_B = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0,0,z_B), App.Vector(0,0,1))
    body_B = Part.makeBox(LEG_W, ARM_EXT, LEG_D, App.Vector(-LEG_W/2, 0, z_B))
    body_base = hub_B.fuse(body_B).removeSplitter()
    
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    # ─── FEMALE THREAD (Y = +ARM_EXT, pointing inward to -Y) ──────────────────
    tf_radius  = params.PEG_THREAD_RADIUS  # Nominal
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    
    tf_length_cut = t_length + 2.0
    tf_total_len = tf_length_cut + t_pitch*2
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    
    inner_X_m = tf_r_inner - 2.0 * params.SCALE
    f1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    f2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    f3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    f4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([f1, f2, f3, f4, f1]))
    
    tf_sweep = Part.Solid(Part.Wire(tf_helix).makePipeShell([tf_wire], True, True))
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len, App.Vector(0, 0, 0))
    sock_cutter_base = tf_core.fuse(tf_sweep).removeSplitter()
    
    sock_cutter = sock_cutter_base.copy()
    tf_start_y = ARM_EXT + t_pitch
    # +90 around X makes local +Z point to global -Y
    sock_cutter.Placement = App.Placement(App.Vector(0, tf_start_y, LEG_D/2), App.Rotation(App.Vector(1,0,0), 90))
    
    # Chamfer at female opening
    chamfer_f = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0,
        4.0,
        App.Vector(0, ARM_EXT + 2.0, LEG_D/2),
        App.Vector(0,-1,0)
    )

    body_base = body_base.cut(sock_cutter).cut(chamfer_f).removeSplitter()
    
    # Center Hole for Pin (clearance fit)
    hole_radius = 8.0 * params.SCALE + params.GENERAL_CLEARANCE
    hole_B = Part.makeCylinder(hole_radius, HUB_H + 2.0, App.Vector(0,0,z_B - 1.0), App.Vector(0,0,1))
    
    shape = body_base.cut(hole_B).removeSplitter()
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return shape

def main():
    doc = App.newDocument("TopBracketLegMount")
    shape = construct_leg_mount()
    feature = doc.addObject("Part::Feature", "LegMount")
    feature.Shape = shape

if __name__ == "__main__":
    main()
