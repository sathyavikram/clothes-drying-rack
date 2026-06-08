SCALE = 1.0

import os

# ─── Build plate ──────────────────────────────────────────────────────────────
BUILD_PLATE_X        = 175.0 * SCALE
BUILD_PLATE_Y        = 175.0 * SCALE
BUILD_PLATE_Z        = 175.0 * SCALE

# ─── Overall rack dimensions (79" variant) ────────────────────────────────────
# Source: specs/tech-stack.md — imperial → mm
RACK_LENGTH_MIN      = 1298.0 * SCALE   # 51.1" deployed minimum
RACK_LENGTH_MAX      = 2007.0 * SCALE   # 79.0" deployed maximum
RACK_HEIGHT          = 1300.0 * SCALE   # 51.2" total height
RACK_DEPTH           =  490.0 * SCALE   # 19.3" depth (rod-to-rod)
FOOT_SPREAD          =  699.0 * SCALE   # 27.5" foot spread (deployed)
FOLDED_LENGTH        = 1430.0 * SCALE   # 56.3" folded length
FOLDED_THICKNESS     =  102.0 * SCALE   # 4.0" folded thickness

# ─── Leg profile (Rectangular) ────────────────────────────────────────────────
LEG_WIDTH            =   25.0 * SCALE   # outer width
LEG_DEPTH            =   25.0 * SCALE   # outer depth
LEG_WALL             =    3.0 * SCALE   # wall thickness
SEGMENT_BODY_LENGTH  =  170.0 * SCALE

# ─── Threaded Cylindrical Peg joinery (Phase 2) ──────────────────────────────────
# Inner cavity needs space for threaded peg
# Thread nominal radius is less than inner dimension half
PEG_THREAD_RADIUS    = ((LEG_WIDTH - 2*LEG_WALL) / 2) - 0.5 * SCALE
PEG_THREAD_PITCH     = 6.0 * SCALE
PEG_LENGTH           = 25.0 * SCALE

# ─── Rod profile (drying rods share leg profile) ──────────────────────────────
ROD_WIDTH            = LEG_WIDTH
ROD_DEPTH            = LEG_DEPTH
ROD_WALL             = LEG_WALL

# ─── Side-arm rod (retractable lower-right rod) ───────────────────────────────
SIDE_ARM_LENGTH      =  300.0 * SCALE   # estimated from reference images

# ─── Tolerances ───────────────────────────────────────────────────────────────
TOLERANCE_SLIDING    =    0.4 * SCALE   # sliding-fit clearance per side
TOLERANCE_PRESS      =    0.2 * SCALE   # press-fit interference per side

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR  = os.path.join(PROJECT_DIR, "exports")

if __name__ == "__main__":
    for k, v in globals().items():
        if k.isupper() and isinstance(v, (int, float, str)):
            print(f"{k} = {v}")

# ─── Threading and Clearance ──────────────────────────────────────────────────
THREAD_CLEARANCE     = 0.6 * SCALE   # shrink male thread OD for easy rotation after printing
GENERAL_CLEARANCE    = 0.4 * SCALE   # sliding fits, pins
