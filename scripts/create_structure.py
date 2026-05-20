#!/usr/bin/env python3
"""
create_structure.py
-------------------
One-time scaffold: creates the Apigee proxy bundle directory tree.

Run once when bootstrapping the project:
    python scripts/create_structure.py

Safe to re-run — existing directories are silently ignored.
All XML content is managed exclusively by generate_xml.py.
"""

import os
import sys

# ── Directory tree ────────────────────────────────────────────────────────────
DIRECTORIES = [
    "apiproxy",
    "apiproxy/policies",
    "apiproxy/proxies",
    "apiproxy/targets",
    "apiproxy/resources/jsc",
    "apiproxy/resources/py",
]


def create_directories(base_path: str = ".") -> None:
    print(f"==> Scaffolding directory tree under: {os.path.abspath(base_path)}")
    for directory in DIRECTORIES:
        full_path = os.path.join(base_path, directory)
        os.makedirs(full_path, exist_ok=True)
        print(f"[OK] {full_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    create_directories(base_path)
    print("==> Scaffold complete.")
    print("==> Next step: python scripts/generate_xml.py")


if __name__ == "__main__":
    main()
