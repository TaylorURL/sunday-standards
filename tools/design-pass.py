#!/usr/bin/env python3
"""Runs the design gate tool that ships inside the skill.

The tool lives with the skill rather than beside it, so that wherever the skill
lands - a synced ~/.sunday/profile, an uploaded account skill, a cloud container that has
the skill and nothing else - the gates and the thing that runs them arrive
together. This is the local entry point the hooks in settings.json call; it holds
no logic of its own so the two cannot drift.
"""

import os
import sys
from pathlib import Path

CANDIDATES = [
    Path.home() / ".sunday/profile" / "skills" / "design-checklist" / "bin" / "design-pass.py",
    Path(__file__).resolve().parent.parent / "skills" / "design-checklist" / "bin" / "design-pass.py",
]


def main():
    for path in CANDIDATES:
        if path.is_file():
            os.execv(sys.executable, [sys.executable, str(path), *sys.argv[1:]])
    print("design-pass: the design skill is not installed - looked for %s"
          % " and ".join(str(p) for p in CANDIDATES), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
