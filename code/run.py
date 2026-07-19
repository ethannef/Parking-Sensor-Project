"""
YOLO11 Entry/Exit Tally Monitor
---------------------------------
Loads two zones from zones.json (created by calibrate.py) and watches for
a chosen object class crossing them in sequence:

    Zone A covered, then Zone B covered within CROSSING_TIMEOUT  -> ENTRY (+1)
    Zone B covered, then Zone A covered within CROSSING_TIMEOUT  -> EXIT  (-1)

Zone A is automatically the left-most zone, Zone B the right-most, based on
their saved coordinates. If your physical setup means entries actually cross
B before A, flip REVERSE_DIRECTION to True below.

The terminal shows a live, in-place refreshing dashboard (like `watch`) with
current zone status, crossing progress, the tally, and recent events. Every
entry/exit is also permanently logged to tally_log.csv.

Usage:
    python run.py

Requires zones.json to exist (run calibrate.py first).
"""

from ultralytics import YOLO
from collections import deque
import cv2
import time
import csv
import json
import os
import sys

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

MODEL_PATH = "yolo11n_ncnn_model"   # use "yolo11n.pt" if not exported to NCNN yet
CAMERA_SOURCE = 0
CONFIDENCE_THRESHOLD = 0.5
ZONES_FILE = "zones.json"
LOG_FILE = "tally_log.csv"

COVERAGE_THRESHOLD = 0.5     # fraction of a zone's area that must be overlapped to count as "covered"
CONFIRM_FRAMES = 2           # consecutive frames required to confirm a zone covered/cleared (debounce)
CROSSING_TIMEOUT = 30        # seconds allowed between first zone covered and second zone covered
REFRESH_INTERVAL = 1.0       # seconds between dashboard redraws, like `watch -n 1`
EVENT_HISTORY = 8            # number of recent events shown on the dashboard
HEADLESS = True              # set False only if you have a display (VNC/X11) attached

REVERSE_DIRECTION = False    # flip to True if Zone B should be crossed first for an ENTRY

# ---------------------------------------------------------------------------
# ANSI HELPERS (for the live dashboard)
# ---------------------------------------------------------------------------

CLEAR_HOME = "\033[H\033[J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def log(msg):
    """Plain timestamped print, used only during one-time setup below."""
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# ---------------------------------------------------------------------------
# STEP 1 — LOAD ZONES
# ---------------------------------------------------------------------------

if not os.path.isfile(ZONES_FILE):
    raise RuntimeError(f"{ZONES_FILE} not found. Run calibrate.py first.")

with open(ZONES_FILE) as f:
    zones_config = json.load(f)

if len(zones_config) != 2:
    raise RuntimeError(f"Expected exactly 2 zones in {ZONES_FILE}, found {len(zones_config)}.")

sorted_zones = sorted(zones_config.items(), key=lambda kv: kv[1]["coords"][0])
(ZONE_A_NAME, zone_a_data), (ZONE_B_NAME, zone_b_data) = sorted_zones
ZONE_A = tuple(zone_a_data["coords"])
ZONE_B = tuple(zone_b_data["coords"])

log(f"Zone A (left):  '{ZONE_A_NAME}' -> {ZONE_A}")
log(f"Zone B (right): '{ZONE_B_NAME}' -> {ZONE_B}")
if REVERSE_DIRECTION:
    log("Direction: B -> A counts as ENTRY, A -> B counts as EXIT (reversed).")
else:
    log("Direction: A -> B counts as ENTRY, B -> A counts as EXIT.")

# ---------------------------------------------------------------------------
# STEP 2 — LOAD MODEL & PICK OBJECT CLASS TO WATCH
# ---------------------------------------------------------------------------

log("Loading YOLO11 model...")
model = YOLO(MODEL_PATH)
class_names = model.names
log("Model loaded.")

print("\nAvailable classes:")
for class_id, name in class_names.items():
    print(f"  [{class_id}] {name}")

target_class_id = None
target_class_name = None

while target_class_id is None:
    choice = input("\nEnter the object class to watch crossing the zones (name or ID): ").strip().lower()
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

log(f"Watching for '{target_class_name}' (class ID {target_class_id}) crossing the zones.")

# ---------------------------------------------------------------------------
# STEP 3 — SET MAX CAPACITY
# ---------------------------------------------------------------------------

MAX_CAPACITY = None
while MAX_CAPACITY is None:
    raw = input("Enter max capacity (max tally before lot is 'full'): ").strip()
    if raw.isdigit() and int(raw) > 0:
        MAX_CAPACITY = int(raw)
    else:
        print("Please enter a positive whole number.")

log(f"Max capacity set to {MAX_CAPACITY}.")

