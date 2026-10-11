#!/usr/bin/env python3
"""Create a native editable Godot 4.3+ starter; never overwrite existing files."""
import argparse
import json
from pathlib import Path
import shutil
import sys

SKILL = Path(__file__).resolve().parent.parent


def scaffold(destination, genre, levels, name):
    destination = Path(destination).expanduser().resolve()
    if destination.exists() and any(p.name != ".git" for p in destination.iterdir()):
        raise ValueError("Destination must be empty (an empty Git repository is allowed); no files overwritten")
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SKILL / "LICENSE", destination / "LICENSE")
    for source in (SKILL / "assets" / "starter" / "common").rglob("*"):
        if source.is_file():
            target = destination / source.relative_to(SKILL / "assets" / "starter" / "common")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    genre_root = SKILL / "assets" / "starter" / genre
    for source in genre_root.rglob("*"):
        if source.is_file() and source.name != "level.tscn.in":
            target = destination / source.relative_to(genre_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    level_paths = [f"res://levels/level_{i:02d}.tscn" for i in range(1, levels + 1)]
    template = (genre_root / "level.tscn.in").read_text(encoding="utf-8")
    (destination / "levels").mkdir(exist_ok=True)
    for index, path in enumerate(level_paths):
        next_scene = level_paths[index + 1] if index + 1 < levels else ""
        # Generated once: static node positions in .tscn remain authoritative thereafter.
        scene = template.replace("__LEVEL_NAME__", f"Level{index + 1:02d}")
        scene = scene.replace("__TITLE__", f"Level {index + 1}").replace("__NEXT_SCENE__", next_scene)
        (destination / path.removeprefix("res://")).write_text(scene, encoding="utf-8")
    config = (destination / "project.godot").read_text(encoding="utf-8")
    config = config.replace('"__GAME_NAME__"', json.dumps(name, ensure_ascii=False))
    (destination / "project.godot").write_text(config, encoding="utf-8")
    inventory = {"schema_version": 1, "genre": genre, "minimum_godot": "4.3", "levels": level_paths,
                 "status": "starter placeholders; customize every level to the agreed plan"}
    (destination / "ref2godot.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    for folder in ["art/source", "art/prompts", "art/references", "art/requests", "assets/textures", "docs", "qa"]:
        (destination / folder).mkdir(parents=True, exist_ok=True)
    # Keep raw references/source/prompts out of Godot's importer and release export.
    (destination / "art/.gdignore").write_text("", encoding="utf-8")
    (destination / "qa/.gdignore").write_text("", encoding="utf-8")
    (destination / "docs/.gdignore").write_text("", encoding="utf-8")
    return {"project": str(destination), "genre": genre, "levels": level_paths,
            "main_scene": level_paths[0], "editing_guide": str(destination / "EDITING.md")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination")
    parser.add_argument("--genre", choices=["topdown", "platformer"], required=True)
    parser.add_argument("--levels", type=int, required=True, help="Agreed number of authored levels")
    parser.add_argument("--name", default="Reference Game")
    args = parser.parse_args()
    if args.levels < 1:
        parser.error("--levels must be at least 1")
    try:
        print(json.dumps(scaffold(args.destination, args.genre, args.levels, args.name), indent=2))
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
