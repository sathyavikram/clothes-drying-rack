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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_07_threaded_adapter_pin.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_07_threaded_adapter_pin.stl")

def construct_threaded_adapter_pin():
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.ADAPTER_PIN_LENGTH
    
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    # ─── CONTINUOUS MALE THREAD ───────────────────────────────────────────────
    # We build it starting from Z=0, then we will translate it so it's centered at origin
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    p2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    tm_sweep = Part.Wire(tm_helix).makePipeShell([tm_wire], True, True)
    
    tm_core = Part.makeCylinder(tm_r_inner, t_length)
    
    # Chamfer at both ends
    chamfer_top = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, t_length - t_pitch / 2 - 1)
    )
    end_cutter_top = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, t_length - 1)
    )
    
    chamfer_bottom = Part.makeCone(
        tm_r_inner, tm_radius + 2.0,
        t_pitch / 2 + 1,
        App.Vector(0, 0, -1)
    )
    end_cutter_bottom = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, -t_pitch - 1)
    )
    
    tm_sweep = tm_sweep.cut(end_cutter_top.cut(chamfer_top))
    tm_sweep = tm_sweep.cut(end_cutter_bottom.cut(chamfer_bottom))
    tm_core = tm_core.cut(end_cutter_top.cut(chamfer_top))
    tm_core = tm_core.cut(end_cutter_bottom.cut(chamfer_bottom))
    
    shape = Part.makeCompound([tm_core, tm_sweep])
    
    # Center the pin at the origin
    shape.Placement.Base = App.Vector(0, 0, -t_length / 2)
    
    # Print orientation: vertical printing is best for threaded shafts
    # So we leave it aligned with Z axis.
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return shape

def main():
    doc = App.newDocument("ThreadedAdapterPin")
    shape = construct_threaded_adapter_pin()
    feature = doc.addObject("Part::Feature", "ThreadedAdapterPin")
    feature.Shape = shape

if __name__ == "__main__":
    main()
