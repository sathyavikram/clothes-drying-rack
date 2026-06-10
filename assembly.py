import FreeCAD as App
import Part
import Import
import os
import sys
import math

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")

def load_step(filename):
    path = os.path.join(EXPORT_BASE, filename)
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
    t_bracket_base = load_step("part_05_top_l_bracket.step")
    adapter_pin = load_step("part_07_threaded_adapter_pin.step")
    drying_rod = load_step("part_06_drying_rod.step")

    color_arm_a  = (0.3, 0.8, 0.3)
    color_arm_b  = (0.3, 0.6, 0.8)
    color_pin    = (0.8, 0.8, 0.2)
    color_leg_1  = (0.7, 0.7, 0.7)
    color_leg_2  = (0.5, 0.5, 0.5)

    base_leg = seg_shape.copy()
    base_leg.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), -90))
    leg_d_half = params.LEG_DEPTH / 2.0
    arm_b_z = 25.4
    rot_65 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 65))
    
    num_leg_segments = 1
    num_horizontal_rods = 1
    
    rod_length = 170.0 * params.SCALE
    arm_len_x = 45.0 * params.SCALE
    
    left_z = 0.0
    right_z = left_z + (num_horizontal_rods * rod_length) + (2 * arm_len_x)

    def place_t_bracket(doc_obj, prefix, name, P_local_leg_top, leg_angle_deg, trans_world, is_right_side):
        rad = math.radians(leg_angle_deg)
        mat = App.Matrix(
            0, -math.sin(rad), -math.cos(rad), 0,
            0,  math.cos(rad), -math.sin(rad), 0,
            1,  0,             0,              0,
            0,  0,             0,              1
        )
        rot_local = App.Rotation(mat)
        
        # If right side, rotate the bracket 180 around its vertical axis (local Y) to face inward
        if is_right_side:
            rot_local = rot_local.multiply(App.Rotation(App.Vector(0,1,0), 180))
            
        stem_len = 45.0 * params.SCALE
        hole_local_offset = rot_local.multVec(App.Vector(0, -stem_len, 0))
        O_local = P_local_leg_top.sub(hole_local_offset)
        
        bracket_local = App.Placement(O_local, rot_local)
        bracket_world = trans_world.multiply(bracket_local)
        
        t_bracket_p = t_bracket_base.copy()
        t_bracket_p.Placement = bracket_world
        add_part_to_doc(doc_obj, t_bracket_p, f"{prefix}_{name}", (0.3, 0.8, 0.3))
        return bracket_world

    def build_x_frame(z_offset, prefix, is_right_side):
        # We DO NOT rotate the right frame around Y, to keep leg_a aligned with leg_a and leg_b with leg_b
        trans_world = App.Placement(App.Vector(0,0,z_offset), App.Rotation(App.Vector(0,1,0), 0))
        
        arm_a_placed = arm_a.copy()
        arm_a_placed.Placement = trans_world
        add_part_to_doc(doc, arm_a_placed, f"{prefix}_Hinge_ArmA", color_arm_a)
        
        arm_b_placed = arm_b.copy()
        trans_z = App.Placement(App.Vector(0,0,arm_b_z), App.Rotation(App.Vector(0,1,0), 0))
        arm_b_placed.Placement = trans_world.multiply(trans_z.multiply(rot_65))
        add_part_to_doc(doc, arm_b_placed, f"{prefix}_Hinge_ArmB", color_arm_b)
        
        pin_placed = pin_shape.copy()
        unrot_flat = App.Placement(App.Vector(0, -16.0, 0), App.Rotation(App.Vector(1,0,0), -90))
        shift_z = App.Placement(App.Vector(0, 0, 4.4), App.Rotation(App.Vector(0,1,0), 0))
        pin_local = shift_z.multiply(unrot_flat.multiply(pin_shape.copy().Placement))
        pin_placed.Placement = trans_world.multiply(pin_local)
        add_part_to_doc(doc, pin_placed, f"{prefix}_Hinge_Pin", color_pin)
        
        P_local_A_top = None
        P_local_B_top = None
        
        for i in range(num_leg_segments):
            y_val = 125 + i * 170
            
            place_a_top = App.Placement(App.Vector(0, y_val, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
            leg_a_top = base_leg.copy()
            leg_a_top.Placement = trans_world.multiply(place_a_top.multiply(base_leg.Placement))
            add_part_to_doc(doc, leg_a_top, f"{prefix}_Leg_A_Top_{i}", color_leg_1)
            
            if i == num_leg_segments - 1:
                P_local_A_top = place_a_top.multVec(App.Vector(0, 0, 85.0))
                
            place_a_bot = App.Placement(App.Vector(0, -y_val, leg_d_half), App.Rotation(App.Vector(1,0,0), -90))
            leg_a_bot = base_leg.copy()
            leg_a_bot.Placement = trans_world.multiply(place_a_bot.multiply(base_leg.Placement))
            add_part_to_doc(doc, leg_a_bot, f"{prefix}_Leg_A_Bot_{i}", color_leg_2)
            
            place_b_top = App.Placement(App.Vector(0, y_val, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
            leg_b_top = base_leg.copy()
            leg_b_top.Placement = trans_world.multiply(rot_65.multiply(place_b_top.multiply(base_leg.Placement)))
            add_part_to_doc(doc, leg_b_top, f"{prefix}_Leg_B_Top_{i}", color_leg_1)
            
            if i == num_leg_segments - 1:
                P_local_B_top = rot_65.multiply(place_b_top).multVec(App.Vector(0, 0, 85.0))
                
            place_b_bot = App.Placement(App.Vector(0, -y_val, leg_d_half + arm_b_z), App.Rotation(App.Vector(1,0,0), -90))
            leg_b_bot = base_leg.copy()
            leg_b_bot.Placement = trans_world.multiply(rot_65.multiply(place_b_bot.multiply(base_leg.Placement)))
            add_part_to_doc(doc, leg_b_bot, f"{prefix}_Leg_B_Bot_{i}", color_leg_2)
            
        bracket_A = place_t_bracket(doc, prefix, "TBracket_A", P_local_A_top, 0, trans_world, is_right_side)
        bracket_B = place_t_bracket(doc, prefix, "TBracket_B", P_local_B_top, 65, trans_world, is_right_side)
        
        return bracket_A, bracket_B

    left_bracket_A, left_bracket_B = build_x_frame(left_z, "Left", False)
    right_bracket_A, right_bracket_B = build_x_frame(right_z, "Right", True)

    def build_horizontal_rods(start_bracket_world, prefix, add_adapter=True):
        if add_adapter:
            pin_side_local_pos = App.Vector(arm_len_x, 0, 0)
            pin_side_local_rot = App.Rotation(App.Vector(0,1,0), 90)
            pin_side_placement = App.Placement(pin_side_local_pos, pin_side_local_rot)
            
            pin_side_placed = adapter_pin.copy()
            pin_side_placed.Placement = start_bracket_world.multiply(pin_side_placement)
            add_part_to_doc(doc, pin_side_placed, f"{prefix}_Adapter_Pin_Side", (0.34, 0.74, 0.56))
            
            # Add adapter pin to the OTHER side too for symmetry in the assembly
            # Wait, the other side is the right bracket. The right bracket points inward now.
            # So its adapter pin would be placed by the right bracket. We don't need to do it here
            # because the horizontal rods connect them.
        
        for i in range(num_horizontal_rods):
            rod_local_pos = App.Vector(arm_len_x + 85.0 * params.SCALE + i * rod_length, 0, 0)
            rod_local_rot = App.Rotation(App.Vector(0,1,0), 90)
            rod_local_placement = App.Placement(rod_local_pos, rod_local_rot)
            
            rod_placed = drying_rod.copy()
            unrot_rod = App.Placement(App.Vector(), App.Rotation(App.Vector(1,0,0), -90))
            rod_placed.Placement = start_bracket_world.multiply(rod_local_placement).multiply(unrot_rod)
            add_part_to_doc(doc, rod_placed, f"{prefix}_Drying_Rod_{i}", (0.8, 0.5, 0.2))

    build_horizontal_rods(left_bracket_A, "Horiz_A")
    build_horizontal_rods(left_bracket_B, "Horiz_B")

    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
