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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_05_top_t_bracket.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_05_top_t_bracket.stl")

def construct_t_bracket():
    w = params.LEG_WIDTH
    d = params.LEG_DEPTH
    
    arm_len = 45.0 * params.SCALE
    C = 4.0 * params.SCALE # Chamfer size for the inner corners
    
    # --- MAIN BODY 2D PROFILE ---
    p1 = App.Vector(-w/2, w/2, 0)
    p2 = App.Vector(arm_len, w/2, 0)
    p3 = App.Vector(arm_len, -w/2, 0)
    p4 = App.Vector(w/2 + C, -w/2, 0)
    p5 = App.Vector(w/2, -w/2 - C, 0)
    p6 = App.Vector(w/2, -arm_len, 0)
    p7 = App.Vector(-w/2, -arm_len, 0)
    
    wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p5, p6, p7, p1]))
    face = Part.Face(wire)
    body = face.extrude(App.Vector(0, 0, d))
    body.Placement.Base = App.Vector(0, 0, -d/2)
    body = body.makeFillet(2.0 * params.SCALE, body.Edges)
    
    # --- THREAD PARAMETERS ---
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    # --- MALE THREAD (Crossbar, pointing +X) ---
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    pm1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    pm2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    pm3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    pm4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([pm1, pm2, pm3, pm4, pm1]))
    
    tm_sweep = Part.Solid(Part.Wire(tm_helix).makePipeShell([tm_wire], True, True))
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, 0))
    male_thread_base = tm_core.fuse(tm_sweep).removeSplitter()
    
    # Chamfer and clean
    chamfer_m = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, t_length - t_pitch / 2 - 1)
    )
    end_cutter_m = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, t_length - 1)
    )
    male_peg_clean = male_thread_base.cut(end_cutter_m.cut(chamfer_m)).removeSplitter()
    
    # Rotate to point +X
    rot_to_X = App.Rotation(App.Vector(0,1,0), 90)
    male_peg_X = male_peg_clean.copy()
    male_peg_X.Placement = App.Placement(App.Vector(arm_len - 1.0, 0, 0), rot_to_X)
    
    # --- FEMALE THREAD CUTTER ---
    tf_radius  = params.PEG_THREAD_RADIUS
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    tf_length_cut = t_length + 2.0
    tf_total_len = tf_length_cut + t_pitch*2
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    inner_X_f = tf_r_inner - 2.0 * params.SCALE
    pf1 = App.Vector(inner_X_f,  0, -t_pitch * 0.35)
    pf2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    pf3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    pf4 = App.Vector(inner_X_f,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([pf1, pf2, pf3, pf4, pf1]))
    
    tf_sweep = Part.Solid(Part.Wire(tf_helix).makePipeShell([tf_wire], True, True))
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len, App.Vector(0, 0, 0))
    thread_cutter_base = tf_core.fuse(tf_sweep).removeSplitter()
    
    chamfer_f_base = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0, 4.0,
        App.Vector(0, 0, 0)
    )
    
    # Female at -Y (points +Y, placed at bottom)
    rot_to_Y = App.Rotation(App.Vector(1,0,0), -90)
    thread_cutter_neg_Y = thread_cutter_base.copy()
    thread_cutter_neg_Y.Placement = App.Placement(App.Vector(0, -arm_len - t_pitch, 0), rot_to_Y)
    chamfer_f_neg_Y = chamfer_f_base.copy()
    chamfer_f_neg_Y.Placement = App.Placement(App.Vector(0, -arm_len - 2.0, 0), rot_to_Y)

    # --- FUSE AND CUT ---
    # Combine body with male peg
    bracket_fused = body.fuse(male_peg_X).removeSplitter()
    
    # Cut female socket
    bracket_cut = bracket_fused.cut(thread_cutter_neg_Y).cut(chamfer_f_neg_Y).removeSplitter()
    
    # Add a nice chamfer to the outer corners for visual appeal
    # Not using Part.makeChamfer on edges to avoid index fragility.
    # Instead, we just keep the flat T-shape. The inner fillet is already built into the 2D profile!
    
    # Print orientation: The part is completely flat in the XY plane.
    # We can just leave it exactly as is!
    # XY plane is the build plate. The Z thickness is 20mm.
    # The female thread points along Y (horizontal).
    # Wait! If the female thread points along Y, it is printed horizontally!
    # And the male thread points along X, which is also printed horizontally!
    # If the user is okay with printing horizontal threads (as done in part_01), this is perfectly printable!
    shape = bracket_cut.copy()
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape

def main():
    doc = App.newDocument("TopTBracket")
    shape = construct_t_bracket()
    feature = doc.addObject("Part::Feature", "TBracket")
    feature.Shape = shape

if __name__ == "__main__":
    main()
