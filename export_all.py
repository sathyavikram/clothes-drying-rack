import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FREECAD_CMD = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"

def build():
    print(f"Building leg segment...")
    subprocess.run([FREECAD_CMD, "-c", "import sys; sys.path.append('.'); import part_01_leg_segment; part_01_leg_segment.main()"], cwd=CURRENT_DIR)

    print(f"Building hinge bottom...")
    subprocess.run([FREECAD_CMD, "-c", "import sys; sys.path.append('.'); import part_02_xframe_hinge_bottom; part_02_xframe_hinge_bottom.main()"], cwd=CURRENT_DIR)

    print(f"Building hinge top...")
    subprocess.run([FREECAD_CMD, "-c", "import sys; sys.path.append('.'); import part_03_xframe_hinge_top; part_03_xframe_hinge_top.main()"], cwd=CURRENT_DIR)

    print(f"Building hinge pin...")
    subprocess.run([FREECAD_CMD, "-c", "import sys; sys.path.append('.'); import part_04_xframe_hinge_pin; part_04_xframe_hinge_pin.main()"], cwd=CURRENT_DIR)
    
    print(f"Building assembly...")
    subprocess.run([FREECAD_CMD, "-c", "import sys; sys.path.append('.'); import assembly; assembly.build_assembly()"], cwd=CURRENT_DIR)

if __name__ == "__main__":
    build()
