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
import part_05_top_bracket_rod_mount
import part_06_top_bracket_leg_mount
import part_07_top_bracket_pin

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
    clear_exports()
    
    part_01_leg_segment.construct_leg_segment()
    part_02_xframe_hinge_bottom.construct_hinge_bottom()
    part_03_xframe_hinge_top.construct_hinge_top()
    part_04_xframe_hinge_pin.construct_hinge_pin()
    part_05_top_bracket_rod_mount.construct_rod_mount()
    part_06_top_bracket_leg_mount.construct_leg_mount()
    part_07_top_bracket_pin.construct_bracket_pin()
    
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
    
    # ─── PHASE 4 T-Bracket at the top of Leg_B_Top ───
    shoulder_z = params.SEGMENT_BODY_LENGTH / 2.0  # 85.0
    arm_b_z = 25.4
    unrot = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), -90))
    
    leg_mount = load_step("part_06_top_bracket_leg_mount.step")
    leg_mount_base = leg_mount.copy()
    leg_mount_base.Placement = unrot.multiply(leg_mount.Placement)
    offset_p6 = App.Placement(App.Vector(0, 0, shoulder_z), App.Rotation(0,0,0,1))
    p6_world = rot_65.multiply(place_b_top.multiply(offset_p6.multiply(leg_mount_base.Placement)))
    
    leg_mount_p = leg_mount_base.copy()
    leg_mount_p.Placement = p6_world
    add_part_to_doc(doc, leg_mount_p, "TBracket_LegMount", (0.3, 0.6, 0.8))
    
    rod_mount = load_step("part_05_top_bracket_rod_mount.step")
    rod_mount_base = rod_mount.copy()
    rod_mount_base.Placement = unrot.multiply(rod_mount.Placement)
    offset_p5 = App.Placement(App.Vector(0, -arm_b_z, shoulder_z + 40.0), App.Rotation(0,0,0,1))
    rot_p5_deploy = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,1,0), -45))
    p5_world = rot_65.multiply(place_b_top.multiply(offset_p5.multiply(rot_p5_deploy.multiply(rod_mount_base.Placement))))
    
    rod_mount_p = rod_mount_base.copy()
    rod_mount_p.Placement = p5_world
    add_part_to_doc(doc, rod_mount_p, "TBracket_RodMount", (0.3, 0.8, 0.3))
    
    # Position of part 07 (Pin)
    t_pin = load_step("part_07_top_bracket_pin.step")
    t_pin_base = t_pin.copy()
    
    # Let's completely override the placement. The shape points +Z originally.
    # The pin native export lies flat via rotation:
    # rot_flat = App.Placement(App.Vector(0,0,head_radius), App.Rotation(App.Vector(1,0,0), 90))
    # We unrotate it with unrot (App.Rotation((1,0,0), -90)). Just shifting it to origin.
    shift_z = App.Placement(App.Vector(0, 0, -16.0), App.Rotation(0,0,0,1))
    t_pin_base.Placement = shift_z.multiply(unrot.multiply(t_pin.Placement))
    
    # Pin axis is +Z. We want it pointing -Y relative to the leg frame.
    offset_pin = App.Placement(App.Vector(0, 15.0, shoulder_z + 40.0), App.Rotation(App.Vector(1,0,0), 90))
    pin_world = rot_65.multiply(place_b_top.multiply(offset_pin.multiply(t_pin_base.Placement)))
    
    t_pin_p = t_pin_base.copy()
    t_pin_p.Placement = pin_world
    add_part_to_doc(doc, t_pin_p, "TBracket_Pin", color_pin)

    # Export Assembly
    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