# ---------------------------------------------------------------------------
# STEP 4 — SETUP CAMERA & LOG FILE
# ---------------------------------------------------------------------------

cap = cv2.VideoCapture(CAMERA_SOURCE)
if not cap.isOpened():
    raise RuntimeError("Could not open camera. Check CAMERA_SOURCE.")

log_exists = os.path.isfile(LOG_FILE)
log_file = open(LOG_FILE, "a", newline="")
log_writer = csv.writer(log_file)
if not log_exists:
    log_writer.writerow(["timestamp", "event", "class_name", "tally", "max_capacity"])


def log_tally_event(event, tally_value):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    log_writer.writerow([ts, event, target_class_name, tally_value, MAX_CAPACITY])
    log_file.flush()


def box_overlap_fraction(box_xyxy, zone_coords):
    """Fraction of the ZONE's area that is covered by the given detection box."""
    bx1, by1, bx2, by2 = box_xyxy
    zx1, zy1, zx2, zy2 = zone_coords

    ix1, iy1 = max(bx1, zx1), max(by1, zy1)
    ix2, iy2 = min(bx2, zx2), min(by2, zy2)

    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0

    intersection = (ix2 - ix1) * (iy2 - iy1)
    zone_area = (zx2 - zx1) * (zy2 - zy1)
    if zone_area <= 0:
        return 0.0
    return intersection / zone_area


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------

recent_events = deque(maxlen=EVENT_HISTORY)


def add_event(msg):
    ts = time.strftime("%H:%M:%S")
    recent_events.appendleft(f"[{ts}] {msg}")


def capacity_bar(tally_value, max_value, width=24):
    filled = min(width, int(width * tally_value / max_value)) if max_value else 0
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def render_dashboard(tally_value, crossing_state, crossing_start_time):
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(f"{BOLD}Every {REFRESH_INTERVAL:.1f}s{RESET}  YOLO11 Tally Monitor  "
                 f"watching: {CYAN}{target_class_name}{RESET}  {now_str}")
    lines.append("-" * 62)

    a_covered = zone_a_state["covered"]
    b_covered = zone_b_state["covered"]
    a_color = YELLOW if a_covered else GREEN
    b_color = YELLOW if b_covered else GREEN
    a_text = "COVERED" if a_covered else "clear"
    b_text = "COVERED" if b_covered else "clear"

    lines.append(f"  Zone A ({ZONE_A_NAME}):  {a_color}{a_text:<8}{RESET}")
    lines.append(f"  Zone B ({ZONE_B_NAME}):  {b_color}{b_text:<8}{RESET}")
    lines.append("")

    if crossing_state == "NONE":
        lines.append("  Crossing status: idle")
    else:
        elapsed = time.time() - crossing_start_time
        remaining = max(0.0, CROSSING_TIMEOUT - elapsed)
        waiting_for = "Zone B" if crossing_state == "WAITING_FOR_B" else "Zone A"
        lines.append(f"  {YELLOW}Crossing in progress — waiting for {waiting_for} "
                     f"({remaining:.1f}s left){RESET}")

    lines.append("")
    bar = capacity_bar(tally_value, MAX_CAPACITY)
    full = tally_value >= MAX_CAPACITY
    status_color = RED if full else GREEN
    status_text = "FULL" if full else "NOT FULL"
    lines.append(f"  Tally: {tally_value}/{MAX_CAPACITY}  {bar}  {status_color}{BOLD}{status_text}{RESET}")

    lines.append("-" * 62)
    lines.append(f"{BOLD}Recent events:{RESET}")
    if recent_events:
        for e in recent_events:
            lines.append(f"  {e}")
    else:
        lines.append("  (none yet)")

    lines.append("-" * 62)
    lines.append("Ctrl+C to stop")

    sys.stdout.write(CLEAR_HOME)
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------

tally = 0

zone_a_state = {"covered": False, "present_count": 0, "absent_count": 0}
zone_b_state = {"covered": False, "present_count": 0, "absent_count": 0}

crossing_state = "NONE"   # NONE, WAITING_FOR_B, WAITING_FOR_A
crossing_start_time = None
last_render_time = 0.0

add_event("Monitoring started")

# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------

