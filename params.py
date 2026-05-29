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

# ─── Tube profile (leg tubes) ─────────────────────────────────────────────────
# Estimated from reference images; adjust if measured values differ
TUBE_OD              =   25.0 * SCALE   # outer diameter
TUBE_WALL            =    3.0 * SCALE   # wall thickness (updated for Phase 2)
TUBE_ID              = TUBE_OD - 2.0 * TUBE_WALL   # inner diameter (derived = 19mm)
SEGMENT_BODY_LENGTH  =  170.0 * SCALE

# ─── Threaded Spigot & Sleeve joinery (Phase 2) ───────────────────────────────
THREAD_CLEARANCE       = 0.6 * SCALE
GENERAL_CLEARANCE      = 0.4 * SCALE
THREAD_NOM_RADIUS      = 10.0 * SCALE   # nominal 20 mm OD thread
THREAD_PITCH           = 4.0 * SCALE
THREAD_LENGTH          = 20.0 * SCALE
SPIGOT_OD              = 20.0 * SCALE
SPIGOT_LENGTH          = 25.0 * SCALE
SLEEVE_OD              = 34.0 * SCALE
SLEEVE_LENGTH          = 60.0 * SCALE
SLEEVE_BORE_DEPTH      = 25.0 * SCALE

# ─── Rod profile (drying rods share leg-tube profile) ────────────────────────
ROD_OD               = TUBE_OD
ROD_WALL             = TUBE_WALL
ROD_ID               = TUBE_ID          # derived

# ─── Side-arm rod (retractable lower-right rod) ───────────────────────────────
SIDE_ARM_LENGTH      =  300.0 * SCALE   # estimated from reference images

# ─── Tolerances ───────────────────────────────────────────────────────────────
TOLERANCE_SLIDING    =    0.4 * SCALE   # sliding-fit clearance per side
TOLERANCE_PRESS      =    0.2 * SCALE   # press-fit interference per side

# ─── FDM print constraints ────────────────────────────────────────────────────
WALL_MIN_STRUCTURAL  =    3.0 * SCALE   # minimum structural wall thickness
WALL_MIN_COSMETIC    =    2.0 * SCALE   # minimum cosmetic wall thickness
SEGMENT_MAX          =  160.0 * SCALE   # max segment length (build-plate limit)

# ─── Hardware clearance holes ─────────────────────────────────────────────────
BOLT_DIA_M4          =    4.0 * SCALE
BOLT_DIA_M5          =    5.0 * SCALE
BOLT_HOLE_CLEAR_M4   =    4.5 * SCALE   # M4 clearance
BOLT_HOLE_CLEAR_M5   =    5.5 * SCALE   # M5 clearance

# ─── Locking hinge bracket ────────────────────────────────────────────────────
HINGE_LENGTH         =   80.0 * SCALE   # plate long axis
HINGE_WIDTH          =   30.0 * SCALE   # plate short axis
HINGE_THICKNESS      =    5.0 * SCALE   # plate thickness
HINGE_PIN_DIA        =    6.0 * SCALE   # pivot pin/bolt diameter

# ─── Anti-slip foot cap ───────────────────────────────────────────────────────
FOOT_CAP_HEIGHT      =   20.0 * SCALE
FOOT_CAP_WALL        =    3.0 * SCALE
FOOT_CAP_ID          = TUBE_OD + TOLERANCE_SLIDING          # slides over leg tube (derived)
FOOT_CAP_OD          = FOOT_CAP_ID + 2.0 * FOOT_CAP_WALL   # outer diameter (derived)

# ─── Rod end cap (press-fit plug) ─────────────────────────────────────────────
ROD_END_CAP_HEIGHT   =   15.0 * SCALE
ROD_END_CAP_OD       = ROD_ID - TOLERANCE_PRESS             # press-fit into rod bore (derived)

# ─── Windproof hook ───────────────────────────────────────────────────────────
HOOK_CLIP_ID         = ROD_OD + TOLERANCE_SLIDING           # jaw opening (derived)
HOOK_BODY_THICKNESS  =    3.0 * SCALE
HOOK_LENGTH          =   40.0 * SCALE
HOOK_OPENING         =    8.0 * SCALE   # snap-on gap

# ─── Paths ────────────────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR  = os.path.join(PROJECT_DIR, "exports")


