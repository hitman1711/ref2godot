#!/usr/bin/env python3
"""Integration checks against a real Godot editor binary, in an isolated workdir."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import godot
import scaffold
import package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot")
    parser.add_argument("--capture", action="store_true", help="Also exercise displayed rendering")
    args = parser.parse_args()
    engine = godot.find_engine(args.godot)
    info = godot.engine_info(engine)
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix="engine-tests-", dir=work))
    results = []

    def run(name, command, expected=True):
        result = godot.bounded(command, 60)
        if result["ok"] != expected:
            raise RuntimeError(name + " failed:\n" + result["output"])
        results.append({"name": name, "passed": True})
        print("PASS", name, flush=True)

    try:
        for genre in ["topdown", "platformer"]:
            project = base / genre
            scaffold.scaffold(project, genre, 2, "Ref2Godot " + genre)
            command = [sys.executable, str(ROOT / "scripts/godot.py")]
            run(genre + " import/load/all-level smoke", command + ["check", str(project), "--godot", engine])
            for phase in (["save", "verify", "gameplay"] if genre == "topdown" else ["gameplay"]):
                run(genre + " " + phase, [engine, "--headless", "--path", str(project), "--log-file", str(project / "qa" / (phase + ".engine.log")), "--script", str(ROOT / "tests/starter_checks.gd"), "--", "--phase", phase, "--genre", genre])
            if args.capture:
                run(genre + " rendered capture", command + ["capture", str(project), "--godot", engine, "--frames", "30", "--out", str(project / "qa/frame.png")])
                if genre == "topdown":
                    replay = project / "qa/replay.json"
                    replay.write_text(json.dumps([
                        {"frame": 0, "action": "move_right", "pressed": True},
                        {"frame": 20, "action": "move_right", "pressed": False},
                    ]))
                    moved = project / "qa/moved.png"
                    run("topdown action replay", command + ["capture", str(project), "--godot", engine, "--frames", "30", "--actions", str(replay), "--out", str(moved)])
                    if hashlib.sha256(moved.read_bytes()).digest() == hashlib.sha256((project / "qa/frame.png").read_bytes()).digest():
                        raise RuntimeError("Action replay did not change the rendered frame")
                    replay.write_text('[{"frame": -1, "action": "unknown_action", "pressed": true}]')
                    rejected = project / "qa/rejected.png"
                    run("invalid replay rejected", command + ["capture", str(project), "--godot", engine, "--actions", str(replay), "--out", str(rejected)], expected=False)
                    if rejected.exists():
                        raise RuntimeError("Invalid replay unexpectedly produced an image")
            archive = base / (genre + ".zip")
            package.package(project, archive)
            clean = base / (genre + "-unpacked")
            with zipfile.ZipFile(archive) as source:
                source.extractall(clean)
            run(genre + " packaged source reimport", command + ["check", str(clean / genre), "--godot", engine])
            # A broken second level must fail, even when the starting level still works.
            (project / "levels/level_02.tscn").write_text('[gd_scene format=3]\n[node name="Broken" type="NoSuchNodeType"]\n')
            run(genre + " broken second level detection", command + ["check", str(project), "--godot", engine], expected=False)
        report = {"ok": True, "engine": info, "workdir": str(base), "results": results}
        (base / "results.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        print("Evidence retained in " + str(base), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
