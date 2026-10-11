# Validation evidence

Validated on macOS on 2026-10-11. This records checks of the **skill and its
starters**, not a guarantee that every future generated game is correct.

## Executed checks

- Codex skill frontmatter validation passed using the skill-creator validator.
- Eight offline helper tests passed, including unchanged PNG import, alpha
  checks, edit preservation, safe source packaging, timeout handling, and
  rejecting engine errors even when the process returns zero.
- Fourteen integration checks passed on **each** of Godot
  `4.3.stable.official.77dcf97d8` and
  `4.7.2.stable.official.ed1daf0bf`. Both genres were imported, all saved scenes
  were loaded, and every inventoried starter level was executed.
- Native behavior checks exercised movement, solid collision, platformer
  jumping/landing, pickup triggers, gated exits, progression, and final
  completion. Trigger tests also use deliberate actor repositioning; ordinary
  route reachability was separately tested in the forward test below.
- A saved object transform and Player speed override survived packing and
  reopening in a fresh engine process. The reusable Player instance remained
  an instance, and running used the changed spawn.
- Actual viewport PNGs were captured and inspected for both genres. Input
  replay changed the rendered frame; invalid replay was rejected without
  producing an output image.
- Source ZIPs were unpacked into clean directories and successfully reimported.
  A broken second level correctly failed validation while the first level still
  worked.
- The five unchanged ref2game utilities were exercised on rendered/synthetic
  fixtures: study, diff/report, connected-component slicing, contact sheets,
  and variant alignment. The variant fixture uses varied colors because color
  matching can erase a difference on a uniform-color base; threshold choices
  still require inspection for real art.

An independent forward test used the skill to create two distinct geometric
top-down levels. Eleven focused assertions passed: persisted placement/speed,
retained scene instances, ordinary movement and boundary collision, restart,
exit gating, traversal of both levels using normal controls, progression, and
final completion. Both rendered levels were inspected, and the full checker
passed. Its feedback led to explicit support for user-selected native geometric
art and a linked scene persistence test example.

## Repeat the automated checks

From the skill repository, using Python 3.9+:

```bash
python3 -m unittest discover -s tests -v
python3 tests/run_engine_tests.py --godot /absolute/path/to/Godot --capture
```

Pillow enables the optional PNG test; otherwise that test is explicitly skipped.
The utility fixtures additionally need NumPy and SciPy. The integration runner
needs Godot 4.3+; `--capture` needs a working display. Omit that flag for headless
resource/gameplay checks. A sandbox must permit the engine's normal user-data
and editor-settings writes.

The runner creates isolated projects and retains logs, captures, source ZIPs,
and `results.json` under ignored `work/engine-tests-*`. Tests intentionally
corrupt a second level at the end to prove detection; those temporary projects
are evidence fixtures, not deliverables. No user project is regenerated.

Final authoring-run reports are `work/engine-tests-jygwsvfa/results.json`
(4.3) and `work/engine-tests-1klzhzm7/results.json` (4.7.2). These are local
evidence files; a new checkout can reproduce them with the commands above.

[starter_checks.gd](starter_checks.gd) contains the starter-specific save,
fresh-process verify, and gameplay harness. Adapt node paths and game rules
before using it on another game. Forward-test evidence remains under ignored
`work/forward-test/` in the authoring checkout, rather than becoming a dependency
of the portable skill.

## Coverage limits

No live Godot MCP server was connected. The CLI path was exercised; MCP support
uses runtime capability/schema discovery. No paid image generation, target
device benchmark, platform binary export, 3D workflow, or manual Inspector UI
edit was claimed. Persistence was tested through Godot's saved editor scene
state in separate processes, alongside actual rendered inspection. A restricted
run and an intermittent installed-engine import crash were retained as failures;
successful native runs required normal engine data access and a clean retry.