# ─── Smoke-test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _fields = [
        ("SCALE",               SCALE,               ""),
        ("BUILD_PLATE_X",       BUILD_PLATE_X,       "mm"),
        ("BUILD_PLATE_Y",       BUILD_PLATE_Y,       "mm"),
        ("BUILD_PLATE_Z",       BUILD_PLATE_Z,       "mm"),
        ("RACK_LENGTH_MIN",     RACK_LENGTH_MIN,     "mm"),
        ("RACK_LENGTH_MAX",     RACK_LENGTH_MAX,     "mm"),
        ("RACK_HEIGHT",         RACK_HEIGHT,         "mm"),
        ("RACK_DEPTH",          RACK_DEPTH,          "mm"),
        ("FOOT_SPREAD",         FOOT_SPREAD,         "mm"),
        ("FOLDED_LENGTH",       FOLDED_LENGTH,       "mm"),
        ("FOLDED_THICKNESS",    FOLDED_THICKNESS,    "mm"),
        ("TUBE_OD",             TUBE_OD,             "mm"),
        ("TUBE_WALL",           TUBE_WALL,           "mm"),
        ("TUBE_ID",             TUBE_ID,             "mm  (derived)"),
        ("SEGMENT_BODY_LENGTH", SEGMENT_BODY_LENGTH, "mm"),
        ("THREAD_CLEARANCE",    THREAD_CLEARANCE,    "mm"),
        ("GENERAL_CLEARANCE",   GENERAL_CLEARANCE,   "mm"),
        ("THREAD_NOM_RADIUS",   THREAD_NOM_RADIUS,   "mm"),
        ("THREAD_PITCH",        THREAD_PITCH,        "mm"),
        ("THREAD_LENGTH",       THREAD_LENGTH,       "mm"),
        ("SPIGOT_OD",           SPIGOT_OD,           "mm"),
        ("SPIGOT_LENGTH",       SPIGOT_LENGTH,       "mm"),
        ("SLEEVE_OD",           SLEEVE_OD,           "mm"),
        ("SLEEVE_LENGTH",       SLEEVE_LENGTH,       "mm"),
        ("SLEEVE_BORE_DEPTH",   SLEEVE_BORE_DEPTH,   "mm"),
        ("ROD_OD",              ROD_OD,              "mm"),
        ("ROD_WALL",            ROD_WALL,            "mm"),
        ("ROD_ID",              ROD_ID,              "mm  (derived)"),
        ("SIDE_ARM_LENGTH",     SIDE_ARM_LENGTH,     "mm"),
        ("TOLERANCE_SLIDING",   TOLERANCE_SLIDING,   "mm"),
        ("TOLERANCE_PRESS",     TOLERANCE_PRESS,     "mm"),
        ("WALL_MIN_STRUCTURAL", WALL_MIN_STRUCTURAL, "mm"),
        ("WALL_MIN_COSMETIC",   WALL_MIN_COSMETIC,   "mm"),
        ("SEGMENT_MAX",         SEGMENT_MAX,         "mm"),
        ("BOLT_DIA_M4",         BOLT_DIA_M4,         "mm"),
        ("BOLT_DIA_M5",         BOLT_DIA_M5,         "mm"),
        ("BOLT_HOLE_CLEAR_M4",  BOLT_HOLE_CLEAR_M4,  "mm"),
        ("BOLT_HOLE_CLEAR_M5",  BOLT_HOLE_CLEAR_M5,  "mm"),
        ("HINGE_LENGTH",        HINGE_LENGTH,        "mm"),
        ("HINGE_WIDTH",         HINGE_WIDTH,         "mm"),
        ("HINGE_THICKNESS",     HINGE_THICKNESS,     "mm"),
        ("HINGE_PIN_DIA",       HINGE_PIN_DIA,       "mm"),
        ("FOOT_CAP_HEIGHT",     FOOT_CAP_HEIGHT,     "mm"),
        ("FOOT_CAP_WALL",       FOOT_CAP_WALL,       "mm"),
        ("FOOT_CAP_ID",         FOOT_CAP_ID,         "mm  (derived)"),
        ("FOOT_CAP_OD",         FOOT_CAP_OD,         "mm  (derived)"),
        ("ROD_END_CAP_HEIGHT",  ROD_END_CAP_HEIGHT,  "mm"),
        ("ROD_END_CAP_OD",      ROD_END_CAP_OD,      "mm  (derived)"),
        ("HOOK_CLIP_ID",        HOOK_CLIP_ID,        "mm  (derived)"),
        ("HOOK_BODY_THICKNESS", HOOK_BODY_THICKNESS, "mm"),
        ("HOOK_LENGTH",         HOOK_LENGTH,         "mm"),
        ("HOOK_OPENING",        HOOK_OPENING,        "mm"),
        ("PROJECT_DIR",         PROJECT_DIR,         "path"),
        ("EXPORT_DIR",          EXPORT_DIR,          "path"),
    ]
    _col = max(len(n) for n, *_ in _fields) + 2
    print(f'\n{"─" * 60}')
    print(f'  params.py — 79" variant (SCALE={SCALE})')
    print(f'{"─" * 60}')
    for name, val, unit in _fields:
        if isinstance(val, float):
            print(f"  {name:<{_col}} {val:>10.2f}  {unit}")
        else:
            print(f"  {name:<{_col}} {str(val):>10}  {unit}")
    print(f'{"─" * 60}\n')
