import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FREECAD_CMD = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")

def build_all():
    scripts = [f for f in os.listdir(CURRENT_DIR) if f.startswith("part_") and f.endswith(".py")]
    
    success = 0
    for script in scripts:
        print(f"Building {script}...")
        try:
            res = subprocess.run([FREECAD_CMD, script], cwd=CURRENT_DIR, capture_output=True, text=True)
            for line in res.stdout.splitlines():
                if "Exported to" in line or "Assembly exported to" in line or "Error" in line or "Warning" in line or "failed" in line:
                    print("  " + line)
            if res.returncode == 0:
                success += 1
            else:
                print(f"  Failed with exit code: {res.returncode}")
        except Exception as e:
            print(f"  Execution error: {e}")
            
    print(f"--- Export Summary ---")
    print(f"Successfully processed {success}/{len(scripts)} part scripts.")

    print(f"Building assembly.py...")
    try:
        res = subprocess.run([FREECAD_CMD, "assembly.py"], cwd=CURRENT_DIR, capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if "Assembly exported to" in line or "Error" in line or "Warning" in line or "failed" in line:
                print("  " + line)
    except Exception as e:
        print(f"  Execution error: {e}")

if __name__ == "__main__":
    build_all()
