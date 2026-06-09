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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_01_leg_segment.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_01_leg_segment.stl")


def construct_leg_segment():
    w = params.LEG_WIDTH
    d = params.LEG_DEPTH
    l = params.SEGMENT_BODY_LENGTH
    wall = params.LEG_WALL
    
    # Body (Solid Rectangular initially)
    body = Part.makeBox(w, d, l)
    body.Placement.Base = App.Vector(-w/2, -d/2, -l/2)
    body = body.makeFillet(2.0 * params.SCALE, body.Edges)
    
    # Hollow out the center, leaving 30mm solid at each end for joinery
    inner_w = w - 2*wall
    inner_d = d - 2*wall
    inner_l = l - 60.0 * params.SCALE
    if inner_l > 0:
        inner_box = Part.makeBox(inner_w, inner_d, inner_l)
        inner_box.Placement.Base = App.Vector(-inner_w/2, -inner_d/2, -inner_l/2)
        inner_box = inner_box.makeFillet(2.0 * params.SCALE, inner_box.Edges)
        body = body.cut(inner_box)
    
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    # ─── MALE THREAD (Top, Z = +l/2) ──────────────────────────────────────────
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
    tm_sweep.Placement = App.Placement(App.Vector(0, 0, l/2), App.Rotation(0,0,0,1))
    
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, l/2))
    
    chamfer_m = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, l/2 + t_length - t_pitch / 2 - 1)
    )
    end_cutter_m = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, l/2 + t_length - 1)
    )
    
    tm_sweep = tm_sweep.cut(end_cutter_m.cut(chamfer_m))
    tm_core = tm_core.cut(end_cutter_m.cut(chamfer_m))
    
    # IMPORTANT: use makeCompound, NOT fuse()
    male_peg = Part.makeCompound([tm_core, tm_sweep])
    
    # We need to cut the female socket first.
    
    # ─── FEMALE THREAD (Bottom, Z = -l/2) ────────────────────────────────────
    tf_radius  = params.PEG_THREAD_RADIUS  # Nominal
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    
    tf_length_cut = t_length + 2.0
    tf_start_z = -l/2 - t_pitch
    tf_total_len = tf_length_cut + t_pitch*2
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    
    inner_X_f = tf_r_inner - 2.0 * params.SCALE
    pf1 = App.Vector(inner_X_f,  0, -t_pitch * 0.35)
    pf2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    pf3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    pf4 = App.Vector(inner_X_f,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([pf1, pf2, pf3, pf4, pf1]))
    
    tf_sweep = Part.Wire(tf_helix).makePipeShell([tf_wire], True, True)
    tf_sweep.Placement = App.Placement(App.Vector(0, 0, tf_start_z), App.Rotation(0,0,0,1))
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len + 2.0, App.Vector(0, 0, tf_start_z - 1.0))
    
    thread_cutter = Part.makeCompound([tf_core, tf_sweep])
    
    # Cut female socket into main body
    body = body.cut(thread_cutter)
    
    
    # Add a chamfer to female opening
    chamfer_f = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0,
        4.0,
        App.Vector(0, 0, -l/2 - 2.0)
    )
    body = body.cut(chamfer_f)
    
    # Now combine the male peg
    shape = Part.makeCompound([body, male_peg])
    
    # Print orientation: lying flat on the long face (horizontal).
    shape.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90)

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape


def main():
    doc = App.newDocument("LegSegment")
    shape = construct_leg_segment()
    feature = doc.addObject("Part::Feature", "LegSegment")
    feature.Shape = shape


if __name__ == "__main__":
    main()
