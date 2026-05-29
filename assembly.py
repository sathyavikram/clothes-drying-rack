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
import part_01b_leg_connector

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
    part_01b_leg_connector.construct_leg_connector()
    
    # 2. Setup doc
    doc = App.newDocument("Assembly")
    
    # 3. Load generated geometry
    seg_shape  = load_step("part_01_leg_segment.step")
    conn_shape = load_step("part_01b_leg_connector.step")
    
    # Due to print orientation, segment is rotated.
    # We rotate it back for vertical assembly visualization.
    seg_rot_axis = App.Vector(1, 0, 0)
    seg_rot_angle = -90
    
    color_seg  = (0.7, 0.7, 0.7)
    color_conn = (0.2, 0.2, 0.8)
    
    # Adjust spacing mathematically to show how legs attach to connector
    # segment length is body + pegs
    # However we're transforming the total shape. The pivot is the origin of the base shape.
    # Just space them out vertically.
    z_cursor = 0.0
    
    # Segment 1 (bottom)
    add_part_to_doc(doc, seg_shape, "LegSegment_1", App.Vector(0, 0, z_cursor), seg_rot_axis, seg_rot_angle, color_seg)
    z_cursor += params.SEGMENT_BODY_LENGTH / 2 + params.PEG_LENGTH / 2 + params.CONNECTOR_LENGTH / 2
    
    # Connector
    add_part_to_doc(doc, conn_shape, "LegConnector", App.Vector(0, 0, z_cursor), App.Vector(0, 0, 1), 0, color_conn)
    z_cursor += params.CONNECTOR_LENGTH / 2 + params.PEG_LENGTH / 2 + params.SEGMENT_BODY_LENGTH / 2
    
    # Segment 2 (top)
    add_part_to_doc(doc, seg_shape, "LegSegment_2", App.Vector(0, 0, z_cursor), seg_rot_axis, seg_rot_angle, color_seg)
    
    # 4. Export Assembly
    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, EXPORT_STEP)
    
    compound = Part.makeCompound([obj.Shape for obj in objs])
    compound.exportStl(EXPORT_STL)
    
    print(f"Assembly exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__":
    build_assembly()
