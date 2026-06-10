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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_06_drying_rod.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_06_drying_rod.stl")

def make_square_wire(w, d, z, r=2.0 * params.SCALE):
    import math
    cx_tr = w/2 - r; cy_tr = d/2 - r
    cx_br = w/2 - r; cy_br = -d/2 + r
    cx_bl = -w/2 + r; cy_bl = -d/2 + r
    cx_tl = -w/2 + r; cy_tl = d/2 - r
    
    p1 = App.Vector(-w/2 + r, d/2, z)
    p2 = App.Vector(w/2 - r, d/2, z)
    mid_tr = App.Vector(cx_tr + r*math.cos(math.pi/4), cy_tr + r*math.sin(math.pi/4), z)
    p3 = App.Vector(w/2, d/2 - r, z)
    
    p4 = App.Vector(w/2, -d/2 + r, z)
    mid_br = App.Vector(cx_br + r*math.cos(-math.pi/4), cy_br + r*math.sin(-math.pi/4), z)
    p5 = App.Vector(w/2 - r, -d/2, z)
    
    p6 = App.Vector(-w/2 + r, -d/2, z)
    mid_bl = App.Vector(cx_bl + r*math.cos(-3*math.pi/4), cy_bl + r*math.sin(-3*math.pi/4), z)
    p7 = App.Vector(-w/2, -d/2 + r, z)
    
    p8 = App.Vector(-w/2, d/2 - r, z)
    mid_tl = App.Vector(cx_tl + r*math.cos(3*math.pi/4), cy_tl + r*math.sin(3*math.pi/4), z)
    
    e1 = Part.makeLine(p1, p2)
    e2 = Part.Edge(Part.Arc(p2, mid_tr, p3))
    e3 = Part.makeLine(p3, p4)
    e4 = Part.Edge(Part.Arc(p4, mid_br, p5))
    e5 = Part.makeLine(p5, p6)
    e6 = Part.Edge(Part.Arc(p6, mid_bl, p7))
    e7 = Part.makeLine(p7, p8)
    e8 = Part.Edge(Part.Arc(p8, mid_tl, p1))
    
    return Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])

def make_stadium_wire(w, h, z):
    import math
    r = h / 2.0
    s_len = w - h
    tiny = 0.002
    
    cx_r = s_len/2
    cx_l = -s_len/2
    
    p1 = App.Vector(-s_len/2, r, z)
    p2 = App.Vector(s_len/2, r, z)
    
    p3 = App.Vector(cx_r + r, tiny/2, z)
    p4 = App.Vector(cx_r + r, -tiny/2, z)
    
    p5 = App.Vector(s_len/2, -r, z)
    p6 = App.Vector(-s_len/2, -r, z)
    
    p7 = App.Vector(cx_l - r, -tiny/2, z)
    p8 = App.Vector(cx_l - r, tiny/2, z)
    
    e1 = Part.makeLine(p1, p2)
    e2 = Part.Edge(Part.Arc(p2, App.Vector(cx_r + r*math.cos(math.pi/4), r*math.sin(math.pi/4), z), p3))
    e3 = Part.makeLine(p3, p4)
    e4 = Part.Edge(Part.Arc(p4, App.Vector(cx_r + r*math.cos(-math.pi/4), r*math.sin(-math.pi/4), z), p5))
    e5 = Part.makeLine(p5, p6)
    e6 = Part.Edge(Part.Arc(p6, App.Vector(cx_l + r*math.cos(-3*math.pi/4), r*math.sin(-3*math.pi/4), z), p7))
    e7 = Part.makeLine(p7, p8)
    e8 = Part.Edge(Part.Arc(p8, App.Vector(cx_l + r*math.cos(3*math.pi/4), r*math.sin(3*math.pi/4), z), p1))
    
    return Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])

def construct_drying_rod():
    l = params.SEGMENT_BODY_LENGTH
    wall = params.LEG_WALL
    
    outer_radius = params.LEG_WIDTH / 2.0  # 12.5mm
    
    # Outer body (uniform cylindrical tube)
    body = Part.makeCylinder(outer_radius, l, App.Vector(0, 0, -l/2))
    
    # Hollow out the center. The solid sections at the ends (30mm) shouldn't be hollowed the same way.
    sq_len = 30.0 * params.SCALE
    hollow_start = -l/2 + sq_len
    hollow_len = l - 2 * sq_len
    
    inner_radius = outer_radius - wall  # 9.5mm
    
    inner_solid = Part.makeCylinder(inner_radius, hollow_len, App.Vector(0, 0, hollow_start))
    
    body = body.cut(inner_solid)
    
    # ─── THREADING (Copied from part_01_leg_segment.py) ──────────────────────
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
    
    male_peg = Part.makeCompound([tm_core, tm_sweep])
    
    # ─── FEMALE THREAD (Bottom, Z = -l/2) ────────────────────────────────────
    tf_radius  = params.PEG_THREAD_RADIUS
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
    
    body = body.cut(thread_cutter)
    
    chamfer_f = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0,
        4.0,
        App.Vector(0, 0, -l/2 - 2.0)
    )
    body = body.cut(chamfer_f)
    
    body.removeSplitter()
    
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
    doc = App.newDocument("DryingRod")
    shape = construct_drying_rod()
    feature = doc.addObject("Part::Feature", "DryingRod")
    feature.Shape = shape

if __name__ == "__main__":
    main()
