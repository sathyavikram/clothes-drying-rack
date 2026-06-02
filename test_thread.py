import FreeCAD as App
import Part
import os
import sys

import params

def main():
    w = params.LEG_WIDTH
    d = params.LEG_DEPTH
    l = 40.0
    wall = params.LEG_WALL
    
    # Body (Solid Rectangular for test)
    body = Part.makeBox(w, d, l)
    body.Placement.Base = App.Vector(-w/2, -d/2, -l/2)
    
    # Male Peg (Top)
    t_pitch   = params.PEG_THREAD_PITCH
    t_length  = params.PEG_LENGTH
    
    # MALE THREAD
    tm_radius  = params.PEG_THREAD_RADIUS - params.THREAD_CLEARANCE
    tm_r_inner = tm_radius - (t_pitch * 0.45)
    
    tm_helix = Part.makeHelix(t_pitch, t_length, tm_r_inner, 0)
    
    inner_X_m = tm_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X_m,  0, -t_pitch * 0.35)
    p2 = App.Vector(tm_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(tm_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X_m,  0,  t_pitch * 0.35)
    tm_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    tm_sweep = Part.Wire(tm_helix).makePipeShell([tm_wire], True, True)
    tm_sweep.Placement = App.Placement(App.Vector(0, 0, l/2), App.Rotation(0,0,0,1))
    
    tm_core = Part.makeCylinder(tm_r_inner, t_length, App.Vector(0, 0, l/2))
    
    # Tip chamfer on male thread
    chamfer = Part.makeCone(
        tm_radius + 2.0, tm_r_inner,
        t_pitch / 2 + 1,
        App.Vector(0, 0, l/2 + t_length - t_pitch / 2 - 1)
    )
    end_cutter = Part.makeCylinder(
        tm_radius + 5.0, t_pitch + 2.0,
        App.Vector(0, 0, l/2 + t_length - 1)
    )
    
    male_thread_base = tm_core.fuse(tm_sweep).removeSplitter()
    male_peg = male_thread_base.cut(end_cutter.cut(chamfer)).removeSplitter()
    
    body = body.fuse(male_peg).removeSplitter()
    
    # FEMALE SOCKET (Bottom)
    tf_radius  = params.PEG_THREAD_RADIUS
    tf_r_inner = tf_radius - (t_pitch * 0.45)
    
    # Start the female thread exactly an integer number of pitches below -l/2
    # to maintain timing. Let's do 1 pitch below.
    tf_length_cut = t_length + 2.0
    tf_start_z = -l/2 - t_pitch
    tf_total_len = tf_length_cut + t_pitch*2
    
    tf_helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
    
    inner_X_f = tf_r_inner - 2.0 * params.SCALE
    f1 = App.Vector(inner_X_f,  0, -t_pitch * 0.35)
    f2 = App.Vector(tf_radius, 0, -t_pitch * 0.10)
    f3 = App.Vector(tf_radius, 0,  t_pitch * 0.10)
    f4 = App.Vector(inner_X_f,  0,  t_pitch * 0.35)
    tf_wire = Part.Wire(Part.makePolygon([f1, f2, f3, f4, f1]))
    
    tf_sweep = Part.Wire(tf_helix).makePipeShell([tf_wire], True, True)
    tf_sweep.Placement = App.Placement(App.Vector(0, 0, tf_start_z), App.Rotation(0,0,0,1))
    
    tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len, App.Vector(0, 0, tf_start_z))
    thread_cutter = tf_core.fuse(tf_sweep).removeSplitter()
    
    body = body.cut(thread_cutter).removeSplitter()
    
    body.exportStep("exports/test_thread.step")
    print("Done")

if __name__ == "__main__":
    main()
