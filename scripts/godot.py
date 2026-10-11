#!/usr/bin/env python3
"""Discover Godot and validate/run/capture native projects. Python stdlib only."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ERROR_LINE = re.compile(r"(?:^|\n)\s*(?:SCRIPT ERROR:|ERROR:|Parse Error:|Shader compilation failed)", re.I)
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def find_engine(explicit=None):
    candidates = [explicit or os.environ.get("GODOT_PATH")] if explicit or os.environ.get("GODOT_PATH") else [
        shutil.which("godot"), shutil.which("godot4"),
        "/Applications/Godot.app/Contents/MacOS/Godot",
        "/Applications/Godot_mono.app/Contents/MacOS/Godot",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if path.suffix.lower() == ".app":
            path = path / "Contents/MacOS/Godot"
        resolved = str(path) if path.is_file() else shutil.which(str(path))
        if resolved and os.access(resolved, os.X_OK):
            return str(Path(resolved).resolve())
    raise ValueError("Godot not found. Set GODOT_PATH or pass --godot with the executable path.")


def bounded(command, timeout, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        output = error.stdout or b""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return {"ok": False, "exit_code": None, "timed_out": True, "output": output}
    output = ANSI.sub("", result.stdout)
    return {"ok": result.returncode == 0 and not ERROR_LINE.search(output),
            "exit_code": result.returncode, "timed_out": False, "output": output}


def engine_info(path):
    result = bounded([path, "--version"], 10)
    version = result["output"].strip()
    match = re.search(r"^(\d+)\.(\d+)", version)
    if not result["ok"] or not match:
        raise ValueError("Cannot read Godot version: " + version)
    if int(match[1]) != 4:
        raise ValueError("ref2godot requires Godot 4; detected " + version)
    return {"binary": path, "version": version, "minor": int(match[2])}


def project_path(value):
    path = Path(value).expanduser().resolve()
    if not (path / "project.godot").is_file():
        raise ValueError("Missing project.godot in " + str(path))
    return path


def stage(engine, project, name, arguments, timeout):
    qa = project / "qa"
    qa.mkdir(exist_ok=True)
    command = [engine, "--path", str(project), "--log-file", str(qa / (name + ".engine.log"))] + arguments
    result = bounded(command, timeout, project)
    (qa / (name + ".log")).write_text(result["output"], encoding="utf-8")
    return {"stage": name, "log": str(qa / (name + ".log")), **result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["doctor", "import", "check", "run", "editor", "capture"]:
        command = sub.add_parser(name)
        command.add_argument("--godot", help="Engine binary, PATH command, or macOS .app")
        command.add_argument("--timeout", type=float, default=90, help="Per-stage timeout in seconds")
        if name != "doctor":
            command.add_argument("project")
        if name in {"check", "run", "capture"}:
            command.add_argument("--scene", help="A res:// scene; check otherwise uses the full level inventory")
        if name == "check":
            command.add_argument("--frames", type=int, default=12, help="Physics frames per level smoke test")
        if name == "capture":
            command.add_argument("--out", required=True)
            command.add_argument("--frames", type=int, default=90)
            command.add_argument("--actions", help="JSON replay events; see references/validation.md")
    args = parser.parse_args()
    if args.timeout <= 0 or getattr(args, "frames", 1) < 1:
        parser.error("timeout and frames must be positive")
    try:
        engine = find_engine(args.godot)
        info = engine_info(engine)
        if args.command == "doctor":
            print(json.dumps({"ok": True, **info}, indent=2))
            return 0
        project = project_path(args.project)
        inventory_path = project / "ref2godot.json"
        if inventory_path.is_file():
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            required = inventory.get("minimum_godot", "4.0")
            if not re.fullmatch(r"4\.\d+", required):
                raise ValueError("minimum_godot must be a 4.x minor version")
            if info["minor"] < int(required.split(".")[1]):
                raise ValueError(f"Project requires Godot {required}+; detected {info['version']}")
        if args.command in {"run", "editor"}:
            qa = project / "qa"
            qa.mkdir(exist_ok=True)
            command = [engine, "--path", str(project), "--log-file", str(qa / (args.command + ".engine.log"))]
            if args.command == "editor":
                command.append("--editor")
            elif args.scene:
                command.append(args.scene)
            return subprocess.call(command, cwd=project)
        results = [stage(engine, project, "import", ["--headless", "--editor", "--import"], args.timeout)]
        if results[0]["ok"] and args.command == "check":
            extra = ["--headless", "--script", str(HERE / "scene_check.gd"), "--", "--frames", str(args.frames)]
            if args.scene:
                extra += ["--scene", args.scene]
            result = stage(engine, project, "scene_check", extra, args.timeout)
            result["ok"] = bool(result["ok"] and re.search(r"^REF2GODOT_CHECK ", result["output"], re.M))
            results.append(result)
        if results[0]["ok"] and args.command == "capture":
            out = Path(args.out).expanduser().resolve()
            if out.suffix.lower() != ".png":
                raise ValueError("Capture output must have a .png extension")
            if out.exists():
                raise ValueError("Capture output already exists; choose a new path: " + str(out))
            out.parent.mkdir(parents=True, exist_ok=True)
            extra = ["--audio-driver", "Dummy", "--fixed-fps", "60", "--script",
                     str(HERE / "capture.gd"), "--", "--out", str(out), "--frames", str(args.frames)]
            if args.scene:
                extra += ["--scene", args.scene]
            if args.actions:
                extra += ["--actions", str(Path(args.actions).expanduser().resolve())]
            result = stage(engine, project, "capture", extra, args.timeout)
            result["ok"] = bool(result["ok"] and out.is_file() and out.stat().st_size > 0)
            results.append(result)
        ok = all(item["ok"] for item in results)
        report = {"ok": ok, "engine": info, "project": str(project), "results": results}
        (project / "qa" / (args.command + "_report.json")).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0 if ok else 1
    except (ValueError, OSError, TypeError, AttributeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
