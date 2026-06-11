#!/usr/bin/env python
import os
import subprocess
import sys

SCRIPTS = [
    "part_01_leg_segment.py",
    "part_02_xframe_hinge_bottom.py",
    "part_03_xframe_hinge_top.py",
    "part_04_xframe_hinge_pin.py",
    "part_05_top_l_bracket.py",
    "part_06_drying_rod.py",
    "part_07_threaded_adapter_pin.py",
    "part_08_foot_cap.py",
    "assembly.py"
]

FREECAD_CMD = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
if not os.path.exists(FREECAD_CMD):
    FREECAD_CMD = "freecadcmd"

def main():
    print(f"Starting batched export of {len(SCRIPTS)} scripts...")
    success_count = 0
    
    for script in SCRIPTS:
        if not os.path.exists(script):
            print(f"Warning: {script} not found. Skipping.")
            continue
            
        print(f"\n--- Running {script} ---")
        try:
            # Execute exactly how run.sh would execute them to ensure __main__ issues are bypassed
            # run.sh handles calling the .main() or .build_assembly() proper hook
            script_arg = script
            if script == "assembly.py":
                script_arg = "assembly"
                
            cmd = ["./run.sh", script_arg]
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout + "\n" + result.stderr
            
            for line in output.split('\n'):
                if "Exported to" in line or "Error" in line or "Exception" in line or "Traceback" in line:
                    print(line)
            
            if result.returncode == 0 and "Traceback" not in output:
                success_count += 1
            else:
                print(f"!!! Error detected in {script}")
                
        except Exception as e:
            print(f"Failed to execute {script}: {e}")
            
    print(f"\nFinished. {success_count}/{len(SCRIPTS)} scripts executed successfully.")
    
if __name__ == "__main__":
    main()
