# AI Traffic Signal Optimization System

A real-time, AI-driven traffic signal controller that uses **Q-Learning**
to dynamically adjust green-light durations at a 4-way intersection, minimising
average vehicle waiting time and maximising throughput.

---

## Features

| Feature | Details |
|---|---|
| AI Algorithm | Tabular Q-Learning (ε-greedy policy) |
| Simulation | Pygame 4-way intersection with animated vehicles |
| Input Mode 1 | Pure simulation (random density generator) |
| Input Mode 2 | Aerial video processed with OpenCV (MOG2 background subtraction) |
| Metrics | Avg wait time · Queue length · Throughput · Signal efficiency |
| Logging | CSV log in `output_logs/metrics.csv` |
| Persistence | Q-table auto-saved to `models/q_table.npy` |

---

## Quick Start (Windows)

```
double-click  run_project.bat
```

The BAT file will:
1. Check / install Python 3.11
2. Check pip
3. Create a virtual environment (`venv/`)
4. Install all dependencies
5. Launch `main.py`

---

## Manual Run

```bash
# Activate venv (after first run of run_project.bat)
venv\Scripts\activate

# Simulation mode (no video required)
python main.py

# Video input mode
python main.py --video input_videos\your_traffic_video.mp4

# Skip saving Q-table on exit
python main.py --no-save
```

---

## Project Structure

```
AI_Traffic_Signal_Optimization/
│
├── main.py                 # Entry point – orchestrates all modules
├── simulation.py           # Pygame rendering + vehicle physics
├── traffic_controller.py   # Signal phase state machine
├── vehicle_detector.py     # OpenCV vehicle counter (video mode)
├── traffic_generator.py    # Synthetic density generator (sim mode)
├── ai_optimizer.py         # Q-Learning agent
├── config.py               # All tunable constants
│
├── requirements.txt
├── run_project.bat         # One-click setup & launch (Windows)
├── README.md
│
├── models/
│   └── q_table.npy         # Persisted Q-table (auto-created)
├── input_videos/           # Place aerial traffic videos here
├── output_logs/
│   └── metrics.csv         # Per-cycle performance log
└── assets/                 # Optional images / fonts
```

---

## AI Algorithm Detail

### State Space
Each state is a 2-tuple:
```
(density_bucket_primary, density_bucket_secondary)
```
where each bucket is in `[0, 4]` (5 levels for `MAX_DENSITY = 10`).

### Action Space
8 discrete green-time durations (seconds):
```
[5, 8, 10, 12, 15, 20, 25, 30]
```

### Reward Function
```
reward = vehicles_cleared * 0.5 − 1.0
```
A phase that clears many vehicles earns a higher (less negative) reward.

### Q-Update (Bellman)
```
Q(s,a) ← Q(s,a) + α [ r + γ · max Q(s',·) − Q(s,a) ]
```

| Hyper-parameter | Value |
|---|---|
| α (learning rate) | 0.10 |
| γ (discount) | 0.90 |
| ε start | 1.00 |
| ε min | 0.05 |
| ε decay | 0.995 per step |

---

## Signal Phase Cycle

```
Phase 0 → NS GREEN  / EW RED     (AI-chosen duration)
Phase 1 → NS YELLOW / EW RED     (3 s fixed)
Phase 2 → EW GREEN  / NS RED     (AI-chosen duration)
Phase 3 → EW YELLOW / NS RED     (3 s fixed)
```

---

## Configuration

Edit `config.py` to tune any aspect of the system:

- `MIN_GREEN_TIME` / `MAX_GREEN_TIME` – clamp the agent's action range
- `VEHICLE_SPEED` – animation speed
- `SPAWN_INTERVAL` – how aggressively vehicles are spawned
- `ACTIONS` – the discrete green-time choices available to the agent
- `ALPHA`, `GAMMA`, `EPSILON_*` – Q-Learning hyper-parameters
- `DETECT_SENSITIVITY` – minimum blob area for vehicle detection (video mode)

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `ESC` | Quit and save Q-table |
| Window close | Quit and save Q-table |

---

## Performance Metrics (CSV columns)

| Column | Description |
|---|---|
| timestamp | HH:MM:SS |
| cycle | Completed full signal cycles |
| density_N/S/E/W | Vehicle count per lane |
| queue_N/S/E/W | Stopped vehicles per lane |
| wait_N/S/E/W | Rolling avg wait time (seconds) |
| cleared_total | Cumulative vehicles that exited |
| epsilon | Current exploration rate |
| avg_reward | Mean reward per agent step |

---

## Dependencies

| Package | Purpose |
|---|---|
| `pygame` | Simulation window, rendering, event loop |
| `opencv-python` | Video capture and vehicle detection |
| `numpy` | Q-table storage and numerical ops |
| `matplotlib` | (Optional) offline metric plotting |

---

## License
MIT – free to use and modify.
