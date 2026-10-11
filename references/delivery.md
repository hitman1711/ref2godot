# Editable delivery

Deliver `project.godot`, every scoped level and reusable entity/UI `.tscn`, GDScript, Resources/animations/TileSets, shaders, runtime textures/audio/fonts, source art/prompts/style notes, and asset provenance. Include the level inventory, completed plan, project-specific `EDITING.md`, and `qa/REPORT.md` with exact tested version and known gaps.

The editing guide explains opening/running, controls, placed-node changes, collision/tile editing, shared actors versus instance overrides, and duplicating/connecting levels. Preserve generated `.gd.uid` and import sidecars where applicable. Exclude cache/build/VCS internals and export credentials. Carry the actual licenses of redistributed assets/code.

```bash
python3 "<skill>/scripts/package.py" "<project>" --out "/path/outside-project/game-source.zip"
```

This creates an editable source ZIP, not an engine export. It excludes common local credentials/configuration, caches, build directories, and logs. It refuses unresolved source symlinks instead of silently shipping broken assets. Inspect custom project content; exclusions cannot identify every secret. Output must be outside the game directory and absent. Unzip to a clean directory and verify import/loading when packaging is part of delivery.

For requested platform builds, configure the actual preset, verify matching export templates, create the output directory, and use the engine's export capability. Keep source alongside it. A requested web build is a Godot export of the native project. Missing export templates block that build specifically, not editable source delivery.

Hand back project path, controls, all level paths, editing guide, checks performed, and gaps. Do not promise browser hot reload, untested export success, or later messages after the turn ends.
