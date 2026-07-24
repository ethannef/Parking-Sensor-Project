# Parking Sensor Project — Raspberry Pi Setup Guide

A YOLO11-based entry/exit tally system for the Raspberry Pi. Two zones are
calibrated using printed ArUco markers, then continuously monitored for a
chosen object class (car, person, etc.) crossing them in sequence — logging
entries/exits, driving a live terminal dashboard, and lighting up green/red
LEDs based on whether a max capacity has been reached.

---

## 1. Prepare the Raspberry Pi

Flash Raspberry Pi OS (64-bit) using Raspberry Pi Imager, boot it, connect
over SSH, then update the system:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

## 2. Install build tools and git

```bash
sudo apt install -y build-essential git
```

## 3. Clone the repository

```bash
git clone <YOUR_REPO_URL> Parking-Sensor-Project
cd Parking-Sensor-Project
git checkout main
```

## 4. Install system prerequisites

OpenCV and its dependencies need a few system packages beyond just Python:

```bash
sudo apt install -y python3-pip python3-venv libgl1 libglib2.0-0
```

## 5. Create and activate a virtual environment

```bash
python3 -m venv yolo-env
source yolo-env/bin/activate
```

Activate this environment (`source yolo-env/bin/activate`) every time you
open a new terminal to work on this project.

## 6. Install Ultralytics (YOLO11)

Raspberry Pi OS is configured by default to pull pre-built ARM wheels from
**piwheels** instead of compiling from source, which is much faster:

```bash
pip install ultralytics --extra-index-url https://www.piwheels.org/simple
```

### If this pulls in huge NVIDIA/CUDA packages or torch/torchvision mismatch errors

This can happen on newer Python versions where piwheels doesn't yet have a
matching build, causing pip to silently fall back to generic PyPI wheels
(which bundle unnecessary CUDA dependencies on some platforms). Fix it by
installing matched CPU-only builds directly:

```bash
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir
```

Verify before continuing:

```bash
python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"
```

Both should print clean version numbers with no errors.

## 7. Download the model weights and export the fast format

```bash
# auto-downloads yolo11n.pt (fast, used for continuous monitoring)
yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg'

# auto-downloads yolo11s.pt (more accurate, used only for one-time calibration)
yolo predict model=yolo11s.pt source='https://ultralytics.com/images/bus.jpg'

# export yolo11n to NCNN — the ARM-optimized format run.py uses for speed
yolo export model=yolo11n.pt format=ncnn
```

The export step creates a `yolo11n_ncnn_model/` folder. This is what
`run.py` loads by default for fast continuous inference.

## 8. Put everything in one working directory

The scripts, the model files/exports, `zones.json`, and the log CSVs all
use relative paths and expect to live side by side. Copy everything from
the repo's `code/` folder into the same directory as `yolo-env` and the
exported model:

```bash
cp code/*.py ~/Parking-Sensor-Project/
```

Your working directory should end up containing, at minimum:
`calibrate.py`, `run.py`, `screenshot.py`, `yolo11n_ncnn_model/`,
`yolo11n.pt`, `yolo11s.pt`, and the `yolo-env/` folder.

## 9. Print the calibration markers

`marker_0.png` and `marker_1.png` (included in the repo) are ArUco markers
used to mark your two zones — print both on regular paper. Keep the white
border around each marker; it improves detection reliability.

---

## 10. What each script does, and the order to run them

### `calibrate.py` — run this first

Detects your two printed markers and saves their positions to `zones.json`.
No YOLO model is used here at all — marker detection is built directly
into OpenCV, so this step is fast and doesn't depend on lighting/object
recognition the way the old object-based calibration did.

1. Place `marker_0.png` and `marker_1.png` where you want your two zones
2. Run `python calibrate.py`
3. It retries across a few frames automatically if a marker isn't caught
   on the first attempt, pads each marker's box slightly for jitter
   tolerance, and writes `zones.json` plus an annotated snapshot image you
   can pull off the Pi to visually confirm placement

### `run.py` — the main monitoring loop

Loads `zones.json`, asks which object class to watch (any of the 80 COCO
classes) and your max capacity, then continuously watches both zones.

- Crops each frame down to just the two calibrated zones and runs
  detection on those crops only (not the full frame)
- Automatically pads each crop based on the chosen object's typical
  real-world size (a car gets a much bigger crop margin than a bottle)
- Zone A covered → then Zone B covered = **ENTRY** (tally +1)
- Zone B covered → then Zone A covered = **EXIT** (tally −1)
- A live, in-place refreshing dashboard (like `watch`) shows zone status,
  crossing progress, and the running tally
- Green/red LEDs on GPIO17/GPIO27 reflect NOT FULL / FULL status
- Every entry/exit is permanently logged to `tally_log.csv`

### `screenshot.py` — optional utility, run any time

Captures a single frame and pushes it to a dedicated `screenshots` branch
of the repo, using a separate git worktree so your main working directory
and branch are never touched or disturbed.

### Run order

```bash
python calibrate.py   # once, after placing/repositioning markers
python run.py          # the main monitoring session
python screenshot.py   # optional, any time you want a logged snapshot
```

---

## 11. Known issues / current limitations

**Crossings can take a few seconds to register.** Two things stack up:
`run.py` runs two separate inference calls per frame (one per zone crop),
and each detection requires 2 consecutive confirming frames
(`CONFIRM_FRAMES`) before it counts, as a debounce against flicker.
Since each inference call takes real time on the Pi's CPU, needing two
consecutive successful calls means the object has to sit in the zone for
a few seconds before it registers. `DETECTION_IMGSZ` in `run.py` has been
lowered to reduce this, but it isn't fully solved — a bigger fix (running
camera capture on a separate thread from inference, so frames aren't
dropped while a slow prediction is running) would help further with both
the delay and with catching fast-moving objects that pass through a zone
too quickly to be sampled.

**Detection struggles in low light.** Dim, low-contrast scenes reduce the
model's confidence, especially for smaller/thinner objects. `yolo11s.pt`
(used for calibration) is noticeably more accurate than `yolo11n.pt` in
these conditions but also slower — worth keeping in mind if you swap
`run.py` to a bigger model for reliability over speed. Improving physical
lighting on the zones is the most effective fix.

---

## Quick reference — full command cheat sheet

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y build-essential git python3-pip python3-venv libgl1 libglib2.0-0

git clone <YOUR_REPO_URL> Parking-Sensor-Project
cd Parking-Sensor-Project

python3 -m venv yolo-env
source yolo-env/bin/activate

pip install ultralytics --extra-index-url https://www.piwheels.org/simple

yolo predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg'
yolo predict model=yolo11s.pt source='https://ultralytics.com/images/bus.jpg'
yolo export model=yolo11n.pt format=ncnn

cp code/*.py .

python calibrate.py
python run.py
```