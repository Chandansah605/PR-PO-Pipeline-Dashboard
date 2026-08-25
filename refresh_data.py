#!/usr/bin/env python3
"""
One-drop daily refresh for the PR/PO Pipeline Dashboard.

What it does (in plain language):
 1. Looks for the newest D365 PR / PO exports in THREE places:
      - the "Email-Drops" folder next to this repo (filled automatically by the
        Power Automate flow that saves Abdul's daily email attachments there)
      - your Downloads folder ("Purchase requisition*.xlsx" / "Purchase order*.xlsx")
      - the folder above this repo
    Files from Email-Drops are recognised by their COLUMNS (any filename works):
    a sheet with a 'Purchase requisition' column but no 'Purchase order' column
    is PR data; a sheet with a 'Purchase order' column is PO data.
 2. Copies the newest of each into this repo as pr.xlsx / po.xlsx.
 3. Regenerates pr_steps.json (when PR changes), journey_board.json, and the
    matching embedded fallback arrays in index.html.
 4. Commits and pushes, so GitHub Pages republishes the dashboard (~1 min).

Usage:
    python refresh_data.py            # full run (copy + regenerate + push)
    python refresh_data.py --no-push  # do everything except git commit/push
"""
import glob
import os
import shutil
import subprocess
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(REPO)
DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
EMAIL_DROPS = os.path.join(PARENT, "Email-Drops")
NO_PUSH = "--no-push" in sys.argv


def clear_git_locks():
    """Rename stale git lock files aside (index.lock, HEAD.lock, refs locks).

    On OneDrive-synced/sandboxed filesystems git sometimes cannot delete its own
    lock files, which then block the next git operation. Renaming is allowed even
    when deleting is not. Safe here because git() runs git synchronously - by the
    time we sweep, no git process started by this script is still running.
    """
    # On Windows git cleans up after itself, so an existing lock may belong to a
    # live GitHub Desktop operation - only clear clearly-abandoned ones there.
    min_age = 60 if os.name == "nt" else 0
    now = datetime.now().timestamp()
    for root, _dirs, fnames in os.walk(os.path.join(REPO, ".git")):
        if "stale-locks" in root:
            continue
        for fn in fnames:
            if fn.endswith(".lock"):
                lock = os.path.join(root, fn)
                try:
                    if now - os.path.getmtime(lock) >= min_age:
                        # Quarantine OUTSIDE refs/ etc. - a renamed file left inside
                        # .git/refs/ would be misread by git as a corrupt ref.
                        qdir = os.path.join(REPO, ".git", "stale-locks")
                        os.makedirs(qdir, exist_ok=True)
                        qname = (os.path.relpath(lock, os.path.join(REPO, ".git"))
                                 .replace(os.sep, "_")
                                 + ".stale." + datetime.now().strftime("%Y%m%d%H%M%S%f"))
                        os.rename(lock, os.path.join(qdir, qname))
                        print(f"  (cleared stale git lock: {fn})")
                except OSError:
                    pass


def git(args, **kw):
    """Run a git command in the repo, sweeping stale locks first."""
    clear_git_locks()
    return subprocess.run(["git"] + args, cwd=REPO, **kw)


def sheet_kind(path):
    """'pr', 'po', or None - decided by the header row, so filenames don't matter."""
    try:
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True).active
        hdr = set(next(ws.iter_rows(min_row=1, max_row=1, values_only=True)) or ())
    except Exception as e:
        print(f"  (couldn't read {os.path.basename(path)}: {e})")
        return None
    if "Purchase order" in hdr:
        return "po"
    if "Purchase requisition" in hdr:
        return "pr"
    return None


def candidates():
    """All potential source files: {'pr': [paths], 'po': [paths]}."""
    out = {"pr": [], "po": []}
    # 1) Email-Drops: any xlsx, classified by columns
    for f in glob.glob(os.path.join(EMAIL_DROPS, "*.xlsx")):
        k = sheet_kind(f)
        if k:
            out[k].append(f)
    # 2) Downloads + repo parent: matched by the D365 export filename
    for folder in (DOWNLOADS, PARENT):
        out["pr"] += glob.glob(os.path.join(folder, "Purchase requisition*.xlsx"))
        out["po"] += glob.glob(os.path.join(folder, "Purchase order*.xlsx"))
    return out


