"""
Camera Screenshot -> Git Push
-------------------------------
Captures a single frame from the camera and pushes it to the 'screenshots'
branch of this repo, WITHOUT touching your current branch or working files.

How it works: a separate git worktree (a second checkout of just the
'screenshots' branch) is created alongside this repo the first time you run
this. Every run after that just drops the new image into that worktree,
commits, and pushes -- your main branch here is never checked out or
disturbed.

Usage:
    python screenshot.py
"""

import cv2
import subprocess
import time
import os

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CAMERA_SOURCE = 0
BRANCH_NAME = "screenshots"
SCREENSHOT_SUBDIR = "screenshots"   # folder inside the branch to keep images in
REMOTE_NAME = "origin"
PROJECT_FOLDER_NAME = "Parking-Sensor-Project"


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def run_git(*args, cwd=None, check=True):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def find_project_root(target_name):
    """Locate a directory named `target_name`. Checks, in order: the current
    directory itself, a direct subdirectory of it, then each parent
    directory going upward. Covers running the script from inside the
    project, from its parent, or from a sibling folder like 'code/'."""
    cwd = os.getcwd()

    if os.path.basename(cwd) == target_name:
        return cwd

    candidate = os.path.join(cwd, target_name)
    if os.path.isdir(candidate):
        return candidate

    path = cwd
    while True:
        if os.path.basename(path) == target_name:
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent

    raise RuntimeError(
        f"Could not find a directory named '{target_name}' at, below, or above {cwd}."
    )


# ---------------------------------------------------------------------------
# STEP 1 — CD INTO Parking-Sensor-Project/, THEN LOCATE REPO & SET UP WORKTREE
# ---------------------------------------------------------------------------

log(f"Locating '{PROJECT_FOLDER_NAME}' directory...")
project_root = find_project_root(PROJECT_FOLDER_NAME)
os.chdir(project_root)
log(f"Changed working directory to {project_root}")

log("Locating git repository...")
repo_root = run_git("rev-parse", "--show-toplevel")
log(f"Repo root: {repo_root}")

worktree_path = os.path.join(os.path.dirname(repo_root), "screenshots-worktree")

existing_worktrees = run_git("worktree", "list", cwd=repo_root)

if worktree_path not in existing_worktrees:
    log(f"No screenshots worktree found. Setting one up at {worktree_path}...")

    run_git("fetch", REMOTE_NAME, check=False)  # best effort, ok if no remote yet

    local_branches = run_git("branch", "--list", BRANCH_NAME, cwd=repo_root)
    remote_branches = run_git("ls-remote", "--heads", REMOTE_NAME, BRANCH_NAME, cwd=repo_root, check=False)

    if local_branches:
        log(f"Branch '{BRANCH_NAME}' already exists locally, attaching worktree to it...")
        run_git("worktree", "add", worktree_path, BRANCH_NAME, cwd=repo_root)
    elif remote_branches:
        log(f"Branch '{BRANCH_NAME}' exists on remote, checking it out into the worktree...")
        run_git("worktree", "add", worktree_path, "-b", BRANCH_NAME,
                 f"{REMOTE_NAME}/{BRANCH_NAME}", cwd=repo_root)
    else:
        log(f"Branch '{BRANCH_NAME}' doesn't exist yet, creating it fresh...")
        run_git("worktree", "add", "-b", BRANCH_NAME, worktree_path, cwd=repo_root)

    log("Worktree ready.")
else:
    log(f"Using existing screenshots worktree at {worktree_path}")

# ---------------------------------------------------------------------------
# STEP 2 — CAPTURE FRAME
# ---------------------------------------------------------------------------

log("Opening camera...")
cap = cv2.VideoCapture(CAMERA_SOURCE)
if not cap.isOpened():
    raise RuntimeError("Could not open camera. Check CAMERA_SOURCE.")

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Failed to capture frame from camera.")

screenshot_dir = os.path.join(worktree_path, SCREENSHOT_SUBDIR)
os.makedirs(screenshot_dir, exist_ok=True)

timestamp = time.strftime("%Y%m%d_%H%M%S")
filename = f"{timestamp}.jpg"
filepath = os.path.join(screenshot_dir, filename)

cv2.imwrite(filepath, frame)
log(f"Saved screenshot: {filepath}")

# ---------------------------------------------------------------------------
# STEP 3 — COMMIT & PUSH FROM THE WORKTREE
# ---------------------------------------------------------------------------

relative_path = os.path.join(SCREENSHOT_SUBDIR, filename)

log("Committing screenshot...")
run_git("add", relative_path, cwd=worktree_path)
run_git("commit", "-m", f"Screenshot {timestamp}", cwd=worktree_path)

log(f"Pushing to {REMOTE_NAME}/{BRANCH_NAME}...")
run_git("push", "-u", REMOTE_NAME, BRANCH_NAME, cwd=worktree_path)

log("Done. Your current branch and working files were not touched.")
