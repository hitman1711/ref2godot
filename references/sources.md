# Sources and design decisions

Researched 2026-10-11. Full integration runs on macOS passed with Godot **4.3.stable.official.77dcf97d8** and **4.7.2.stable.official.ed1daf0bf**. Starter API baseline: 4.3+; this does not claim every intermediate release or platform was tested. Stable documentation advances; match docs to the installed engine. See [validation evidence](../tests/VALIDATION.md).

## ref2game

[studioigor/ref2game](https://github.com/studioigor/ref2game), reviewed commit `61d8f9e5457b9b3a379fa016621efcf1904ce249`. Studied Codex entrypoint, generation, engine, art/animation, setup, QA, and delivery. Retained reference study, coherent art generation, playable iteration, visual comparison, and source handoff. Replaced JS/WebGL2, browser preview/Playwright, and static web packaging with native scenes/GDScript, engine checks, viewport capture, and editable source packaging. Upstream's Godot port is a separate later task; this skill authors native Godot directly.

Unmodified `study.py`, `compare.py`, `slice.py`, `sheet.py`, and `variantfix.py` from that commit are in `scripts/vendor/ref2game/`; `compare.py` depends on `study.py`. The MIT copyright/license is retained there. No browser engine or JS rig runtime is needed.

## GD-Agentic-Skills

[thedivergentai/gd-agentic-skills](https://github.com/thedivergentai/gd-agentic-skills), reviewed commit `6c110973e447b96bafb5f1e75663d2b08ce2de6c`. Studied builder, project foundations/templates, 2D animation, CharacterBody2D, and TileMap skills. Useful directions include scoped references, explicit ownership, native CLI validation, feature organization, typed tuning, and saved tile resources.

Research input only, not a dependency. Its root license at that commit is LGPL-3.0; no code/substantial instructional text from it is vendored. Native helpers/templates here are independently implemented. Do not load its entire skill graph or import asserted mandatory orchestration. Do not require UIDs instead of supported `.tscn` paths, force upgrades/universal rigs, or delete caches by default.

## Official Godot references

- [PackedScene](https://docs.godotengine.org/en/stable/classes/class_packedscene.html), [Node](https://docs.godotengine.org/en/stable/classes/class_node.html), [ResourceSaver](https://docs.godotengine.org/en/stable/classes/class_resourcesaver.html): ownership, lifecycle, saving/loading.
- [SceneTree](https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html): transitions.
- [CLI](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html): import, scripts, checks, export.
- [Exports](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html): Inspector properties.
- [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html), [TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html): editable tile content.
- [2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html), [CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html): native animation/effects.
- [Data paths](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html): normal user-data/editor-settings writes.

## MCP

[bradypp/godot-mcp](https://github.com/bradypp/godot-mcp) was reviewed as one example of information, native launch/debug, and scene-saving tools. No server code is included. Capabilities/schemas are discovered at runtime. No live Godot MCP was connected during validation; native CLI/files were exercised.