def main():
    print("== PR/PO Dashboard data refresh ==")
    # Sync with GitHub first: the cloud flow (Power Automate -> GitHub) may have
    # already pushed today's data. After a successful pull, freshly-updated repo
    # files are newer than the email drops, so this run becomes a clean no-op.
    if not NO_PUSH:
        try:
            p = git(["pull", "--rebase", "--autostash"], capture_output=True, text=True)
            print("  (synced with GitHub first)" if p.returncode == 0
                  else f"  (git pull skipped: {(p.stdout + p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else 'unknown'})")
        except FileNotFoundError:
            pass
    updated = []
    cand = candidates()

    for kind, target_name in (("pr", "pr.xlsx"), ("po", "po.xlsx")):
        files = cand[kind]
        target = os.path.join(REPO, target_name)
        if not files:
            print(f"  {target_name}: no new export found - skipped.")
            continue
        src = max(files, key=os.path.getmtime)
        src_time = os.path.getmtime(src)
        if os.path.exists(target) and src_time <= os.path.getmtime(target):
            print(f"  {target_name}: newest source ({os.path.basename(src)}) is not newer "
                  f"than the repo copy - already processed, skipped.")
            continue
        age_h = (datetime.now().timestamp() - src_time) / 3600
        if age_h > 24:
            print(f"  WARNING: {os.path.basename(src)} is {age_h:.0f}h old - using it anyway.")
        shutil.copy2(src, target)
        updated.append(target_name)
        print(f"  {target_name}  <-  {os.path.basename(src)} "
              f"(from {os.path.basename(os.path.dirname(src))}, "
              f"saved {datetime.fromtimestamp(src_time):%d %b %H:%M})")

    if not updated:
        print("Nothing new to process.")
        return 0

    if "pr.xlsx" in updated:
        print("Regenerating pr_steps.json from the fresh PR export...")
        r = subprocess.run([sys.executable, os.path.join(REPO, "gen_pr_steps.py"),
                            os.path.join(REPO, "pr.xlsx")], cwd=REPO)
        if r.returncode != 0:
            print("ERROR: gen_pr_steps.py failed - not pushing. Fix and rerun.")
            return 1

    print("Regenerating Journey Board data and embedded dashboard fallbacks...")
    r = subprocess.run([
        sys.executable,
        os.path.join(REPO, "gen_journey_board.py"),
        "--pr", os.path.join(REPO, "pr.xlsx"),
        "--po", os.path.join(REPO, "po.xlsx"),
        "--out", os.path.join(REPO, "journey_board.json"),
        "--sync-index", os.path.join(REPO, "index.html"),
    ], cwd=REPO)
    if r.returncode != 0:
        print("ERROR: gen_journey_board.py failed - not pushing. Fix and rerun.")
        return 1

    if NO_PUSH:
        print("Done (no-push mode). Commit the refreshed data and generated dashboard files in GitHub Desktop.")
        return 0

    print("Committing and pushing to GitHub...")
    files = updated + ["journey_board.json", "index.html"] + (["pr_steps.json"] if "pr.xlsx" in updated else [])
    try:
        git(["add"] + files, check=True)
        if git(["diff", "--cached", "--quiet"]).returncode == 0:
            print("  Data is identical to what's already published - no push needed.")
            return 0
        msg = f"Data refresh {datetime.now():%Y-%m-%d %H:%M}"
        c = git(["commit", "-m", msg], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"  git commit failed: {c.stdout}{c.stderr}")
            return 1
        git(["push"], check=True)
        print("Pushed. GitHub Pages will republish the dashboard in about a minute.")
    except FileNotFoundError:
        print("git command not found - files are updated in the repo folder.")
        print("Open GitHub Desktop and press Commit + Push (or install Git and rerun).")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"git step failed ({e}). Open GitHub Desktop and Commit + Push manually.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