sys.stdout.write(HIDE_CURSOR)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            add_event("Camera read failed, stopping.")
            render_dashboard(tally, crossing_state, crossing_start_time)
            break

        results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, classes=[target_class_id], verbose=False)

        best_overlap_a = 0.0
        best_overlap_b = 0.0
        for r in results:
            for box in r.boxes:
                xyxy = box.xyxy[0].tolist()
                best_overlap_a = max(best_overlap_a, box_overlap_fraction(xyxy, ZONE_A))
                best_overlap_b = max(best_overlap_b, box_overlap_fraction(xyxy, ZONE_B))

        found_a = best_overlap_a >= COVERAGE_THRESHOLD
        found_b = best_overlap_b >= COVERAGE_THRESHOLD
        now = time.time()

        # ---- debounce zone A, detect rising edge ----
        if found_a:
            zone_a_state["present_count"] += 1
            zone_a_state["absent_count"] = 0
        else:
            zone_a_state["absent_count"] += 1
            zone_a_state["present_count"] = 0

        a_just_covered = False
        if not zone_a_state["covered"] and zone_a_state["present_count"] >= CONFIRM_FRAMES:
            zone_a_state["covered"] = True
            a_just_covered = True
        if zone_a_state["covered"] and zone_a_state["absent_count"] >= CONFIRM_FRAMES:
            zone_a_state["covered"] = False

        # ---- debounce zone B, detect rising edge ----
        if found_b:
            zone_b_state["present_count"] += 1
            zone_b_state["absent_count"] = 0
        else:
            zone_b_state["absent_count"] += 1
            zone_b_state["present_count"] = 0

        b_just_covered = False
        if not zone_b_state["covered"] and zone_b_state["present_count"] >= CONFIRM_FRAMES:
            zone_b_state["covered"] = True
            b_just_covered = True
        if zone_b_state["covered"] and zone_b_state["absent_count"] >= CONFIRM_FRAMES:
            zone_b_state["covered"] = False

        # ---- crossing state machine ----
        if crossing_state == "NONE":
            if a_just_covered:
                crossing_state = "WAITING_FOR_B"
                crossing_start_time = now
                add_event(f"Zone A covered by '{target_class_name}' — waiting for Zone B")
            elif b_just_covered:
                crossing_state = "WAITING_FOR_A"
                crossing_start_time = now
                add_event(f"Zone B covered by '{target_class_name}' — waiting for Zone A")

        elif crossing_state == "WAITING_FOR_B":
            if b_just_covered:
                event = "EXIT" if REVERSE_DIRECTION else "ENTRY"
                tally = min(MAX_CAPACITY, tally + 1) if event == "ENTRY" else max(0, tally - 1)
                add_event(f"{event} logged — tally now {tally}/{MAX_CAPACITY}")
                log_tally_event(event, tally)
                crossing_state = "NONE"
                crossing_start_time = None
            elif now - crossing_start_time > CROSSING_TIMEOUT:
                add_event("Crossing timed out waiting for Zone B — not logged")
                crossing_state = "NONE"
                crossing_start_time = None

        elif crossing_state == "WAITING_FOR_A":
            if a_just_covered:
                event = "ENTRY" if REVERSE_DIRECTION else "EXIT"
                tally = min(MAX_CAPACITY, tally + 1) if event == "ENTRY" else max(0, tally - 1)
                add_event(f"{event} logged — tally now {tally}/{MAX_CAPACITY}")
                log_tally_event(event, tally)
                crossing_state = "NONE"
                crossing_start_time = None
            elif now - crossing_start_time > CROSSING_TIMEOUT:
                add_event("Crossing timed out waiting for Zone A — not logged")
                crossing_state = "NONE"
                crossing_start_time = None

        # ---- redraw dashboard on its own cadence, like `watch -n` ----
        if now - last_render_time >= REFRESH_INTERVAL:
            render_dashboard(tally, crossing_state, crossing_start_time)
            last_render_time = now

        # ---- optional visualization window (only if HEADLESS is False) ----
        if not HEADLESS:
            color_a = (0, 255, 0) if zone_a_state["covered"] else (0, 0, 255)
            color_b = (0, 255, 0) if zone_b_state["covered"] else (0, 0, 255)
            cv2.rectangle(frame, (ZONE_A[0], ZONE_A[1]), (ZONE_A[2], ZONE_A[3]), color_a, 2)
            cv2.rectangle(frame, (ZONE_B[0], ZONE_B[1]), (ZONE_B[2], ZONE_B[3]), color_b, 2)
            cv2.putText(frame, "A", (ZONE_A[0], ZONE_A[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_a, 2)
            cv2.putText(frame, "B", (ZONE_B[0], ZONE_B[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_b, 2)
            cv2.putText(frame, f"Tally: {tally}/{MAX_CAPACITY}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("YOLO11 Tally Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except KeyboardInterrupt:
    add_event("Stopped by user (Ctrl+C)")
    render_dashboard(tally, crossing_state, crossing_start_time)

finally:
    sys.stdout.write(SHOW_CURSOR)
    cap.release()
    if not HEADLESS:
        cv2.destroyAllWindows()
    log_file.close()
    print(f"\nFinal tally: {tally}/{MAX_CAPACITY}")
