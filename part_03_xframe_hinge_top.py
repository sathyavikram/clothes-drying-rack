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
    PEG_L = params.PEG_LENGTH
    
    HUB_R = 20.0 * params.SCALE
    HUB_H = 25.0 * params.SCALE
    ARM_L = 100.0 * params.SCALE
    ARM_EXT = ARM_L / 2.0
    
    z_B = 0.0 # Printed flat on Z=0
    hub_B = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0,0,z_B), App.Vector(0,0,1))
    body_B = Part.makeBox(LEG_W, ARM_L, LEG_D, App.Vector(-LEG_W/2, -ARM_EXT, z_B))
    
    # ─── MALE THREAD (Top, Y = +ARM_EXT) ──────────────────────────────────────
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    p2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    tm_sweep = Part.Wire(tm_helix).makePipeShell([tm_wire], True, True)
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, 0))
    
    male_thread_base = Part.makeCompound([tm_core, tm_sweep])
    male_thread = male_thread_base.copy()
    male_thread.Placement = App.Placement(App.Vector(0, ARM_EXT, LEG_D/2), App.Rotation(App.Vector(1,0,0), -90))
    
    chamfer_m = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, ARM_EXT + t_length - t_pitch / 2 - 1, LEG_D/2),
        App.Vector(0,1,0)
    )
    end_cutter_m = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, ARM_EXT + t_length - 1, LEG_D/2),
        App.Vector(0,1,0)
    )
    
    male_peg = male_thread.cut(end_cutter_m.cut(chamfer_m))
    
    # ─── FEMALE THREAD (Bottom, Y = -ARM_EXT) ──────────────────────────────────
    tf_radius  = params.PEG_THREAD_RADIUS  # Nominal
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    
    tf_length_cut = t_length + 2.0
    tf_start_y = -ARM_EXT - t_pitch 
    tf_total_len = tf_length_cut + t_pitch*2
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    
    inner_X_f = tf_r_inner - 2.0 * params.SCALE
    f1 = App.Vector(inner_X_f,  0, -t_pitch * 0.35)
    f2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    f3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    f4 = App.Vector(inner_X_f,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([f1, f2, f3, f4, f1]))
    
    tf_sweep = Part.Wire(tf_helix).makePipeShell([tf_wire], True, True)
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len, App.Vector(0, 0, 0))
    sock_cutter_base = Part.makeCompound([tf_core, tf_sweep])
    
    sock_cutter = sock_cutter_base.copy()
    sock_cutter.Placement = App.Placement(App.Vector(0, tf_start_y, LEG_D/2), App.Rotation(App.Vector(1,0,0), -90))
    
    # Chamfer at female opening
    chamfer_f = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0,
        4.0,
        App.Vector(0, -ARM_EXT - 2.0, LEG_D/2),
        App.Vector(0,1,0)
    )

    body_base = hub_B.fuse(body_B)
    body_base = body_base.makeFillet(2.0 * params.SCALE, body_base.Edges)
    
    # Apply segment joints
    body_base = body_base.cut(sock_cutter).cut(chamfer_f)
    
    # Center Hole for Pin (clearance fit)
    hole_radius = 8.0 * params.SCALE + params.GENERAL_CLEARANCE
    hole_B = Part.makeCylinder(hole_radius, HUB_H + 2.0, App.Vector(0,0,z_B - 1.0), App.Vector(0,0,1))
    
    # Stop Slot (sweep from 0 to -65)
    slot_tool = Part.makeCylinder(4.2, 4.5, App.Vector(14.0 * params.SCALE, 0, z_B - 0.1), App.Vector(0,0,1))
    slot_B = slot_tool.copy()
    for angle in range(0, -66, -2):
        c = slot_tool.copy()
        c.Placement.Rotation = App.Rotation(App.Vector(0,0,1), angle)
        slot_B = slot_B.fuse(c)
    
    shape_cut = body_base.cut(hole_B).cut(slot_B)
    
    shape = Part.makeCompound([shape_cut, male_peg])
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return shape

def main():
    doc = App.newDocument("XFrameHingeTop")
    shape = construct_hinge_top()
    feature = doc.addObject("Part::Feature", "HingeTop")
    feature.Shape = shape

if __name__ == "__main__":
    main()
