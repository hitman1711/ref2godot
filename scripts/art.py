#!/usr/bin/env python3
"""Prepare current imagegen arguments or import a PNG; never calls a generator."""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys


def asset_name(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
        raise ValueError("Asset name must contain letters, digits, underscores, or hyphens only")
    return value


def prepare(project, name, prompt_path, refs, opaque, replace):
    bible = project / "art/style_bible.txt"
    if not bible.is_file() or not bible.read_text(encoding="utf-8").strip():
        raise ValueError("Write art/style_bible.txt from the reference before preparing images")
    if not refs:
        raise ValueError("Pass at least one --ref: first style reference, then optional design anchors")
    references = [Path(path).expanduser().resolve() for path in refs]
    if any(not path.is_file() for path in references):
        raise ValueError("Every referenced image must be an existing local file")
    prompt_file = Path(prompt_path).expanduser().resolve()
    prompt_text = prompt_file.read_text(encoding="utf-8").strip()
    if not prompt_text:
        raise ValueError("Asset prompt must not be empty")
    roles = "Image 1 sets style, palette, medium, and projection; composition is defined by ASSET."
    if len(references) > 1:
        roles += " Remaining images are design anchors: preserve their character/object identity and proportions."
    request = {"prompt": bible.read_text(encoding="utf-8").strip() + "\n\n" + roles + "\n\nASSET:\n" + prompt_text,
               "referenced_image_paths": [str(path) for path in references],
               "transparent_background": not opaque}
    target = project / "art/requests" / (name + ".json")
    if target.exists() and not replace:
        raise ValueError("Request exists; use --replace for an intentional revision")
    saved_prompt = project / "art/prompts" / (name + ".txt")
    if saved_prompt.resolve() != prompt_file:
        if saved_prompt.exists() and not replace:
            raise ValueError("Saved prompt exists; use --replace for an intentional revision")
    target.parent.mkdir(parents=True, exist_ok=True)
    saved_prompt.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if saved_prompt.resolve() != prompt_file:
        saved_prompt.write_text(prompt_text + "\n", encoding="utf-8")
    return request


def import_png(project, name, source, alpha, replace):
    try:
        from PIL import Image
    except ImportError as error:
        raise ValueError("PNG validation requires Pillow. Use a project-local environment; see art-pipeline.md.") from error
    source = Path(source).expanduser().resolve()
    with Image.open(source) as image:
        if image.format != "PNG":
            raise ValueError("Expected a PNG returned by image generation or supplied by the user")
        rgba = image.convert("RGBA")
        channel = rgba.getchannel("A")
        low, high = channel.getextrema()
        if high == 0:
            raise ValueError("Image is entirely transparent")
        if alpha == "required" and low == 255:
            raise ValueError("Expected transparency but the image is fully opaque")
        if alpha == "opaque" and low != 255:
            raise ValueError("Expected an opaque background/texture")
        metadata = {"size": list(image.size), "alpha_bbox": list(channel.getbbox()),
                    "alpha_range": [low, high], "source": f"art/source/{name}.png",
                    "texture": f"res://assets/textures/{name}.png"}
    targets = [project / metadata["source"], project / metadata["texture"].removeprefix("res://")]
    if not replace and any(path.exists() for path in targets):
        raise ValueError("Asset exists; use --replace for an intentional revision")
    manifest_path = project / "art/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    if not isinstance(manifest, dict):
        raise ValueError("art/manifest.json must be an object")
    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.resolve() != source:
            shutil.copy2(source, target)
    manifest[name] = metadata
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["prepare", "import"]:
        command = sub.add_parser(name)
        command.add_argument("project")
        command.add_argument("name")
        command.add_argument("source", help="Prompt text file (prepare) or returned PNG (import)")
        command.add_argument("--replace", action="store_true")
        if name == "prepare":
            command.add_argument("--ref", action="append", default=[])
            command.add_argument("--opaque", action="store_true", help="Opaque background/terrain texture")
        else:
            command.add_argument("--alpha", choices=["required", "optional", "opaque"], default="optional")
    args = parser.parse_args()
    try:
        project = Path(args.project).expanduser().resolve()
        if not (project / "project.godot").is_file():
            raise ValueError("Project must contain project.godot")
        name = asset_name(args.name)
        result = prepare(project, name, args.source, args.ref, args.opaque, args.replace) if args.command == "prepare" else import_png(project, name, args.source, args.alpha, args.replace)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
