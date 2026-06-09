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
    PEG_L = params.PEG_LENGTH
    
    HUB_R = 20.0 * params.SCALE
    HUB_H = 25.0 * params.SCALE
    ARM_L = 100.0 * params.SCALE
    ARM_EXT = ARM_L / 2.0
    
    z_A = 0.0
    hub_A = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0,0,z_A), App.Vector(0,0,1))
    body_A = Part.makeBox(LEG_W, ARM_L, LEG_D, App.Vector(-LEG_W/2, -ARM_EXT, z_A))
    
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
    rot_m = App.Rotation(App.Vector(1,0,0), -90)
    base_m = App.Vector(0, ARM_EXT, LEG_D/2)
    tm_sweep.Placement = App.Placement(base_m, rot_m)
    
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, 0))
    tm_core.Placement = App.Placement(base_m, rot_m)
    
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
    
    tm_sweep = tm_sweep.cut(end_cutter_m.cut(chamfer_m))
    tm_core = tm_core.cut(end_cutter_m.cut(chamfer_m))
    male_peg = Part.makeCompound([tm_core, tm_sweep])
    
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
    rot_f = App.Rotation(App.Vector(1,0,0), -90)
    base_f = App.Vector(0, tf_start_y, LEG_D/2)
    tf_sweep.Placement = App.Placement(base_f, rot_f)
    
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len + 2.0, App.Vector(0, 0, -1.0))
    tf_core.Placement = App.Placement(base_f, rot_f)
    
    sock_cutter = Part.makeCompound([tf_core, tf_sweep])
    
    # Chamfer at female opening
    chamfer_f = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0,
        4.0,
        App.Vector(0, -ARM_EXT - 2.0, LEG_D/2),
        App.Vector(0,1,0)
    )

    # Stop Peg for the hinge mechanism itself
    stop_peg_A = Part.makeCylinder(3.6, 4.0, App.Vector(14.0 * params.SCALE, 0, HUB_H), App.Vector(0,0,1))
    
    body_base = hub_A.fuse(body_A)
    body_base = body_base.makeFillet(2.0 * params.SCALE, body_base.Edges)
    body_base = body_base.fuse(stop_peg_A)
    
    # Apply segment joints
    body_base = body_base.cut(sock_cutter).cut(chamfer_f)
    
    # ─── Pivot Thread Cutter (Female inside the hub) ──────────────────────────────
    p_pitch   = 4.0 * params.SCALE
    p_radius  = 8.0 * params.SCALE          # nominal — NO clearance reduction
    p_r_inner = p_radius - (p_pitch * 0.45)
    
    start_z = 3.0 * params.SCALE
    p_length  = HUB_H - start_z + 1.0 
    
    p_helix = Part.makeHelix(p_pitch, p_length, p_r_inner, 0)
    
    inner_X_p = p_r_inner - 2.0 * params.SCALE
    p_1 = App.Vector(inner_X_p,  0, -p_pitch * 0.35)
    p_2 = App.Vector(p_radius, 0, -p_pitch * 0.10)
    p_3 = App.Vector(p_radius, 0,  p_pitch * 0.10)
    p_4 = App.Vector(inner_X_p,  0,  p_pitch * 0.35)
    p_wire = Part.Wire(Part.makePolygon([p_1, p_2, p_3, p_4, p_1]))

    p_sweep = Part.Wire(p_helix).makePipeShell([p_wire], True, True)
    p_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(0,0,0,1))
    
    p_core  = Part.makeCylinder(p_r_inner, p_length + 2.0, App.Vector(0, 0, start_z - 1.0))
    
    pivot_cutter = Part.makeCompound([p_core, p_sweep])

    bottom_trimmer = Part.makeBox(100.0, 100.0, 100.0, App.Vector(-50.0, -50.0, -100.0 + start_z))
    pivot_chamfer = Part.makeCone(p_radius+1.0, p_radius-1.0, 2.0, App.Vector(0,0,HUB_H-2.0))

    # Cut pivot thread into arm (sequentially to avoid OpenCASCADE procedural shape corruption)
    # The bottom trimmer removes the extra thread geometry from the hub bottom
    shape_cut = body_base.cut(pivot_cutter).cut(pivot_chamfer)
    
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
    doc = App.newDocument("XFrameHingeBottom")
    shape = construct_hinge_bottom()
    feature = doc.addObject("Part::Feature", "HingeBottom")
    feature.Shape = shape

if __name__ == "__main__":
    main()
