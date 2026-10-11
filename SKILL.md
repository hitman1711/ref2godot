---
name: ref2godot
description: Create or refine a reference-driven 2D Godot game from screenshots, concept art, gameplay video, or a style reference. Deliver a native Godot project with every level saved as an editable .tscn scene, consistent art, gameplay, and verified scene loading. Works with optional Godot MCP tools or the Godot CLI. Use for Godot games and Godot asset-to-scene workflows; not for browser-engine prototypes or 3D asset generation.
---

# ref2godot

Turn a visual reference into a playable **native Godot 4 project**. Every requested level must open in the Godot editor with its authored layout visible and editable. Adapt the reference-to-art-to-play workflow of ref2game; implement gameplay, animation, rendering, and delivery in Godot from the start.

## Non-negotiable output contract

- Save **every authored level** as a distinct `.tscn`, including tutorial, boss, puzzle, and alternate rooms in the agreed scope. Keep a level inventory in `ref2godot.json`; finish all agreed levels, not only the first polished screen.
- Save terrain, tile cells, collision, prop placement, actor instances, spawn markers, objectives, triggers, lights, and navigation as scene content/resources. A `.tscn` containing only a script that reconstructs the level at runtime does not satisfy this contract.
- Reuse `.tscn` scenes for actors, props, interactables, and UI. Expose meaningful tuning with `@export`, exported Resources, or scene overrides. Level layout must remain editable without editing GDScript or a hidden JSON map.
- Runtime spawning is appropriate for projectiles, particles, temporary enemies, and other gameplay events. Persist encounter/spawn configuration in the level. For procedural layouts, bake an editable scene (or saved chunks) before delivery; retain the generator as an optional authoring tool.
- Preserve user-authored scene edits. Never re-run a generator over edited levels as a normal startup/import step. If building scenes with `PackedScene.pack()`, set ownership for authored children and verify the saved scene by reopening it.

Read [scene authoring](references/scene-authoring.md) before creating or substantially changing levels.

## 1. Resolve the reference and scope

Inspect the reference. For video, inspect representative frames; use ffmpeg/contact sheets when available. Identify projection, composition, palette, scale, layers, likely interactions, and what the image cannot establish.

Ask one compact round only for decisions that materially affect the game: player actions, level count/progression, target platform, fidelity versus inspiration, or an ambiguous art choice. Use the session's input tool if available; keep independent work moving. Do not assume one level means a complete multi-level game. Record the agreed scope and completion criteria in `docs/PLAN.md`.

Inspect an existing project and its instructions before changing it. Detect the installed Godot version, renderer, language, main scene, plugins, and scene conventions. Keep the project's engine version; do not silently upgrade. The supplied starters use Godot **4.3+**, GDScript, and Compatibility rendering. For earlier versions adapt APIs explicitly. The workflow also applies to other 2D genres without forcing a supplied starter.

## 2. Select available tooling

Read [tooling](references/tooling.md). Prefer connected Godot MCP capabilities for editor inspection, play sessions, screenshots, and scene manipulation when useful. Discover actual tool schemas; names and capabilities vary between servers. MCP is **optional**, not an installation prerequisite. Save MCP changes to disk and verify the resulting files.

Without MCP, use file edits and Godot CLI. `<skill>` below is the absolute directory containing this file; `<project>` is the game directory, not the skill repository.

```bash
python3 "<skill>/scripts/godot.py" doctor
python3 "<skill>/scripts/scaffold.py" "<project>" --genre topdown --levels 3 --name "My Game"
python3 "<skill>/scripts/godot.py" check "<project>"
```

Choose `topdown` or `platformer` only when it matches the game. `--levels` is the **agreed count**. Scaffolding is for a new empty directory and refuses to overwrite an existing project. It creates playable placeholder scenes, progression, input settings, an editing guide, and an inventory; these are starting points to customize, not finished levels.

Use `--godot /absolute/path/to/binary` or `GODOT_PATH` if detection fails. With neither engine nor usable MCP, continue creating the native source and clearly mark engine validation blocked; do not claim a playable verified game. Do not replace the target with a web engine.

## 3. Build the playable scene structure

