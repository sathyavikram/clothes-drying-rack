import FreeCAD as App
import Part
import params

t_pitch   = params.PEG_THREAD_PITCH
tf_radius  = params.PEG_THREAD_RADIUS
tf_r_inner = tf_radius - (t_pitch * 0.45)
tf_length_cut = params.PEG_LENGTH + 2.0
tf_total_len = tf_length_cut + t_pitch*2

helix = Part.makeHelix(t_pitch, tf_total_len, tf_r_inner, 0)
f1 = App.Vector(5.2,  0, -t_pitch * 0.35)
f2 = App.Vector(9.0, 0, -t_pitch * 0.10)
f3 = App.Vector(9.0, 0,  t_pitch * 0.10)
f4 = App.Vector(5.2,  0,  t_pitch * 0.35)
tf_wire = Part.Wire(Part.makePolygon([f1, f2, f3, f4, f1]))

# Create solid shell and core, fuse them
tf_sweep = Part.Solid(Part.Wire(helix).makePipeShell([tf_wire], True, True))
tf_core  = Part.makeCylinder(tf_r_inner, tf_total_len)
# tf_core is at origin Z=0 to tf_total_len

thread_cutter_base = tf_core.fuse(tf_sweep).removeSplitter()

# Place it where it belongs
tf_start_z = -170.0/2.0 - t_pitch
thread_cutter = thread_cutter_base.copy()
thread_cutter.Placement.Base = App.Vector(0, 0, tf_start_z)

# Create body
body = Part.makeBox(25, 25, 170)
body.Placement.Base = App.Vector(-12.5, -12.5, -85)

inner_box = Part.makeBox(19, 19, 110)
inner_box.Placement.Base = App.Vector(-9.5, -9.5, -55)
body = body.cut(inner_box)

print("Body faces:", len(body.Faces))
result = body.cut(thread_cutter)
print("Result faces:", len(result.Faces))
print("Result volume:", result.Volume)
print("Body volume:", body.Volume)

# Are there cylindrical faces?
cyls = [f for f in result.Faces if isinstance(f.Surface, Part.Cylinder)]
print("Cylindrical faces:", len(cyls))

