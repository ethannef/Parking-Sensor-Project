"""
YOLO11 Zone Calibration
-------------------------
Pick an object class to detect, place two instances of it in the camera's
view, and this script will find both, pad their bounding boxes, and save
the resulting zones to zones.json for use by run.py.

Usage:
    python calibrate.py
"""

from ultralytics import YOLO
import cv2
import json
import time

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

MODEL_PATH = "yolo11n_ncnn_model"   # use "yolo11n.pt" if not exported to NCNN yet
CAMERA_SOURCE = 0
CONFIDENCE_THRESHOLD = 0.5
OUTPUT_FILE = "zones.json"
SNAPSHOT_FILE = "calibration_snapshot.jpg"
PADDING = 15                         # pixels added around each box for jitter tolerance
CAPTURE_DELAY = 3                    # seconds to wait before capturing, gives you time to step back


def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")


# ---------------------------------------------------------------------------
# STEP 1 — LOAD MODEL
# ---------------------------------------------------------------------------

log("Loading YOLO11 model...")
model = YOLO(MODEL_PATH)
log(f"Model loaded: {MODEL_PATH}")

class_names = model.names  # dict: {id: name}

# ---------------------------------------------------------------------------
# STEP 2 — OBJECT SELECTION
# ---------------------------------------------------------------------------

print("\nAvailable classes:")
for class_id, name in class_names.items():
    print(f"  [{class_id}] {name}")

target_class_id = None
target_class_name = None

while target_class_id is None:
    choice = input("\nEnter the object you want to detect (name or ID): ").strip().lower()

    # allow entry by name or by numeric ID
    if choice.isdigit() and int(choice) in class_names:
        target_class_id = int(choice)
        target_class_name = class_names[target_class_id]
    else:
        matches = [cid for cid, name in class_names.items() if name.lower() == choice]
        if matches:
            target_class_id = matches[0]
            target_class_name = class_names[target_class_id]
        else:
            print(f"'{choice}' is not a valid class. Please try again.")

log(f"Target object selected: '{target_class_name}' (class ID {target_class_id})")

# ---------------------------------------------------------------------------
# STEP 3 — CAPTURE FRAME & RUN INFERENCE
# ---------------------------------------------------------------------------

log("Opening camera...")
cap = cv2.VideoCapture(CAMERA_SOURCE)
if not cap.isOpened():
    raise RuntimeError("Could not open camera. Check CAMERA_SOURCE.")

log(f"Place two '{target_class_name}' objects in view.")
log(f"Capturing in {CAPTURE_DELAY} seconds...")
time.sleep(CAPTURE_DELAY)

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Failed to capture frame from camera.")

h, w = frame.shape[:2]
log(f"Frame captured ({w}x{h}). Running inference...")

results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, classes=[target_class_id], verbose=False)

detections = []
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        detections.append({"coords": (x1, y1, x2, y2), "conf": conf})

log(f"Inference complete. Found {len(detections)} '{target_class_name}' detection(s).")

# ---------------------------------------------------------------------------
# STEP 4 — REQUIRE EXACTLY TWO (AUTO-PICK TOP 2 BY CONFIDENCE IF MORE)
# ---------------------------------------------------------------------------

if len(detections) < 2:
    log(f"ERROR: Need at least 2 detections, only found {len(detections)}.")
    log("Reposition your objects (check lighting/distance) and run calibrate.py again.")
    exit(1)

if len(detections) > 2:
    log("More than 2 detected — auto-selecting the 2 highest-confidence detections.")
    detections.sort(key=lambda d: d["conf"], reverse=True)
    detections = detections[:2]

for i, d in enumerate(detections):
    x1, y1, x2, y2 = d["coords"]
    log(f"  Using detection {i}: conf={d['conf']:.2f}, box=({int(x1)},{int(y1)})-({int(x2)},{int(y2)})")

# ---------------------------------------------------------------------------
# STEP 5 — PAD COORDINATES & BUILD ZONES
# ---------------------------------------------------------------------------

log(f"Padding boxes by {PADDING}px on each side...")

zones = {}
for i, d in enumerate(detections):
    x1, y1, x2, y2 = d["coords"]

    zx1 = max(0, int(x1) - PADDING)
    zy1 = max(0, int(y1) - PADDING)
    zx2 = min(w, int(x2) + PADDING)
    zy2 = min(h, int(y2) + PADDING)

    zone_name = f"{target_class_name}_{i + 1}"
    zones[zone_name] = {
        "coords": [zx1, zy1, zx2, zy2],
        "expected_class": target_class_name,
        "calibration_confidence": round(d["conf"], 3),
        "calibrated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    log(f"  Zone '{zone_name}' -> padded box=({zx1},{zy1})-({zx2},{zy2})")

# ---------------------------------------------------------------------------
# STEP 6 — SAVE TO JSON
# ---------------------------------------------------------------------------

with open(OUTPUT_FILE, "w") as f:
    json.dump(zones, f, indent=2)

log(f"Saved {len(zones)} zone(s) to {OUTPUT_FILE}")

# ---------------------------------------------------------------------------
# STEP 7 — SAVE ANNOTATED SNAPSHOT FOR VISUAL CONFIRMATION
# ---------------------------------------------------------------------------

for zone_name, data in zones.items():
    x1, y1, x2, y2 = data["coords"]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, zone_name, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imwrite(SNAPSHOT_FILE, frame)
log(f"Saved annotated snapshot to {SNAPSHOT_FILE}")
log("Calibration complete. Pull the snapshot to verify placement:")
log(f"  scp pi@<pi-ip>:<path-to-folder>/{SNAPSHOT_FILE} .")
