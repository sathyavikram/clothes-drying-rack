import FreeCAD as App
import Part
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    sys.path.append(os.getcwd())
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR = os.getcwd()
EXPORT_BASE  = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_01b_tube_sleeve.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_01b_tube_sleeve.stl")

def make_female_thread_cutter(start_z):
    t_pitch   = params.THREAD_PITCH
    t_radius  = params.THREAD_NOM_RADIUS
    t_r_inner = t_radius - (t_pitch * 0.45)
    t_length  = params.THREAD_LENGTH

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(0,0,0,1))
    
    t_core  = Part.makeCylinder(t_r_inner, t_length + 2.0 * params.SCALE, App.Vector(0, 0, start_z - 1.0 * params.SCALE))

    return t_core.fuse(t_sweep).removeSplitter()

def make_female_thread_cutter_inverted(start_z):
    t_pitch   = params.THREAD_PITCH
    t_radius  = params.THREAD_NOM_RADIUS
    t_r_inner = t_radius - (t_pitch * 0.45)
    t_length  = params.THREAD_LENGTH

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0, 0, start_z), App.Rotation(1,0,0,0))
    
    t_core  = Part.makeCylinder(t_r_inner, t_length + 2.0 * params.SCALE, App.Vector(0, 0, start_z - t_length - 1.0 * params.SCALE))

    return t_core.fuse(t_sweep).removeSplitter()

def construct_tube_sleeve():
    body = Part.makeCylinder(params.SLEEVE_OD / 2, params.SLEEVE_LENGTH)
    
    offset = params.SPIGOT_LENGTH - params.THREAD_LENGTH # 5 mm entry
    
    # 5 mm entry clearance bore at both ends
    # We use GENERAL_CLEARANCE to the radius of the clearance hole so the spigot base slides in easily
    entry_radius = params.THREAD_NOM_RADIUS + params.GENERAL_CLEARANCE
    entry_bot = Part.makeCylinder(entry_radius, offset + 0.1, App.Vector(0,0,0))
    entry_top = Part.makeCylinder(entry_radius, offset + 0.1, App.Vector(0,0,params.SLEEVE_LENGTH - offset))
    
    # Thread cutters starting past the 5 mm entry
    tc_bot = make_female_thread_cutter(offset)
    tc_top = make_female_thread_cutter_inverted(params.SLEEVE_LENGTH - offset)
    
    body = body.cut(entry_bot).cut(entry_top)
    body = body.cut(tc_bot).cut(tc_top)
    body = body.removeSplitter()

    # Print orientation: standing upright

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    body.exportStep(EXPORT_STEP)
    body.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    print(f"Volume: {body.Volume}")
    return body

def main():
    doc = App.newDocument("TubeSleeve")
    shape = construct_tube_sleeve()
    feature = doc.addObject("Part::Feature", "TubeSleeve")
    feature.Shape = shape

if __name__ == "__main__":
    main()
