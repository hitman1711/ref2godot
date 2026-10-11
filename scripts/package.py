#!/usr/bin/env python3
"""Package editable Godot source as ZIP, excluding caches and local credentials."""
import argparse
import json
import os
from pathlib import Path
import sys
import zipfile

SKIP_DIRS = {".git", ".godot", ".agents", ".codex", "__pycache__", "node_modules", "work", "builds", ".venv", "venv"}
SKIP_FILES = {"export_credentials.cfg", ".DS_Store"}


def source_files(project):
    for directory, folders, files in os.walk(project, followlinks=False):
        for folder in folders:
            path = Path(directory) / folder
            if path.is_symlink() and folder not in SKIP_DIRS:
                raise ValueError("Resolve source symlink before packaging: " + str(path))
        folders[:] = sorted(folder for folder in folders if folder not in SKIP_DIRS and not folder.startswith("."))
        for name in sorted(files):
            if name in SKIP_FILES or name.startswith(".env") or name.endswith((".key", ".pem", ".pyc", ".log")):
                continue
            if name.startswith(".") and name not in {".gitignore", ".gdignore"}:
                continue
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError("Resolve source symlink before packaging: " + str(path))
            yield path


def package(project, output):
    project = Path(project).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if not (project / "project.godot").is_file():
        raise ValueError("Missing project.godot")
    if output == project or project in output.parents:
        raise ValueError("Write the ZIP outside the game project to avoid packaging the output itself")
    if output.suffix.lower() != ".zip":
        raise ValueError("Output must have a .zip extension")
    if output.exists():
        raise ValueError("Output already exists; choose a new path")
    files = list(source_files(project))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, Path(project.name) / path.relative_to(project))
    return {"source_zip": str(output), "files": len(files), "note": "Editable source archive; not a platform binary export"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.project, args.out), indent=2))
        return 0
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
