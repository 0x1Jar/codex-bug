#!/usr/bin/env python3
"""Compatibility wrapper. Canonical implementation: modules/orchestrator/hunt.py"""

import os
import runpy
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(ROOT_DIR, "modules/orchestrator/hunt.py")

if not os.path.exists(TARGET):
    sys.stderr.write(f"Missing canonical script: {TARGET}\n")
    sys.exit(1)

runpy.run_path(TARGET, run_name="__main__")
