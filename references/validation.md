# Observable validation

## Bundled checker

`godot.py check <project>` runs bounded editor import (`--headless --editor --import`), then an external SceneTree checker. It loads project `.gd`, `.gdshader`, `.tres`, and `.tscn` resources, instantiates every scene without activating it, and mounts every inventoried level for a short physics smoke test. Dot directories, `qa`, and `.gdignore` directories are skipped. Godot resolves scene dependencies.

Logs, exact engine version, tested paths, and failures are recorded in `qa/check_report.json`. Nonzero exits and engine error messages fail validation: Godot can report errors with exit code zero. This checker never changes layouts. `--scene` limits runtime smoke to that scene while still loading all resources; use the full inventory for final delivery.

`ref2godot.json` must be an object with a nonempty `levels` array of resource paths. Optional `minimum_godot` is a `4.x` minor version. A missing/empty inventory fails because the main scene alone cannot prove coverage. Reflect existing projects' actual registries in this inventory. The helper does not automatically recognize custom transition settings or game rules.

## Gameplay evidence

Headless loading cannot establish appearance, reachability, collision correctness, animation quality, performance, or full progression. Test each level's ordinary controls and core loop: safe spawn, solids/hazards, reachable objectives, loss/restart/pause where implemented, correct successor, and final ending. Check duplicated/edited levels independently for leaked state.

Use focused project-specific test scenes/action replay for fragile mechanics. Assert outcomes such as movement distance, contact, collected count, transition target, and persisted edits. Teleporting to objectives checks triggers but does **not** establish a playable route: also traverse using normal controls. Add regressions for reproduced defects rather than claiming universal coverage.

## Rendered capture and replay

`capture` loads the chosen level (or main scene), advances physics, and saves a viewport PNG. It needs a real display/renderer; headless dummy output cannot prove appearance. It uses the project's renderer and Dummy audio. Existing output paths are refused so stale images cannot count as success.

```bash
python3 "<skill>/scripts/godot.py" capture "<project>" --scene res://levels/level_01.tscn --frames 120 --out "<project>/qa/frame_120.png"
python3 "<skill>/scripts/godot.py" capture "<project>" --actions "<project>/qa/replay.json" --frames 150 --out "<project>/qa/moved.png"
```

Replay events use physics-frame numbers and actual Input Map names:

```json
[
  {"frame": 0, "action": "move_right", "pressed": true},
  {"frame": 40, "action": "jump", "pressed": true},
  {"frame": 48, "action": "jump", "pressed": false},
  {"frame": 90, "action": "move_right", "pressed": false}
]
```

This is a replay aid, not mouse/touch automation or a benchmark. Inspect actual images/cycle frames at game scale and match reference composition. Check long HUD strings and sprites against real backgrounds. Measure rendered frame rate separately on the target device.

## Editor round trip

Move a placed object and change an exported setting, save, reopen, and verify the run uses the changed values. Inspect ownership and instance boundaries. An automated companion can instantiate with editor state, change values, pack/save a temporary scene, and verify authored nodes/overrides in a fresh process; it complements visual editor testing.

The starter-specific [companion](../tests/starter_checks.gd) demonstrates this save/verify pattern; [the integration runner](../tests/run_engine_tests.py) invokes each phase in a fresh process. Adapt its node paths and assertions to the actual game instead of treating starter rules as universal requirements.

On user projects use a temporary copy/new scene or restore intended test changes exactly. Never regenerate scenes to force a test to pass. In `qa/REPORT.md`, distinguish import/resource checks, per-level gameplay, rendered inspection, edit persistence, and exports. Report only actually executed checks; retain logs for environment restrictions/timeouts.
