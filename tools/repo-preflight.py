#!/usr/bin/env python3
"""Refuse to build or land from a repo checkout when a sibling checkout is newer or dirty.

A machine can hold several clones of one repo. Work done in one is invisible to the others:
git reads clean, the remote shows nothing, and a build from the wrong clone silently ships
stale code over newer work. This scans the usual project roots for every checkout sharing
the target's origin, compares working-tree state and declared versions, and exits nonzero
when the target is not the place to build from.

Usage: repo-preflight.py [repo-dir]        (default: cwd)
Exit:  0 = clear to proceed; 1 = a sibling checkout is dirty or ahead — reconcile first.
"""

import os
import re
import subprocess
import sys

# Where a second clone of a repo would plausibly be sitting. Worktrees are
# deliberately absent: they live under ~/worktrees, outside these roots, precisely
# so this scan does not mistake one for a rival checkout. Adding that directory
# here would flag every open worktree as drift and block every landing.
ROOTS = [
    os.path.expanduser("~/IdeaProjects"),
    os.path.expanduser("~/WebstormProjects"),
    os.path.expanduser("~/Projects"),
]


def git(cwd, *args):
    try:
        out = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=30)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def origin_of(path):
    url = git(path, "remote", "get-url", "origin")
    return url.rstrip("/").removesuffix(".git") if url else None


def version_of(path):
    for probe, pattern in (("gradle.properties", r"^version=(.+)$"),
                          ("package.json", r'"version"\s*:\s*"([^"]+)"')):
        f = os.path.join(path, probe)
        if os.path.isfile(f):
            m = re.search(pattern, open(f).read(), re.M)
            if m:
                return m.group(1).strip()
    return None


def version_tuple(v):
    # Every digit run in order, so 2026.32.48 and 1.4.2 both compare sensibly
    # without knowing which scheme a repo uses. A pre-release suffix contributes
    # its own digits, which makes 1.2.3-rc1 sort above 1.2.3 — wrong in theory,
    # harmless here, because this only ever compares two checkouts of one repo
    # and the answer it drives is "reconcile first".
    return tuple(int(x) for x in re.findall(r"\d+", v or "0")) or (0,)


def dirty_count(path):
    out = git(path, "status", "--porcelain")
    return len([l for l in (out or "").splitlines() if l.strip()])


def describe(path):
    return {
        "path": path,
        "branch": git(path, "branch", "--show-current") or "(detached)",
        "dirty": dirty_count(path),
        "version": version_of(path),
        "head": (git(path, "rev-parse", "--short", "HEAD") or "?"),
    }


def find_checkouts(target_origin, target_real):
    found = []
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if not os.path.isdir(os.path.join(path, ".git")):
                continue
            if origin_of(path) == target_origin and os.path.realpath(path) != target_real:
                found.append(path)
    return found


def main():
    target = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
    origin = origin_of(target)
    if not origin:
        print(f"repo-preflight: {target} is not a git checkout with an origin remote")
        return 1

    me = describe(target)
    siblings = [describe(p) for p in find_checkouts(origin, target)]

    print(f"repo-preflight: {origin}")
    for c in [me] + siblings:
        tag = "TARGET " if c["path"] == target else "sibling"
        print(f"  {tag} {c['path']}")
        print(f"          branch {c['branch']} @ {c['head']}, version {c['version']}, "
              f"{c['dirty']} dirty file(s)")

    problems = []
    for c in siblings:
        if c["dirty"] > 0:
            problems.append(f"{c['path']} has {c['dirty']} uncommitted file(s) — that work is "
                            "invisible from here and a build would ship without it")
        if version_tuple(c["version"]) > version_tuple(me["version"]):
            problems.append(f"{c['path']} declares version {c['version']} > {me['version']} — "
                            "the target checkout is stale")

    if problems:
        print("\nBLOCKED — reconcile before building or landing from this checkout:")
        for p in problems:
            print(f"  - {p}")
        return 1

    if me["dirty"] > 0:
        print(f"\nnote: the target tree itself has {me['dirty']} uncommitted file(s); "
              "the build will carry them.")
    print("clear to proceed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
