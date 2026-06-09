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
    
    arm_len_x = 45.0 * params.SCALE
    arm_len_y = 60.0 * params.SCALE
    C = 4.0 * params.SCALE # Chamfer size for the inner corners
    
    # --- MAIN BODY 2D PROFILE ---
    p1 = App.Vector(-w/2, w/2, 0)
    p2 = App.Vector(arm_len_x, w/2, 0)
    p3 = App.Vector(arm_len_x, -w/2, 0)
    p4 = App.Vector(w/2 + C, -w/2, 0)
    p5 = App.Vector(w/2, -w/2 - C, 0)
    p6 = App.Vector(w/2, -arm_len_y, 0)
    p7 = App.Vector(-w/2, -arm_len_y, 0)

    # Note: Using Counter-Clockwise order here doesn't matter because we added
    # a check to flip the volume if it's negative later.
    wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p5, p6, p7, p1]))
    face = Part.Face(wire)
    body = face.extrude(App.Vector(0, 0, d))
    body.Placement.Base = App.Vector(0, 0, -d/2)
    
    if body.Volume < 0:
        body.reverse()
        
    try:
        body = body.makeFillet(2.0 * params.SCALE, body.Edges)
    except:
        print("Fillet failed, continuing without fillet.")

    # ------------------------------------------------------------------------
    # 3. Create female thread cutter for sockets
    # ------------------------------------------------------------------------
    t_pitch = params.PEG_THREAD_PITCH
    tf_radius = params.PEG_THREAD_RADIUS
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    tf_length_cut = params.PEG_LENGTH + 2.0 
    tf_total_len = tf_length_cut + 2.0
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    inner_X_f = tf_r_inner - 2.0 * params.SCALE
    pf1 = App.Vector(inner_X_f,  0, -t_pitch * 0.35)
    pf2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    pf3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    pf4 = App.Vector(inner_X_f,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([pf1, pf2, pf3, pf4, pf1]))
    
    tf_sweep = Part.Wire(tf_helix).makePipeShell([tf_wire], True, True)
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len + 2.0, App.Vector(0, 0, -1.0))
    
    chamfer_f_base = Part.makeCone(
        tf_radius + 2.0, tf_radius - 2.0, 4.0,
        App.Vector(0, 0, 0)
    )
    
    t_offset = t_pitch + 0.13

    # 1. Female at -Y (Bottom Arm, points +Y to cut inward)
    rot_neg_Y = App.Rotation(App.Vector(1,0,0), -90)
    base_neg_Y = App.Vector(0, -arm_len_y - t_offset, 0)
    
    sweep_neg_Y = tf_sweep.copy()
    sweep_neg_Y.Placement = App.Placement(base_neg_Y, rot_neg_Y)
    core_neg_Y = tf_core.copy()
    core_neg_Y.Placement = App.Placement(base_neg_Y, rot_neg_Y)
    cutter_neg_Y = Part.makeCompound([core_neg_Y, sweep_neg_Y])
    
    chamf_neg_Y = chamfer_f_base.copy()
    chamf_neg_Y.Placement = App.Placement(App.Vector(0, -arm_len_y - 2.0, 0), rot_neg_Y)

    # 2. Female at +X (Side Arm, points -X to cut inward)
    rot_pos_X = App.Rotation(App.Vector(0,1,0), -90)
    base_pos_X = App.Vector(arm_len_x + t_offset, 0, 0)
    
    sweep_pos_X = tf_sweep.copy()
    sweep_pos_X.Placement = App.Placement(base_pos_X, rot_pos_X)
    core_pos_X = tf_core.copy()
    core_pos_X.Placement = App.Placement(base_pos_X, rot_pos_X)
    cutter_pos_X = Part.makeCompound([core_pos_X, sweep_pos_X])
    
    chamf_pos_X = chamfer_f_base.copy()
    chamf_pos_X.Placement = App.Placement(App.Vector(arm_len_x + 2.0, 0, 0), rot_pos_X)

    # 3. Female at +Y (Top face, points -Y to cut inward)
    rot_pos_Y = App.Rotation(App.Vector(1,0,0), 90)
    base_pos_Y = App.Vector(0, w/2 + t_offset, 0)
    
    sweep_pos_Y = tf_sweep.copy()
    sweep_pos_Y.Placement = App.Placement(base_pos_Y, rot_pos_Y)
    core_pos_Y = tf_core.copy()
    core_pos_Y.Placement = App.Placement(base_pos_Y, rot_pos_Y)
    cutter_pos_Y = Part.makeCompound([core_pos_Y, sweep_pos_Y])
    
    chamf_pos_Y = chamfer_f_base.copy()
    chamf_pos_Y.Placement = App.Placement(App.Vector(0, w/2 + 2.0, 0), rot_pos_Y)

    # --- CUT ALL 3 SOCKETS (L-Bracket acting as T-Bracket) ---
    bracket_cut = body.cut(cutter_neg_Y)
    bracket_cut = bracket_cut.cut(chamf_neg_Y)
    bracket_cut = bracket_cut.cut(cutter_pos_X)
    bracket_cut = bracket_cut.cut(chamf_pos_X)
    bracket_cut = bracket_cut.cut(cutter_pos_Y)
    bracket_cut = bracket_cut.cut(chamf_pos_Y)
    # Removing removeSplitter entirely because it causes OCCError
    print(f"Shape valid: {bracket_cut.isValid()}, volume: {bracket_cut.Volume}")    
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