Read [gameplay and animation](references/gameplay-animation.md) for relevant systems. Establish the core interaction on placeholders and run it early. Save actual level layouts and reusable entity scenes, configure Input Map and collision layers, and make the levels launchable independently where practical (F6). Implement progression, restart, failure, and completion for the agreed game.

Give each level a purpose, readable route/objective, authored encounters, and an ending. Vary layouts and difficulty deliberately; do not deliver duplicate starter rooms with different names as completed levels. Use scene-local wiring and signals; add persistent managers only for state that must survive transitions.

For tile games, use paintable `TileMapLayer` nodes and a saved `TileSet` on supported versions. Do not hand-invent serialized tile data; let Godot write it. For freeform art, use placed sprite/prop instances with aligned collision. Use UI containers/anchors and a `CanvasLayer`; keep HUD text as real text.

## 4. Generate and integrate the art

Read [art pipeline](references/art-pipeline.md). Write a concise `art/style_bible.txt` and save prompts. Separate backgrounds, terrain, props, actor designs/parts, and UI art. Generate raster assets with the session's image-generation tool, using the reference and consistent style guidance. Use the available tool's current schema; do not assume a provider, API key, backend, or parallel-generation support. If generation is unavailable, keep building and identify remaining placeholder art.

If the user chooses native geometric/vector art or placeholders, author that style directly in Godot; raster generation is unnecessary. The optional `scripts/art.py` prepares imagegen arguments and imports returned local PNGs; it does not generate images. It preserves source art and records alpha bounds. Set display size, pivot, filtering, repeat, and collision explicitly in Godot. Attach textures and animations to the saved actor/prop scenes. Effects, lights, wind, camera response, and dynamic text belong in Godot.

Retain appropriate animation choices: sprite-frame animation, cutout rigs, procedural secondary motion, or a combination. A supplied art style does not require every creature to use the same rig. Animate actions with readable poses, contacts, and timing; whole-sprite bobbing alone is insufficient for a walking character.

## 5. Validate each level and the complete game

Read [validation](references/validation.md). Run engine import, load **all** scene resources, and execute every level in the inventory after scene/script changes. The bundled checker checks engine logs as well as exit codes; headless success does not establish visual quality or reachable objectives.

```bash
python3 "<skill>/scripts/godot.py" check "<project>"
python3 "<skill>/scripts/godot.py" capture "<project>" --scene res://levels/level_01.tscn --out "<project>/qa/level_01.png"
```

Use a rendered run/MCP screenshot to compare the assembled frame with the reference. Inspect at game display scale. Test movement, collision, interaction, loss/restart, and progression through every authored level, including the final result. Add focused regression checks for reproduced defects; the generic checker does not prove all game rules.

Perform the **editor round trip**: change one placed object's transform and one exported setting, save, reopen, and verify that running uses the changed values. Check scene ownership when generating/baking content. Document coverage and known gaps in `qa/REPORT.md`. If independent review is available and appropriate, use a scoped critic/reviewer; self-review remains a valid fallback.

## 6. Deliver the editable project

Read [delivery](references/delivery.md). Hand back `project.godot`, all level/entity/UI `.tscn` files, GDScript, resources, textures, source art/prompts, and a project-specific `EDITING.md` explaining how to edit, duplicate, run, and connect levels. Include the level inventory, exact tested engine version, controls, checks run, and remaining gaps.

Source delivery is required; a binary, PCK, or web export alone is insufficient. Create platform exports only when requested and after confirming matching export templates/presets. Never promise hot reload, export success, or MCP capabilities that were not verified.

## Supporting resources

- [Scene authoring](references/scene-authoring.md): ownership, editable levels, tiles, baking, and edit preservation.
- [Tooling](references/tooling.md): CLI/MCP capability selection and engine discovery.
- [Art pipeline](references/art-pipeline.md): reference study, image generation, import, and portable ref2game utilities.
- [Gameplay and animation](references/gameplay-animation.md): Godot systems, genre choices, rigs, effects, and feel.
- [Validation](references/validation.md): helper behavior, meaningful gameplay tests, screenshots, and editor round trip.
- [Delivery](references/delivery.md): editable handoff and exports.
- [Sources and design decisions](references/sources.md): researched upstream versions, attribution, official documentation, and rejected assumptions.
