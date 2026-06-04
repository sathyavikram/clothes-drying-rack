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
EXPORT_STEP  = os.path.join(EXPORT_BASE, "part_05_top_bracket_rod_mount.step")
EXPORT_STL   = os.path.join(EXPORT_BASE, "part_05_top_bracket_rod_mount.stl")

def construct_rod_mount():
    LEG_W = params.LEG_WIDTH
    LEG_D = params.LEG_DEPTH
    PEG_L = params.PEG_LENGTH
    
    HUB_R = 20.0 * params.SCALE
    HUB_H = 25.0 * params.SCALE
    ARM_EXT = 40.0 * params.SCALE
    
    # Hub at (0,0,0) along Y axis
    hub_A = Part.makeCylinder(HUB_R, HUB_H, App.Vector(0, -HUB_H/2, 0), App.Vector(0,1,0))
    # Arm extends along +Z from Z=0 to Z=ARM_EXT
    body_A = Part.makeBox(LEG_W, LEG_D, ARM_EXT, App.Vector(-LEG_W/2, -LEG_D/2, 0))
    
    body_base = hub_A.fuse(body_A).removeSplitter()
    
    # ─── MALE THREAD at Top (Z = ARM_EXT) ──────────────────────────────────────
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    p2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    tm_sweep = Part.Solid(Part.Wire(tm_helix).makePipeShell([tm_wire], True, True))
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, 0))
    
    male_thread_base = tm_core.fuse(tm_sweep).removeSplitter()
    male_thread = male_thread_base.copy()
    male_thread.Placement = App.Placement(App.Vector(0, 0, ARM_EXT), App.Rotation(0,0,0,1))
    
    chamfer_m = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, ARM_EXT + t_length - t_pitch / 2 - 1)
    )
    end_cutter_m = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, ARM_EXT + t_length - 1)
    )
    
    male_peg_clean = male_thread.cut(end_cutter_m.cut(chamfer_m)).removeSplitter()
    
    # ─── Pivot Thread Cutter (Female inside the hub) ──────────────────────────
    p_pitch   = 4.0 * params.SCALE
    p_radius  = 8.0 * params.SCALE
    p_r_inner = p_radius - (p_pitch * 0.45)
    
    # Starts from Y = +HUB_H/2 (since part_05 is at -Y relative to part_06)
    start_y = HUB_H/2 + p_pitch
    p_length  = 19.0 + p_pitch * 2.0 
    
    p_helix = Part.makeHelix(p_pitch, p_length, p_r_inner, 0)
    
    inner_X_p = p_r_inner - 2.0 * params.SCALE
    p_1 = App.Vector(inner_X_p,  0, -p_pitch * 0.35)
    p_2 = App.Vector(p_radius, 0, -p_pitch * 0.10)
    p_3 = App.Vector(p_radius, 0,  p_pitch * 0.10)
    p_4 = App.Vector(inner_X_p,  0,  p_pitch * 0.35)
    p_wire = Part.Wire(Part.makePolygon([p_1, p_2, p_3, p_4, p_1]))

    p_sweep = Part.Solid(Part.Wire(p_helix).makePipeShell([p_wire], True, True))
    p_core  = Part.makeCylinder(p_r_inner, p_length, App.Vector(0, 0, 0))
    
    pivot_cutter_base = p_core.fuse(p_sweep).removeSplitter()
    pivot_cutter = pivot_cutter_base.copy()
    
    # Rotate from +Z to -Y: +90 around X sends +Z to -Y
    pivot_cutter.Placement = App.Placement(App.Vector(0, start_y, 0), App.Rotation(App.Vector(1,0,0), 90))
    
    # Chamfer at entry (Y = -HUB_H/2)
    pivot_chamfer = Part.makeCone(p_radius+1.0, p_radius-1.0, 2.0, App.Vector(0, -HUB_H/2 + 2.0, 0), App.Vector(0,-1,0))
    pivot_cutter = pivot_cutter.fuse(pivot_chamfer).removeSplitter()

    # Cut pivot thread into body
    shape_cut = body_base.cut(pivot_cutter).removeSplitter()
    
    shape = Part.makeCompound([shape_cut, male_peg_clean])
    
    # Print orientation: lie flat on Y face
    shape.Placement.Rotation = App.Rotation(App.Vector(1,0,0), 90)
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    
    return shape

def main():
    doc = App.newDocument("TopBracketRodMount")
    shape = construct_rod_mount()
    feature = doc.addObject("Part::Feature", "RodMount")
    feature.Shape = shape

if __name__ == "__main__":
    main()
