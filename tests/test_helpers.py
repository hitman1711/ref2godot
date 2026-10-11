"""Offline helper behavior tests. Run: python3 -m unittest discover -s tests -v"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


scaffold = module("scaffold")
godot = module("godot")
art = module("art")
pack = module("package")


class Helpers(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ref2godot-tests-")
        self.base = Path(self.temporary.name)
        self.project = self.base / "game"
        scaffold.scaffold(self.project, "topdown", 3, 'Test "Scene"')

    def tearDown(self):
        self.temporary.cleanup()

    def test_existing_project_edits_are_not_overwritten(self):
        scene = self.project / "levels/level_02.tscn"
        scene.write_text(scene.read_text().replace("Vector2(120, 270)", "Vector2(150, 300)"))
        edited = scene.read_bytes()
        with self.assertRaises(ValueError):
            scaffold.scaffold(self.project, "platformer", 1, "Another Game")
        self.assertEqual(edited, scene.read_bytes())

    def test_all_levels_and_progression_are_persisted(self):
        inventory = json.loads((self.project / "ref2godot.json").read_text())
        self.assertEqual(3, len(inventory["levels"]))
        for index, path in enumerate(inventory["levels"]):
            text = (self.project / path.removeprefix("res://")).read_text()
            self.assertIn('[node name="Terrain"', text)
            self.assertIn('[node name="PlayerSpawn"', text)
            successor = inventory["levels"][index + 1] if index < 2 else ""
            self.assertIn('next_level = ' + json.dumps(successor), text)

    def test_package_has_editable_source_without_credentials_or_cache(self):
        (self.project / ".godot").mkdir()
        (self.project / ".godot/cache").write_text("cache")
        (self.project / "export_credentials.cfg").write_text("private")
        (self.project / ".env").write_text("private")
        archive = self.base / "game.zip"
        pack.package(self.project, archive)
        with zipfile.ZipFile(archive) as source:
            names = source.namelist()
            self.assertIn("game/levels/level_03.tscn", names)
            self.assertIn("game/project.godot", names)
            self.assertIn("game/art/.gdignore", names)
            self.assertFalse(any(".godot/" in n or "credentials" in n or n.endswith(".env") for n in names))
        with self.assertRaises(ValueError):
            pack.package(self.project, archive)
        with self.assertRaises(ValueError):
            pack.package(self.project, self.project / "inside.zip")

    def test_package_rejects_broken_source_symlink(self):
        (self.project / "missing.png").symlink_to(self.base / "not-present.png")
        with self.assertRaises(ValueError):
            pack.package(self.project, self.base / "broken.zip")

    def test_engine_errors_with_zero_exit_fail(self):
        result = godot.bounded([sys.executable, "-c", "print('\\x1b[31mSCRIPT ERROR: fixture\\x1b[0m')"], 5)
        self.assertEqual(0, result["exit_code"])
        self.assertFalse(result["ok"])

    def test_timeout_fails_and_terminates_owned_process(self):
        result = godot.bounded([sys.executable, "-c", "import time; time.sleep(5)"], 0.1)
        self.assertTrue(result["timed_out"])
        self.assertFalse(result["ok"])

    def test_prepare_preserves_reference_and_style_and_rejects_unsafe_name(self):
        (self.project / "art/style_bible.txt").write_text("Flat geometric shapes. Cool palette.")
        prompt = self.base / "hero.txt"
        prompt.write_text("One isolated hero with transparent background.")
        reference = self.base / "ref.png"
        reference.write_bytes(b"reference fixture")
        request = art.prepare(self.project, "hero", prompt, [reference], False, False)
        self.assertEqual([str(reference.resolve())], request["referenced_image_paths"])
        self.assertTrue(request["transparent_background"])
        self.assertIn("Flat geometric shapes.", request["prompt"])
        with self.assertRaises(ValueError):
            art.asset_name("../../outside")
        with self.assertRaises(ValueError):
            art.prepare(self.project, "hero", prompt, [reference], False, False)

    def test_png_import_preserves_source_and_rejects_wrong_alpha(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Optional Pillow is not installed")
        source = self.base / "sprite.png"
        image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        image.paste((50, 100, 200, 255), (8, 8, 24, 24))
        image.save(source)
        metadata = art.import_png(self.project, "hero", source, "required", False)
        self.assertEqual([8, 8, 24, 24], metadata["alpha_bbox"])
        self.assertEqual(hashlib.sha256(source.read_bytes()).digest(), hashlib.sha256((self.project / "assets/textures/hero.png").read_bytes()).digest())
        with self.assertRaises(ValueError):
            art.import_png(self.project, "hero", source, "required", False)
        with self.assertRaises(ValueError):
            art.import_png(self.project, "background", source, "opaque", False)


if __name__ == "__main__":
    unittest.main()
