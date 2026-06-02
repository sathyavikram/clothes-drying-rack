import FreeCAD as App
import Part
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from part_01_leg_segment import construct_leg_segment

shape = construct_leg_segment()
# it's a compound. Let's look at the sub-shapes
for i, sub in enumerate(shape.Solids):
    print(f"Solid {i}: Volume={sub.Volume}")
    print(f"  X={sub.BoundBox.XMin} to {sub.BoundBox.XMax}")
    print(f"  Y={sub.BoundBox.YMin} to {sub.BoundBox.YMax}")
    print(f"  Z={sub.BoundBox.ZMin} to {sub.BoundBox.ZMax}")

print("Faces for Solid 0:")
for i, f in enumerate(shape.Solids[0].Faces):
    print(f"  Face {i}: {f.Surface}")

