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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")

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

def main():
    doc = App.newDocument("Phase4_Test")
    
    rod_mount = load_step("part_05_top_bracket_rod_mount.step")
    leg_mount = load_step("part_06_top_bracket_leg_mount.step")
    pin_shape = load_step("part_07_top_bracket_pin.step")
    
    # ─── Part 05 (Rod Mount - Bottom) ───
    # Stays at Z=0. Extends in +Y direction.
    add_part_to_doc(doc, rod_mount, "RodMount", (0.3, 0.8, 0.3))
    
    # ─── Part 06 (Leg Mount - Top) ───
    # Folded state stack:
    # Need to translate it up by Z=25.4 (like the Phase 3 hinge).
    # Wait, Phase 4 uses HUB_H = 25.0. 
    trans_z = App.Placement(App.Vector(0,0,25.4), App.Rotation(0,0,0,1))
    
    leg_mount_folded = leg_mount.copy()
    leg_mount_folded.Placement = trans_z.multiply(leg_mount.Placement)
    add_part_to_doc(doc, leg_mount_folded, "LegMount_Folded_0deg", (0.3, 0.6, 0.8))
    
    # Deployed state: rotate Leg Mount by 45 degrees around Z.
    rot_45 = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 45))
    leg_mount_deployed = leg_mount.copy()
    leg_mount_deployed.Placement = trans_z.multiply(rot_45.multiply(leg_mount.Placement))
    add_part_to_doc(doc, leg_mount_deployed, "LegMount_Deployed_45deg", (0.4, 0.5, 0.9))
    
    # ─── Pin ───
    # The pin from part_07 is flat on the bed (+Y). Rotate it back upright.
    pin_placed = pin_shape.copy()
    unrot_flat = App.Placement(App.Vector(0, -16.0, 0), App.Rotation(App.Vector(1,0,0), -90))
    shift_z = App.Placement(App.Vector(0, 0, 4.4), App.Rotation(0,0,0,1))
    pin_placed.Placement = shift_z.multiply(unrot_flat.multiply(pin_placed.Placement))
    add_part_to_doc(doc, pin_placed, "Pin", (0.8, 0.8, 0.2))

    objs = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
    Import.export(objs, os.path.join(EXPORT_BASE, "test_phase4.step"))
    print("Test assembly exported.")

if __name__ == "__main__":
    main()
