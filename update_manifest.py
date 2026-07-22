#!/usr/bin/env python3
"""
Back-compat entry point. The canonical manifest generator now lives at
scripts/generate_manifest.py (the same script CI runs). This shim just
delegates so `python3 update_manifest.py` keeps working.
"""

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).parent / "scripts" / "generate_manifest.py"),
        run_name="__main__",
    )
