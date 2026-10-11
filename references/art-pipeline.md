# Reference, art, and Godot integration

## Study the target

Record a short style bible: projection/camera, shape language, palette/value groups, outline weight, material/brush treatment, texture density, and one consistent light direction. Use the same wording on each generation. Record reference dimensions, target viewport, on-screen actor sizes, and layers in `docs/STYLE.md`. Sketch the first-frame layout; distinguish faithful composition from matching only the art style.

For videos, sample action beats, transitions, and the ending. A still cannot establish movement speed, timing, or camera behavior. ffmpeg can extract frames; optional `vendor/ref2game/study.py` can probe stills/video and analyze palette/layout. Read its `--help` rather than guessing flags.

## Generate and import

Generate separate backgrounds/depth bands, terrain textures, props, character anchors/parts, collectibles, and UI frames as needed. Keep dynamic text, glow, light rays, shadows, particles, and water motion in Godot when they must react or animate. Use an approved actor anchor as a design reference for parts and variants.

Use the session's image-generation capability and current schema. Inspect local references before edits. Choose real transparency for isolated sprites, opaque output for backgrounds/tiles. Respect the tool's limits on references/concurrency. Do not promise exact AI output or an unverified cost model.

```bash
python3 "<skill>/scripts/art.py" prepare "<project>" hero "<project>/art/prompts/hero.txt" --ref "/path/ref.png"
python3 "<skill>/scripts/art.py" prepare "<project>" ground "<project>/art/prompts/ground.txt" --ref "/path/ref.png" --opaque
python3 "<skill>/scripts/art.py" import "<project>" hero "/returned/hero.png" --alpha required
```

`prepare` writes `art/requests/<name>.json` with prompt/reference/transparency arguments. Call the image tool yourself; the helper never generates. For conversation-only references use the image tool's conversation-reference mechanism directly instead of inventing a local path. `import` copies the unchanged PNG into `art/source/` and `assets/textures/` and records dimensions/alpha bounds in `art/manifest.json`. It requires Pillow; `prepare` uses only stdlib. `--replace` means an intentional revision.

Inspect for baked checkerboard, halos, inconsistent anatomy, missing parts, and unwanted effects; alpha bounds cannot catch these. The manifest records measurements, not level placement or completed rig data. Set display sizes/pivots in the actor/prop scene and retain those values when replacing textures at a different resolution.

## Native integration

- Runtime textures go in `assets/textures/`; raw references/prompts are excluded by `art/.gdignore`.
- Choose nearest filtering/integer scaling for low-res pixel art; linear filtering where needed. Set repeat for tileable materials and check seams.
- Use Sprite2D regions/AtlasTexture when appropriate. Trimming must preserve crop offsets/pivots so variants stay registered.
- Save visuals/animations in reusable `.tscn` scenes and SpriteFrames/AnimationLibrary Resources. ref2game JS rig output is not a Godot animation resource.
- Align collision with readable solid surfaces, not decorative overhangs. Top-down actors commonly collide at their feet; separate that from sprite center.
- Implement lights, occlusion, particles, and shaders with native nodes compatible with the renderer. Compare a neutral frame before strong effects conceal mismatches.

## Optional portable upstream utilities

`scripts/vendor/ref2game/` contains unchanged MIT helpers; see [sources](sources.md). Load only the relevant utility. Pillow, NumPy, and SciPy are optional dependencies (sheet.py needs only Pillow). Use a project-local environment rather than changing system Python.

```bash
python3 -m venv "<project>/.venv"
"<project>/.venv/bin/python" -m pip install Pillow numpy scipy
"<project>/.venv/bin/python" "<skill>/scripts/vendor/ref2game/slice.py" "/path/parts.png" body,arm,leg --out "<project>/art/source"
"<project>/.venv/bin/python" "<skill>/scripts/vendor/ref2game/sheet.py" "<project>/qa/cycle.png" "/path/frame_01.png" "/path/frame_02.png" --label
"<project>/.venv/bin/python" "<skill>/scripts/vendor/ref2game/compare.py" report "/path/reference.png" "<project>/qa/match.png" --out "<project>/qa/comparison"
```

Windows venvs use `Scripts/python.exe`. `variantfix.py` aligns/color-matches variants and preserves unchanged regions; inspect before replacing approved art. `compare.py` imports `study.py`, so retain both. These tools measure visual gaps, not gameplay/human quality. Align camera/composition and crop borders consistently before comparing.
