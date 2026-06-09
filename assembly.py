import FreeCAD as App
import Part
import Import
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

import part_01_leg_segment
import part_02_xframe_hinge_bottom
import part_03_xframe_hinge_top
import part_04_xframe_hinge_pin
import part_05_top_l_bracket

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")

def clear_exports():
    if os.path.exists(EXPORT_BASE):
        for f in os.listdir(EXPORT_BASE):
            try:
                os.remove(os.path.join(EXPORT_BASE, f))
            except Exception:
                pass

def load_step(filename):
    path = os.path.join(EXPORT_BASE, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path}")
    shape = Part.Shape()
    shape.read(path)
    return shape

def add_part_to_doc(doc, shape, name, color):
    feature = doc.addObject("Part::Feature", name)
    feature.Shape = shape
    if hasattr(feature, "ViewObject") and feature.ViewObject:
        feature.ViewObject.ShapeColor = color
    return feature

def build_assembly():
    
    doc = App.newDocument("Assembly")
    
    seg_shape = load_step("part_01_leg_segment.step")
    arm_a = load_step("part_02_xframe_hinge_bottom.step")
    arm_b = load_step("part_03_xframe_hinge_top.step")
    pin_shape = load_step("part_04_xframe_hinge_pin.step")
    
    color_arm_a  = (0.3, 0.8, 0.3)
    color_arm_b  = (0.3, 0.6, 0.8)
    color_pin    = (0.8, 0.8, 0.2)
    color_leg_1  = (0.7, 0.7, 0.7)
    color_leg_2  = (0.5, 0.5, 0.5)

    add_part_to_doc(doc, arm_a, "Hinge_ArmA_Bottom", color_arm_a)

    arm_b_z = 25.4
    rot_65 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 65))
    trans_z = App.Placement(App.Vector(0,0,arm_b_z), App.Rotation(0,0,0,1))
    
    arm_b_placed = arm_b.copy()
    arm_b_placed.Placement = trans_z.multiply(rot_65)
    add_part_to_doc(doc, arm_b_placed, "Hinge_ArmB_Top", color_arm_b)
    
    pin_placed = pin_shape.copy()
    unrot_flat = App.Placement(App.Vector(0, -16.0, 0), App.Rotation(App.Vector(1,0,0), -90))
    shift_z = App.Placement(App.Vector(0, 0, 4.4), App.Rotation(0,0,0,1))
    pin_placed.Placement = shift_z.multiply(unrot_flat.multiply(pin_placed.Placement))
    add_part_to_doc(doc, pin_placed, "Hinge_Pin", color_pin)
    
    base_leg = seg_shape.copy()
    base_leg.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), -90))
    
    leg_d_half = params.LEG_DEPTH / 2.0
    
    place_a_top = App.Placement(App.Vector(0, 125, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
    leg_a_top = base_leg.copy()
    leg_a_top.Placement = place_a_top.multiply(base_leg.Placement)
    add_part_to_doc(doc, leg_a_top, "Leg_A_Top", color_leg_1)

    place_a_bot = App.Placement(App.Vector(0, -125, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
    leg_a_bot = base_leg.copy()
    leg_a_bot.Placement = place_a_bot.multiply(base_leg.Placement)
    add_part_to_doc(doc, leg_a_bot, "Leg_A_Bottom", color_leg_2)

    place_b_top = App.Placement(App.Vector(0, 125, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
    leg_b_top = base_leg.copy()
    leg_b_top.Placement = rot_65.multiply(place_b_top.multiply(base_leg.Placement))
    add_part_to_doc(doc, leg_b_top, "Leg_B_Top", color_leg_1)

    place_b_bot = App.Placement(App.Vector(0, -125, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
    leg_b_bot = base_leg.copy()
    leg_b_bot.Placement = rot_65.multiply(place_b_bot.multiply(base_leg.Placement))
    add_part_to_doc(doc, leg_b_bot, "Leg_B_Bottom", color_leg_2)
    
    # ─── PHASE 4 Rigid T-Bracket at the top of Leg_B_Top ───
    shoulder_z = params.SEGMENT_BODY_LENGTH / 2.0  # 85.0
    
    t_bracket = load_step("part_05_top_l_bracket.step")
    t_bracket_base = t_bracket.copy()
    
    # ─── Exact Mathematical Placement ───
    # Local Bracket: Stem along -Y, Crossbar along +X.
    # World Target: Stem points down leg (sin 65, -cos 65, 0)
    # Crossbar points along world +Z (0, 0, 1)
    import math
    rad = math.radians(65)
    
    # Rotation Matrix columns: Local X -> World Z, Local Y -> -Stem_World, Local Z -> Cross
    mat = App.Matrix(
        0, -math.sin(rad), -math.cos(rad), 0,
        0,  math.cos(rad), -math.sin(rad), 0,
        1,  0,             0,              0,
        0,  0,             0,              1
    )
    rot_world = App.Rotation(mat)
    
    # Find P_world: The top of the leg peg
    leg_d_half = params.LEG_DEPTH / 2.0
    arm_b_z = 25.4
    Z_b = leg_d_half + arm_b_z
    P_local = App.Vector(0, 0, shoulder_z)
    P_world = rot_65.multiply(place_b_top).multVec(P_local)
    
    # Offset the bracket so the female thread (at Y = -stem_len) aligns with P_world
    stem_len = 45.0 * params.SCALE
    hole_world_offset = rot_world.multVec(App.Vector(0, -stem_len, 0))
    O_world = P_world.sub(hole_world_offset)
    
    bracket_world = App.Placement(O_world, rot_world)
    
    t_bracket_p = t_bracket_base.copy()
    t_bracket_p.Placement = bracket_world
    
    add_part_to_doc(doc, t_bracket_p, "Top_TBracket", (0.3, 0.8, 0.3))

    # Export Assembly
    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
