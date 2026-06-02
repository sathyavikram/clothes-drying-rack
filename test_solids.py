import FreeCAD; import Part; s = Part.Shape(); s.read('exports/part_02_xframe_hinge.step'); print(len(s.Solids))
