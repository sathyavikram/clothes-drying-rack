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
    
    outer_box = Part.makeBox(w, d, l)
    outer_box.Placement.Base = App.Vector(-w/2, -d/2, -l/2)
    inner_w = w - 2*wall
    inner_d = d - 2*wall
    inner_box = Part.makeBox(inner_w, inner_d, l + 2)
    inner_box.Placement.Base = App.Vector(-inner_w/2, -inner_d/2, -l/2 - 1)
    
    body = outer_box.cut(inner_box)
    
    peg_w = params.PEG_WIDTH
    peg_d = params.PEG_DEPTH
    peg_l = params.PEG_LENGTH
    peg1 = Part.makeBox(peg_w, peg_d, peg_l)
    peg1.Placement.Base = App.Vector(-peg_w/2, -peg_d/2, l/2)
    
    # GROOVES on MALE PEG
    r = params.SNAP_BUMP_DEPTH
    offset = 2.5 * params.SCALE
    
    g_left = Part.makeCylinder(r, peg_d + 2*r)
    g_left.Placement.Rotation = App.Rotation(App.Vector(1,0,0), -90)
    g_left.Placement.Base = App.Vector(-peg_w/2, -peg_d/2 - r, l/2 + offset)
    
    g_right = Part.makeCylinder(r, peg_d + 2*r)
    g_right.Placement.Rotation = App.Rotation(App.Vector(1,0,0), -90)
    g_right.Placement.Base = App.Vector(peg_w/2, -peg_d/2 - r, l/2 + offset)
    
    peg_cut = peg1.cut(g_left).cut(g_right)
    
    # BUMPS on FEMALE SOCKET
    # Female opening is at Z = -l/2
    b_left = Part.makeCylinder(r, inner_d)
    b_left.Placement.Rotation = App.Rotation(App.Vector(1,0,0), -90)
    b_left.Placement.Base = App.Vector(-inner_w/2, -inner_d/2, -l/2 + offset)
    
    b_right = Part.makeCylinder(r, inner_d)
    b_right.Placement.Rotation = App.Rotation(App.Vector(1,0,0), -90)
    b_right.Placement.Base = App.Vector(inner_w/2, -inner_d/2, -l/2 + offset)
    
    # Wait, the cylinder at -inner_w/2 extends outward into the positive X? 
    # No, cylinder is symmetric around its axis. If we place it at -inner_w/2, its radius r goes from X = -inner_w/2 - r to -inner_w/2 + r.
    # We want it to be a bump INSIDE the female socket.
    # The female wall is at X = -inner_w/2. So the cylinder half-sticks into the empty space.
    # This is perfect.
    
    body_with_bumps = body.fuse(b_left).fuse(b_right).removeSplitter()
    
    shape = body_with_bumps.fuse(peg_cut).removeSplitter()
    shape.exportStep("exports/test_snap.step")
    print("Done")

if __name__ == "__main__":
    main()
