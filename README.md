# ref2godot

**Turn a visual reference into a playable 2D Godot game—with every level saved as an editable scene.**

Attach a screenshot, concept image, or gameplay video, describe the game you want,
and invoke `$ref2godot` in Codex. The skill guides the agent through reference
study, gameplay, art, animation, level authoring, testing, and source delivery.
You receive a native Godot project that you can open, play, and continue editing.

Inspired by [ref2game](https://github.com/studioigor/ref2game), with Godot scenes,
GDScript, native rendering, and an editable source handoff. A connected Godot MCP
can help with editor operations; the file-and-CLI workflow also works on its own.

[Install](#install) · [First game](#create-your-first-game) · [Workflow](#the-workflow) · [Editable levels](#what-editable-levels-means) · [Renderers and platforms](#renderers-and-target-platforms) · [Tools](#bundled-tools) · [Validation](#validation)

## What you get

- **Every agreed level:** distinct `.tscn` files with authored terrain, collision,
  props, actors, spawns, and objectives visible in the editor.
- **Reusable game objects:** entity and UI scenes, with useful settings exposed
  in the Inspector rather than buried in coordinate lists.
- **A complete gameplay loop:** the planned controls, interactions, progression,
  restart/failure behavior, and final result, tested across the agreed levels.
- **Art integrated into Godot:** supplied or generated textures, native animation
  and effects, source art, prompts, and style notes. Intentional geometric art
  can be authored directly in Godot.
- **An editable handoff:** `project.godot`, scripts, resources, an editing guide,
  a level inventory, and a report of what was actually tested.

These are the skill's delivery requirements. The bundled scaffold is an early
playable starting point: its repeated rooms and polygon placeholders still need
to be turned into the distinct levels and art requested by the user.

## Install

### Ask Codex to install it

```text
$skill-installer Install ref2godot from https://github.com/hitman1711/ref2godot.
The skill is at the repository root, where SKILL.md lives.
```

For an existing local checkout, ask Codex to install from that checkout instead.
This repository contains one Codex skill at its root; there is no separate
`codex/` edition to select.

### Install manually

For use across your projects, clone the repository into your personal skills
directory. These shell commands assume Git and a POSIX shell:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/hitman1711/ref2godot.git "$HOME/.agents/skills/ref2godot"
```

For one game repository, place the complete skill folder at
`<game-repository>/.agents/skills/ref2godot/` instead. Keep `SKILL.md`, `agents/`,
`references/`, `scripts/`, `assets/`, and `LICENSE` together: the scripts resolve the
templates relative to the skill folder.

Codex supports both personal and repository skill locations. If the installed
skill does not appear, restart Codex and check its skill selector. See the
[official skill documentation](https://learn.chatgpt.com/docs/build-skills)
for discovery and invocation details.

**The skill directory and the generated game directory are different folders.**
The repository root contains the agent's instructions and tools. Open the
generated game's `project.godot` in Godot.

## Create your first game

Open a Codex chat in the folder where you want to create the game, attach your
reference, and send something like:

```text
Use $ref2godot with the attached reference to create a desktop top-down game.
Make three distinct levels: learn the controls, introduce enemies, then a final
challenge. Use WASD movement and keep the reference's palette and perspective.
Save every level as an editable .tscn, expose player tuning in the Inspector,
and include instructions for editing and adding levels.
```

A useful prompt specifies the player's actions, level count, target platform,
and whether the reference should set the composition, art style, or both.
The agent asks about material gaps and records the agreed scope before building.
It inspects existing projects and their conventions when you ask for an extension.

Other requests you can make:

- **Platformer:** “Use `$ref2godot` to turn this concept art into a two-level
  platformer with jump buffering, checkpoints, and a final goal.”
- **Supplied assets:** “Use `$ref2godot` with these sprites and this layout
  reference. Build four editable puzzle rooms; use the supplied art.”
- **Geometric prototype:** “Use `$ref2godot` for two top-down levels using native
  geometric shapes. Focus on movement, collision, objectives, and progression.”
- **Existing project:** “Use `$ref2godot` to add an editable level to this game.
  Keep the current engine version and scene conventions, and preserve my edits.”
- **Feedback:** “The second level's exit is unreachable. Fix the route, test it
  using normal controls, and add a regression check.”
- **Handoff:** “Package the editable source and explain how I can duplicate and
  connect another level.”

## The workflow

| Phase | What the agent does | What you can review |
| --- | --- | --- |
| Reference and scope | Studies composition, palette, scale, layers, and interactions; agrees on controls, level count, and platform | The game plan and interpretation of your reference |
| Playable structure | Builds saved levels, reusable objects, input, collision, objectives, and progression on placeholders | An early game you can run in Godot |
| Art and motion | Integrates supplied/generated assets, chooses suitable native animation, and adds effects and feedback | Actual rendered frames and gameplay |
| All levels | Gives each agreed level a distinct layout, purpose, route, and ending | The full progression, including the final level |
| Validation and feedback | Checks engine loading, exercises gameplay, inspects captures, and verifies that saved edits survive reopening | Test evidence and fixes for reported defects |
| Delivery | Hands back editable source, source art/prompts, level inventory, editing guide, and QA report | A project you can maintain yourself |

The agent uses the session's image-generation capability when raster generation
is needed. `art.py` prepares requests and imports returned PNGs; it does not
generate images itself. If generation is unavailable, remaining placeholder art
must be identified. Native geometric/vector art does not require image generation.

Animation follows the art and mechanics: sprite frames, cutout rigs, procedural
secondary motion, or a combination. Effects and dynamic text use Godot systems.
There is no requirement to give every actor the same rig or to reproduce a
browser animation runtime.

## What editable levels means

Open a level scene and you should see the authored layout **before pressing Play**.
Move a pickup, adjust collision, change a spawn marker, or override player speed
in the Inspector; save and reopen the scene, and the game should use those edits.

Level content lives in saved nodes, scene instances, and resources. The skill
does not accept a nearly empty `.tscn` whose script rebuilds the whole layout on
startup. `ref2godot.json` lists levels for validation; it is not a hidden map format.
Procedural authoring must leave editable baked scenes/chunks or room templates,
with generated content clearly explained.

A typical delivered project contains:

```text
my-game/
├── project.godot
├── levels/
│   ├── level_01.tscn
│   ├── level_02.tscn
│   └── level_03.tscn
├── entities/                 # Reusable player, props, enemies, interactions
├── ui/                       # Saved UI scenes and scripts
├── assets/                   # Runtime textures and other game assets
├── art/                      # Source art, prompts, references, style notes
├── docs/PLAN.md
├── ref2godot.json             # Inventory of every scoped level
├── EDITING.md                # Project-specific editing and progression guide
└── qa/REPORT.md              # Tested version, checks, and remaining gaps
```

The supplied starters support F5 for the game and F6 for an individual level.
Their controls are WASD/arrows, Space to jump in the platformer, and R to restart.
Collect the diamonds, then enter the green exit. Player, pickups, exit, and HUD
are reusable saved scenes. The [starter editing guide](assets/starter/common/EDITING.md)
explains moving objects, changing shared scenes versus instance overrides, and
adding a level to progression and the inventory.

After initial authoring, saved scene content is the source of truth. Scaffolding
refuses to overwrite an existing project; later work must preserve your changes.

## Renderers and target platforms

The supplied starters use **Godot 4.3+, GDScript, and Compatibility rendering**.
The skill reads the renderer of an existing project and requires effects to work
with the selected renderer. It has no automatic renderer-selection policy.

| Renderer | Current behavior |
| --- | --- |
| Compatibility | Explicit default in both starters, including their mobile renderer override |
| Mobile | Can be used when selected for the project; no bundled Mobile-specific starter |
| Forward+ | Can be used when selected for the project; no bundled Forward+-specific starter |

**The renderer named Mobile and a mobile game target are separate choices.**
The starter's `rendering_method.mobile="gl_compatibility"` sets its renderer on
mobile; it does not add touch controls or configure a phone build.

The agent asks about the target platform as part of scope. The starters currently
favor desktop: keyboard input and a 960×540 landscape viewport. There is no
dedicated mobile workflow for touch controls, orientation, safe areas, or device
testing. State those requirements when requesting a mobile game; they require
additional implementation and validation.

Source delivery is always required. Desktop, Android/iOS, or web builds are
separate requested exports and need suitable presets, matching export templates,
and platform-specific setup. A source ZIP is not an executable build. A web build,
if requested, is a Godot export of the native project.

## With or without Godot MCP

| Task | With a suitable connected MCP | Without MCP |
| --- | --- | --- |
| Inspect the project | Query available editor/project tools | Read project settings and saved scenes; discover the engine |
| Author scenes | Use supported editor operations and explicitly save | Edit `.tscn` or run an offline Godot authoring script |
| Play and debug | Use available run, input, and log tools | Run Godot and inspect engine logs |
| Review appearance | Use an actual screenshot capability | Capture the rendered Godot viewport |

MCP capabilities vary by server. The skill discovers the actual tools rather
than assuming a fixed API, and checks that changes are saved to disk. It does not
install a server or change your MCP configuration as a prerequisite. See
[tooling](references/tooling.md) for the complete fallback workflow.

If neither a usable local engine nor an MCP engine is available, the agent can
write native source but must report that engine validation remains unverified.

## Requirements

| Dependency | When needed |
| --- | --- |
| Codex with this skill available | Agent workflow |
| Godot 4 | Native execution and validation; bundled starters require 4.3+ |
| Python 3.9+ | Bundled CLI helpers |
| Session image-generation tool | Generating raster art, when requested/appropriate |
| Pillow | Optional PNG import and contact sheets |
| Pillow, NumPy, SciPy | Optional ref2game image-analysis utilities |
| ffmpeg | Video-reference extraction and related video utilities |
| Working display/renderer | Rendered viewport capture; headless checks run separately |
| Matching export templates | Requested platform builds |

The native CLI workflow does not require Node.js, Playwright, a browser engine,
or MCP. Core scaffolding, checking, and source packaging use Python's standard
library. Optional Python dependencies can live in a project-local virtual environment.

## Bundled tools

Codex can run these tools during the workflow; you can also use them directly.

| Tool | Purpose |
| --- | --- |
| [scaffold.py](scripts/scaffold.py) | Create a new top-down/platformer starter with the requested level count; refuse overwrites |
| [godot.py](scripts/godot.py) | Discover the engine; import, check, run, open the editor, and capture frames |
| [scene_check.gd](scripts/scene_check.gd) | Load resources and instantiate scenes; briefly run every inventoried level |
| [capture.gd](scripts/capture.gd) | Render a scene with optional Input Map action replay |
| [art.py](scripts/art.py) | Prepare reference/style-guided image requests; preserve and validate imported PNGs |
| [package.py](scripts/package.py) | Package editable source, excluding caches and common local credentials |
| [ref2game utilities](scripts/vendor/ref2game/) | Reference study, visual comparison, slicing, contact sheets, and variant alignment |

For a manual starter, replace these two paths with your installed skill directory
and a **new empty game directory**:

```bash
R2G_SKILL="/absolute/path/to/ref2godot"
R2G_GAME="/absolute/path/to/my-game"

python3 "$R2G_SKILL/scripts/godot.py" doctor
python3 "$R2G_SKILL/scripts/scaffold.py" "$R2G_GAME" --genre topdown --levels 3 --name "My Game"
python3 "$R2G_SKILL/scripts/godot.py" check "$R2G_GAME"
python3 "$R2G_SKILL/scripts/godot.py" editor "$R2G_GAME"
```

Use `--genre platformer` for the other starter. `--levels` creates that many
saved rooms and connects progression; it does not design distinct finished rooms.
`editor` is an interactive foreground process; close it before continuing in that
terminal. You can then capture a level or package the source:

```bash
python3 "$R2G_SKILL/scripts/godot.py" capture "$R2G_GAME" --scene res://levels/level_01.tscn --out "$R2G_GAME/qa/level_01.png"
python3 "$R2G_SKILL/scripts/package.py" "$R2G_GAME" --out "/absolute/path/to/my-game-source.zip"
```

Capture output must be a new PNG path; source ZIP output must be new and outside
the game directory. If engine discovery fails, add `--godot /path/to/Godot` to
the `godot.py` command or set `GODOT_PATH`. Detection supports PATH commands,
common macOS bundles, and an explicit executable or macOS `.app`.

## Validation

The bundled checker imports the project, loads supported scene/script/resource
files, instantiates saved scenes, and runs each inventoried level briefly. It
checks engine error messages as well as exit codes, so an error logged by a
process that exits zero still fails. Reports and logs go under the game's `qa/`.

That establishes resource loading and a runtime smoke test. Finishing the game
also requires ordinary-control traversal, collision and interaction checks,
progression through the final level, rendered inspection, and verifying that
placement and exported-setting edits survive saving and reopening.

The skill and starters were validated on macOS with Godot **4.3 and 4.7.2**:
8 offline helper tests, 14 integration checks on each engine version, and an
independent two-level forward test with 11 gameplay/persistence assertions.
Live MCP, manual Inspector UI editing, mobile devices, and platform binary
exports were not covered. See [validation evidence](tests/VALIDATION.md) for
exact versions, coverage, and repeatable commands.

## How it differs from ref2game

[ref2game's README](https://github.com/studioigor/ref2game/blob/main/README.md)
describes a reference-to-browser-game workflow. ref2godot keeps reference study,
coherent art, playable iteration, visual comparison, and source delivery, and
adapts the implementation to Godot.

| Area | ref2game | ref2godot |
| --- | --- | --- |
| Runtime | Browser game in a small WebGL2 engine | Native Godot 4 project |
| Level handoff | Browser prototype and source | Every authored level saved as an editable `.tscn` |
| Preview | Browser page | Godot play session and rendered capture |
| Animation | Custom engine rigs and motion systems | Native sprite frames, cutout rigs, and suitable Godot systems |
| Tooling | Browser/Node/Python workflow | Godot/Python, with optional MCP |
| Delivery | Static playable build and assets | Editable project source; requested engine exports separately |

This repository is a Codex skill. It does not include ref2game's WebGL2 runtime,
browser reload workflow, or a separate Claude Code edition. Only five portable
MIT-licensed analysis/art utilities are vendored, unchanged and with attribution.

## Further reading

- [SKILL.md](SKILL.md): the agent's workflow and required output contract.
- [Scene authoring](references/scene-authoring.md): saved layouts, ownership, tiles,
  procedural baking, and edit preservation.
- [Art pipeline](references/art-pipeline.md): style guidance, generation requests,
  PNG import, and upstream utilities.
- [Gameplay and animation](references/gameplay-animation.md): controllers, signals,
  genre choices, animation, and effects.
- [Tooling](references/tooling.md), [validation](references/validation.md), and
  [delivery](references/delivery.md): execution, evidence, and source handoff.
- [Sources and design decisions](references/sources.md): researched commits,
  official Godot references, and licensing boundaries.

## License

MIT: see [LICENSE](LICENSE). Vendored ref2game helpers retain their upstream
[MIT license](scripts/vendor/ref2game/LICENSE). The
[GD-Agentic-Skills](https://github.com/thedivergentai/gd-agentic-skills) repository
was a research input; its code is not bundled and it is not a dependency.
