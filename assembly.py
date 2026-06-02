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
    
    # 1. Regenerate parts guarantees correct shapes
    part_01_leg_segment.construct_leg_segment()
    part_02_xframe_hinge_bottom.construct_hinge_bottom()
    part_03_xframe_hinge_top.construct_hinge_top()
    part_04_xframe_hinge_pin.construct_hinge_pin()
    
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

    # Arm B is lifted by z_offset (25.4) and rotated around Z by 65 degrees
    arm_b_z = 25.4
    rot_65 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 65))
    trans_z = App.Placement(App.Vector(0,0,arm_b_z), App.Rotation(0,0,0,1))
    
    arm_b_placed = arm_b.copy()
    arm_b_placed.Placement = trans_z.multiply(rot_65)
    add_part_to_doc(doc, arm_b_placed, "Hinge_ArmB_Top", color_arm_b)
    
    # Place Pin. The pin is currently flat (rotated 90 X, +Z shifted up).
    # We want to unrotate it to bring it back to Z. And Z needs to be pointing downwards or upwards.
    # Actually, the pin was constructed with threads at Z=0..25 and head at Z=50..55.
    # In assembly, we want the head to sit on top of Arm B. Thus the head should be at Z = 50.8 + 5 = 55.4 (approx).
    # Thread starts at Z=0. We rotate it back -90 X, and move its origin to (0,0,0) so the threads sit in Arm A.
    pin_placed = pin_shape.copy()
    unrot_flat = App.Placement(App.Vector(0, -16.0, 0), App.Rotation(App.Vector(1,0,0), -90))
    shift_z = App.Placement(App.Vector(0, 0, 4.4), App.Rotation(0,0,0,1))
    pin_placed.Placement = shift_z.multiply(unrot_flat.multiply(pin_placed.Placement))
    add_part_to_doc(doc, pin_placed, "Hinge_Pin", color_pin)
    
    # Base leg segment has its axis along +Z, but due to export was rotated +90 around X.
    # Realigning with original design space:
    base_leg = seg_shape.copy()
    base_leg.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), -90))
    # In this Z-aligned space, the leg's peg is at +Z and socket at -Z.
    
    leg_d_half = params.LEG_DEPTH / 2.0
    arm_b_z = 25.4
    
    # Arm A goes along Y. Peg is at +Y. Socket is at -Y.
    # To mate with Peg at +Y: Leg needs its Socket (-Z) positioned over +Y. So +Z points +Y.
    place_a_top = App.Placement(App.Vector(0, 125, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
    leg_a_top = base_leg.copy()
    leg_a_top.Placement = place_a_top.multiply(base_leg.Placement)
    add_part_to_doc(doc, leg_a_top, "Leg_A_Top", color_leg_1)

    # To mate with Socket at -Y: Leg needs its Peg (+Z) pushed into -Y. So +Z points -Y.
    # Rot_X(-90): +Z -> +Y.
    place_a_bot = App.Placement(App.Vector(0, -125, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
    leg_a_bot = base_leg.copy()
    leg_a_bot.Placement = place_a_bot.multiply(base_leg.Placement)
    add_part_to_doc(doc, leg_a_bot, "Leg_A_Bottom", color_leg_2)

    # Arm B is lifted by z_offset (25.4) and rotated around Z by 65 degrees
    rot_65 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 65))
    
    place_b_top = App.Placement(App.Vector(0, 125, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
    leg_b_top = base_leg.copy()
    leg_b_top.Placement = rot_65.multiply(place_b_top.multiply(base_leg.Placement))
    add_part_to_doc(doc, leg_b_top, "Leg_B_Top", color_leg_1)

    place_b_bot = App.Placement(App.Vector(0, -125, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
    leg_b_bot = base_leg.copy()
    leg_b_bot.Placement = rot_65.multiply(place_b_bot.multiply(base_leg.Placement))
    add_part_to_doc(doc, leg_b_bot, "Leg_B_Bottom", color_leg_2)

    # Export Assembly
    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
