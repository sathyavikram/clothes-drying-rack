import FreeCAD as App
import Part
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE  = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_09_rod_end_cap.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_09_rod_end_cap.stl")

def construct_rod_end_cap():
    outer_radius = params.LEG_WIDTH / 2.0  # 12.5mm
    
    cap_base_height = 2.0 * params.SCALE
    dome_radius = outer_radius
    
    # Base cylinder
    base = Part.makeCylinder(outer_radius, cap_base_height, App.Vector(0, 0, 0))
    
    # Dome (sphere cut by a plane)
    dome_height = 3.0 * params.SCALE
    r_sphere = (dome_height**2 + dome_radius**2) / (2 * dome_height)
    sphere = Part.makeSphere(r_sphere, App.Vector(0, 0, cap_base_height - r_sphere + dome_height))
    
    # Cut off everything below z = cap_base_height
    cutter = Part.makeCylinder(r_sphere + 10, r_sphere * 2, App.Vector(0, 0, cap_base_height - r_sphere * 2))
    dome = sphere.cut(cutter)
    
    cap_body = Part.makeCompound([base, dome])
    
    # ─── MALE THREAD (Bottom, Z = 0 pointing down into negative Z) ──────────
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    # Thread generated at origin (Z=0 to t_length)
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    p2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    tm_sweep = Part.Wire(tm_helix).makePipeShell([tm_wire], True, True)
    tm_sweep = Part.Solid(tm_sweep)
    
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, 0))
    male_peg_raw = Part.makeCompound([tm_core, tm_sweep])
    
    # Now position it so it points down from Z=0
    male_peg_raw.Placement = App.Placement(App.Vector(0, 0, -t_length), App.Rotation(0,0,0,1))
    
    # Chamfer at the tip of the peg (which is at Z = -t_length)
    chamfer_m = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, -t_length - 1)
    )
    end_cutter_m = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, -t_length - 2.0) 
    )
    
    male_peg = male_peg_raw.cut(end_cutter_m.cut(chamfer_m))
    
    shape = Part.makeCompound([cap_body, male_peg])
    shape.removeSplitter()
    
    # Print orientation: Peg pointing UP, dome pointing DOWN.
    # This requires a small brim/raft for the dome apex, but ensures perfect horizontal layers for the threads and no messy supports under the cap's shoulder overhang.
    shape.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 180)

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape

def main():
    doc = App.newDocument("RodEndCap")
    shape = construct_rod_end_cap()
    feature = doc.addObject("Part::Feature", "RodEndCap")
    feature.Shape = shape

if __name__ == "__main__":
    main()
