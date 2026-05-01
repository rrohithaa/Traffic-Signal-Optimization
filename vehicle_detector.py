# =============================================================================
# config.py - Central configuration for AI Traffic Signal Optimization System
# =============================================================================

# ── Window / Display ──────────────────────────────────────────────────────────
WINDOW_WIDTH  = 900
WINDOW_HEIGHT = 900
WINDOW_TITLE  = "AI Traffic Signal Optimization"
FPS           = 60

# ── Intersection geometry ─────────────────────────────────────────────────────
ROAD_WIDTH      = 120          # pixels – width of each road arm
LANE_WIDTH      = ROAD_WIDTH // 2
CENTER_X        = WINDOW_WIDTH  // 2
CENTER_Y        = WINDOW_HEIGHT // 2

# ── Colours (R, G, B) ─────────────────────────────────────────────────────────
COLOR_BG         = (40,  40,  40)
COLOR_ROAD       = (70,  70,  70)
COLOR_LANE_MARK  = (200, 200, 200)
COLOR_SIDEWALK   = (110, 100,  90)
COLOR_RED        = (220,  50,  50)
COLOR_GREEN      = (50,  200,  80)
COLOR_YELLOW     = (230, 200,  40)
COLOR_WHITE      = (255, 255, 255)
COLOR_BLACK      = (0,    0,   0)
COLOR_PANEL_BG   = (20,  20,  20)
COLOR_ACCENT     = (0,  180, 220)
COLOR_VEHICLE    = {
    "NS": (100, 160, 255),   # blue-ish for North/South vehicles
    "EW": (255, 160,  80),   # orange-ish for East/West vehicles
}

# ── Traffic signal timing ─────────────────────────────────────────────────────
MIN_GREEN_TIME   = 5           # seconds
MAX_GREEN_TIME   = 30          # seconds
YELLOW_TIME      = 3           # seconds (fixed)
DEFAULT_GREEN    = 10          # seconds

# ── AI / Q-Learning ───────────────────────────────────────────────────────────
ALPHA            = 0.1         # learning rate
GAMMA            = 0.9         # discount factor
EPSILON_START    = 1.0         # initial exploration rate
EPSILON_MIN      = 0.05
EPSILON_DECAY    = 0.995
Q_TABLE_PATH     = "models/q_table.npy"

# Discrete green-time actions available to the agent (seconds)
ACTIONS          = [5, 8, 10, 12, 15, 20, 25, 30]

# ── Traffic / vehicle simulation ──────────────────────────────────────────────
MAX_VEHICLES_PER_LANE = 12
VEHICLE_SPEED         = 2.5    # pixels per frame while moving
VEHICLE_LENGTH        = 24
VEHICLE_WIDTH         = 14
SPAWN_INTERVAL        = 45     # frames between spawn attempts per lane
MAX_DENSITY           = 10     # max cars counted from video per lane

# ── Computer-vision / video input ────────────────────────────────────────────
FRAME_SKIP            = 5      # process every Nth video frame
DETECT_SENSITIVITY    = 500    # min contour area to count as a vehicle

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_FILE              = "output_logs/metrics.csv"
LOG_INTERVAL_FRAMES   = 120    # write a log row every N frames

# ── Directions ────────────────────────────────────────────────────────────────
DIRECTIONS = ["North", "South", "East", "West"]
NS_PAIR    = ["North", "South"]
EW_PAIR    = ["East",  "West"]
