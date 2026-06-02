import FreeCAD as App
import Part
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from part_01_leg_segment import construct_leg_segment

shape = construct_leg_segment()

# Check faces
print(f"Volume: {shape.Volume}")
print(f"Num faces: {len(shape.Faces)}")
bboxes = shape.BoundBox
print(f"BBox: {bboxes}")

doc = App.newDocument()
feature = doc.addObject("Part::Feature", "Test")
feature.Shape = shape

print ("Are there any cylindrical faces?")
cyls = [f for f in shape.Faces if isinstance(f.Surface, Part.Cylinder)]
print(len(cyls))

# Find the hole
