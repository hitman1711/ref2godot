# ref2godot

A Codex skill for creating a reference-driven **2D Godot game** with every authored
level saved as an editable `.tscn`. A connected Godot MCP is optional; native CLI
and file tools provide a complete alternative.

[SKILL.md](SKILL.md) is the entrypoint. This repository root is the skill folder,
not a game project. Copy/place it as `ref2godot` in your Codex skill discovery
directory (such as `~/.codex/skills/ref2godot` or a game's
`.agents/skills/ref2godot`), then start a session that discovers it.

> Use $ref2godot with this reference to create a top-down game with three distinct
> levels. Save all levels as editable Godot scenes and include an editing guide.

Included: top-down/platformer placeholder starters, safe scaffolding, engine
checks, rendered capture/action replay, optional art preparation/import,
source packaging, and portable reference-analysis helpers from ref2game.

Python 3.9+ and Godot 4 are required for the CLI path; starters require 4.3+.
Generation uses the session's image tool. Pillow is optional for PNG import;
Pillow/NumPy/SciPy are optional for analysis. Node/Playwright/MCP are not required.

See [sources](references/sources.md) and [validation](tests/VALIDATION.md).
MIT licensed, with retained upstream MIT notices for vendored utilities.
