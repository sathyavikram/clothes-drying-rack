import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FREECAD_CMD = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"

def build():
    print(f"Building leg segment...")
    subprocess.run([FREECAD_CMD, "part_01_leg_segment.py"], cwd=CURRENT_DIR)
    
    print(f"Building assembly...")
    subprocess.run([FREECAD_CMD, "assembly.py"], cwd=CURRENT_DIR)

if __name__ == "__main__":
    build()
