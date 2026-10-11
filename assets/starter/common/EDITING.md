# Edit this game in Godot

Open `project.godot` in Godot 4.3 or later (use the version recorded in the final handoff).
F5 runs the game; F6 runs the currently open level. WASD/arrows move, Space jumps in
the platformer starter, and R restarts the current level. Collect all diamonds, then
enter the green exit. The final level shows completion; R plays it again.

## Change a level

1. Open a scene in `levels/`. The scene tree contains the authored terrain, player,
   pickups, exit, and HUD. Select and move these nodes in the 2D viewport.
2. Move `PlayerSpawn` to change the start position. The saved Player instance is
   moved to this marker when play begins.
3. Duplicate/move a pickup under `Pickups`. The level derives the goal count from
   these saved nodes; there is no separate coordinate list to update.
4. Edit terrain `Polygon2D` vertices and its corresponding collision shape together.
   They are saved scene resources. Keep physics bodies at scale (1, 1); resize shapes
   instead of non-uniformly scaling a collision body.
5. Select the level root to change `level_title` and `next_level` in the Inspector.
   Empty `next_level` means the final level. Select Player to override controller
   settings such as speed (or jump speed in the platformer).
6. Save, close/reopen the scene, and run F6. Changes must remain after a restart.

## Change shared actors and art

Open `entities/player/player.tscn`, `entities/pickup/pickup.tscn`, or
`entities/exit/exit.tscn` to change all instances. Replace placeholder Polygon2D art
with Sprite2D/AnimatedSprite2D or a cutout rig; keep collision and signals wired.
Use scene overrides for a single instance. Textures belong in `assets/textures/`;
source/reference images and prompts belong in `art/` and are excluded from importing.

## Add a level

Save an existing level as a **new** `levels/level_NN.tscn`; change its actual layout
and objectives. Set the previous level root's `next_level` to the new `res://` path.
Set the new level's next path (or leave it empty for the ending). Add its path to
the `levels` array in `ref2godot.json` so automated checks cover it. To change the
starting level, edit Project Settings → Application → Run → Main Scene.

Do not regenerate the project over edited levels. Scene files are the source of
truth; there is no runtime level generator. These starter instructions should be
extended with the finished game's actual mechanics, level list, and tested version.
