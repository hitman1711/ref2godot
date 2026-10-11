# Godot tooling: MCP optional, native files always

## Capability selection

Inspect available tools and their schemas before calling them. Godot MCP implementations differ: some launch a subprocess and edit disk scenes; others require an editor plugin and manipulate the open project. Do not assume `create_scene`, screenshot, input simulation, tile painting, or live scene editing exists because a server is named Godot.

| Needed operation | With a suitable MCP capability | Without MCP |
| --- | --- | --- |
| Engine/project information | Query connected engine and active project | `godot.py doctor`, inspect `project.godot` |
| Create/edit a scene | Use supported operation and save | Edit `.tscn` or run a Godot authoring script |
| Paint/bake tiles/resources | Supported editor API, save resources | Offline Godot API script + `PackedScene`/`ResourceSaver` |
| Run/debug | Run, retrieve output, stop the owned session | `godot.py run` or bounded CLI run |
| View rendered output | Actual screenshot capability | `godot.py capture` with a display/renderer |
| Inspect editor tree/selection | Editor-connected inspection | Saved scene/resource state plus actual editor check |

After MCP mutations, save and inspect the scene on disk. Confirm the target project before editing. Serialize writes to a given scene; do not race a CLI file edit against an MCP editor save. Keep user edits if the editor has unsaved changes. For a tool failure, inspect what was saved before retrying or switching to file edits. A stopped/read-only MCP server is not a reason to abandon a usable CLI path.

No MCP server is required in `agents/openai.yaml`. Do not install one or change Codex/user MCP configuration merely to use this skill. If the user requests setup, use the actual server documentation and current host configuration mechanisms. One researched example is [bradypp/godot-mcp](https://github.com/bradypp/godot-mcp); it is a capability example, not a fixed API contract.

## CLI helper

Python 3.9+ standard library is enough for `scaffold.py`, `godot.py`, and `package.py`. The engine helper discovers `--godot`, then `GODOT_PATH` (a binary, command name, or macOS `.app`), then PATH commands `godot`/`godot4`, then common macOS bundles. It verifies the engine version and rejects Godot 3. The supplied templates require 4.3+; `doctor` accepts other Godot 4 projects without upgrading them.

```bash
python3 "<skill>/scripts/godot.py" doctor --godot "/Applications/Godot.app"
python3 "<skill>/scripts/godot.py" import "<project>"
python3 "<skill>/scripts/godot.py" check "<project>" --timeout 90
python3 "<skill>/scripts/godot.py" run "<project>" --scene res://levels/level_02.tscn
python3 "<skill>/scripts/godot.py" editor "<project>"
```

`run`/`editor` are foreground interactive processes intended for a terminal session; use the session handle to stop the process you started. Bounded checking/capture kills only its own subprocess on timeout. Logs go under project `qa/`. Godot itself still uses normal user-data/editor-settings directories, which may need execution permission in a restricted sandbox. A user-managed portable engine is another option; do not modify an installed application bundle to enable it. The helper does not auto-install dependencies, delete caches, edit export presets, or upgrade the project.

If no local engine is available but the connected MCP can run Godot, perform equivalent loading/runtime checks there and retain its logs. If neither can execute, create source and report the unverified checks. Do not count a static scan as engine validation.

## Version-sensitive API choices

Confirm `--version` and `--help`, and use official documentation matching that minor version. Keep render features compatible with the selected renderer: Compatibility does not provide every Forward+ effect. Do not import another skill's asserted version baseline or blanket prohibition without checking it. Native `.tscn` paths are valid Godot resources; UIDs are useful when actually assigned, not a prerequisite for authoring scenes.

Official reference: [CLI tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html).
