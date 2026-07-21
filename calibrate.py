"""
ArUco Marker Zone Calibration
--------------------------------
Print marker_0.png and marker_1.png, place them where you want your two
zones monitored, then run this script. It detects both markers by their
unique ID (no object-detection model needed at all — ArUco detection is
built into OpenCV), pads their bounding boxes slightly for jitter
tolerance, and saves the result to zones.json for use by run.py.

Usage:
    python calibrate.py
"""

import cv2
import json
import time

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CAMERA_SOURCE = 0
OUTPUT_FILE = "zones.json"
SNAPSHOT_FILE = "calibration_snapshot.jpg"
PADDING = 15                  # pixels added around each marker's box, for jitter tolerance
CAPTURE_DELAY = 3             # seconds to wait before the first capture attempt
MAX_ATTEMPTS = 6              # how many frames to try before giving up
ATTEMPT_DELAY = 1.5           # seconds between retry attempts
MARKER_IDS = [0, 1]           # the two marker IDs to look for (matches marker_0.png, marker_1.png)
ARUCO_DICT = cv2.aruco.DICT_4X4_50


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# ---------------------------------------------------------------------------
# STEP 1 — SET UP THE ARUCO DETECTOR
# ---------------------------------------------------------------------------

log("Setting up ArUco marker detector...")
aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
detector = cv2.aruco.ArucoDetector(aruco_dict)
log(f"Looking for marker IDs: {MARKER_IDS}")

# ---------------------------------------------------------------------------
# STEP 2 — CAPTURE & DETECT (WITH RETRIES)
# ---------------------------------------------------------------------------

log("Opening camera...")
cap = cv2.VideoCapture(CAMERA_SOURCE)
if not cap.isOpened():
    raise RuntimeError("Could not open camera. Check CAMERA_SOURCE.")

log("Place marker_0.png and marker_1.png in view.")
log(f"Capturing in {CAPTURE_DELAY} seconds...")
time.sleep(CAPTURE_DELAY)

best_frame = None
best_markers = {}   # marker_id -> 4x2 array of corner points

for attempt in range(1, MAX_ATTEMPTS + 1):
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to capture frame from camera.")

    log(f"Attempt {attempt}/{MAX_ATTEMPTS}: scanning for markers...")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    found = {}
    if ids is not None:
        for marker_corners, marker_id in zip(corners, ids.flatten()):
            if int(marker_id) in MARKER_IDS:
                found[int(marker_id)] = marker_corners[0]

    log(f"  Found marker(s): {sorted(found.keys()) if found else 'none'}")

    if len(found) > len(best_markers):
        best_frame = frame
        best_markers = found

    if len(found) == len(MARKER_IDS):
        log("  Both markers detected — stopping early.")
        break

    if attempt < MAX_ATTEMPTS:
        log(f"  Only {len(found)}/{len(MARKER_IDS)} found, retrying in {ATTEMPT_DELAY}s...")
        time.sleep(ATTEMPT_DELAY)

cap.release()

frame = best_frame
markers = best_markers
h, w = frame.shape[:2]

log(f"Best result: {len(markers)}/{len(MARKER_IDS)} marker(s) detected after {attempt} attempt(s).")

if len(markers) < len(MARKER_IDS):
    missing = [m for m in MARKER_IDS if m not in markers]
    log(f"ERROR: Missing marker ID(s) {missing}.")
    log("Make sure both markers are flat, well-lit, fully in frame, and not too small/far from the camera.")
    exit(1)

# ---------------------------------------------------------------------------
# STEP 3 — CONVERT MARKER CORNERS TO PADDED ZONE BOXES
# ---------------------------------------------------------------------------

log(f"Padding boxes by {PADDING}px on each side...")

zones = {}
for marker_id, marker_corners in markers.items():
    xs = marker_corners[:, 0]
    ys = marker_corners[:, 1]
    x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()

    zx1 = max(0, int(x1) - PADDING)
    zy1 = max(0, int(y1) - PADDING)
    zx2 = min(w, int(x2) + PADDING)
    zy2 = min(h, int(y2) + PADDING)

    zone_name = f"marker_{marker_id}"
    zones[zone_name] = {
        "coords": [zx1, zy1, zx2, zy2],
        "expected_class": zone_name,
        "marker_id": marker_id,
        "calibrated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    log(f"  Zone '{zone_name}' -> padded box=({zx1},{zy1})-({zx2},{zy2})")

# ---------------------------------------------------------------------------
# STEP 4 — SAVE TO JSON
# ---------------------------------------------------------------------------

with open(OUTPUT_FILE, "w") as f:
    json.dump(zones, f, indent=2)

log(f"Saved {len(zones)} zone(s) to {OUTPUT_FILE}")

# ---------------------------------------------------------------------------
# STEP 5 — SAVE ANNOTATED SNAPSHOT FOR VISUAL CONFIRMATION
# ---------------------------------------------------------------------------

for zone_name, data in zones.items():
    x1, y1, x2, y2 = data["coords"]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, zone_name, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imwrite(SNAPSHOT_FILE, frame)
log(f"Saved annotated snapshot to {SNAPSHOT_FILE}")
log("Calibration complete. Pull the snapshot to verify placement:")
log(f"  scp pi@<pi-ip>:<path-to-folder>/{SNAPSHOT_FILE} .")
