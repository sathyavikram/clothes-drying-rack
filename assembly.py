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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")

def clear_exports():
    if os.path.exists(EXPORT_BASE):
        for f in os.listdir(EXPORT_BASE):
            try:
                os.remove(os.path.join(EXPORT_BASE, f))
            except Exception as e:
                print(f"Warning: could not remove {f}: {e}")

def load_step(filename):
    path = os.path.join(EXPORT_BASE, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path}")
    shape = Part.Shape()
    shape.read(path)
    return shape

def add_part_to_doc(doc, shape, name, pos, rot_axis, rot_angle, color):
    feature = doc.addObject("Part::Feature", name)
    feature.Shape = shape
    feature.Placement = App.Placement(pos, App.Rotation(rot_axis, rot_angle))
    if hasattr(feature, "ViewObject") and feature.ViewObject:
        feature.ViewObject.ShapeColor = color
    return feature

def build_assembly():
    clear_exports()
    
    # 1. Regenerate parts
    part_01_leg_segment.construct_leg_segment()
    
    # 2. Setup doc
    doc = App.newDocument("Assembly")
    
    # 3. Load generated geometry
    seg_shape  = load_step("part_01_leg_segment.step")
    
    # Due to print orientation, segment is rotated.
    # We rotate it back for vertical assembly visualization.
    seg_rot_axis = App.Vector(1, 0, 0)
    seg_rot_angle = -90
    
    color_seg_bottom  = (0.7, 0.7, 0.7)
    color_seg_top     = (0.5, 0.5, 0.5)
    
    # The origin of the base shape is precisely at the center of the segment body.
    # The female end (open) is at -L/2 from the center.
    # The male end (peg) starts exactly at +L/2 and extends to L/2 + peg_length.
    # When standing upright, the peg is at the top.
    
    # Segment 1 (bottom)
    add_part_to_doc(doc, seg_shape, "LegSegment_Bottom", App.Vector(0, 0, 0), seg_rot_axis, seg_rot_angle, color_seg_bottom)
    
    # Segment 2 (top)
    # Stacking it exactly on top of Segment 1. Segment 2's base/female end rests on Segment 1's shoulders.
    # So we shift it up exactly by the body length.
    z_cursor = params.SEGMENT_BODY_LENGTH
    
    add_part_to_doc(doc, seg_shape, "LegSegment_Top", App.Vector(0, 0, z_cursor), seg_rot_axis, seg_rot_angle, color_seg_top)
    
    # 4. Export Assembly
    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
