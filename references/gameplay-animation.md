# Native gameplay, animation, and feel

The starters demonstrate independent saved levels, reusable entities, movement/collision, pickup goals, restart, and progression. They contain polygon placeholders and repeated starter layouts. Adapt them to the planned game; they are not completed reference recreations.

## Systems and genres

- Controlled characters use CharacterBody2D, velocity in pixels/second, and `move_and_slide()` in `_physics_process`. Multiply gravity/acceleration by delta, not velocity again before `move_and_slide()`.
- Platformers benefit from jump buffering, coyote time, variable jump height, and deliberate acceleration/braking. Verify routes under actual physics; a reachable-looking platform must actually be reachable.
- Normalize top-down diagonal input (Input.get_vector). For isometric art, distinguish logical collision coordinates from art projection and use sensible Y-sort/foot origins.
- Puzzle/card/UI games may use Control nodes instead of a character controller. Save editable boards/levels as `.tscn`; do not force a supplied genre starter onto them.
- Combat requires aligned origins/hitboxes, timing, telegraphs, recovery, and loss/restart. Persist encounter configuration in scenes; runtime spawners consume exported Resources/Marker2D nodes.
- Prefer scene-local signals and explicit connections. Add persistent managers only for state that must survive transitions; test reset/restart behavior.
- Read saved transforms/resources instead of resetting props from code constants. A player can start at an editable saved marker; static authored objects must stay where the designer placed them.

Starter collision layers: bit 1 = world (`1`), bit 2 = player (`2`), bit 3 = triggers (`4`). Masks use bit values, not the human layer number. Add project-specific layers deliberately.

## Animation choices

| Need | Native option |
| --- | --- |
| Pixel character frames | AnimatedSprite2D + SpriteFrames |
| Cutout actor | Node2D/Sprite2D hierarchy + AnimationPlayer; Skeleton2D/Bone2D for deformation |
| Blending/state complexity | AnimationTree when warranted |
| Foliage/cloth/breathing accents | Procedural secondary motion or CanvasItem shader |
| UI/pop/one-shot response | Tween or AnimationPlayer |

Do not impose cutout rigs on every style. Check contacts, foot slide, knees, limb lengths, layering, and transitions for rigged walkers. Inspect full cycles and relevant attack directions. Sprite-frame animation needs complete frames and consistent registration, not unrelated poses. Use RESET/property baselines where appropriate. Keep controller root separate from visual/rig root so squash and shake do not distort collision. Avoid animation tracks and gameplay scripts fighting over the same property.

## Effects and feel

Drive sound, flashes, particles, brief hit-stop, camera impulses, and HUD response from actual gameplay events. Camera shake should recover quickly and preserve readability. Keep camera limits/tuning editable. Pause UI must continue processing while gameplay is paused.

Use native particle/light/occluder/modulation nodes and CanvasItem shaders compatible with the selected renderer. Do not copy WebGL2 shaders verbatim. Shared wind/time can keep foliage coherent; reactive objects should respond to the player. Profile actual physics/rendering before introducing low-level optimization that makes a small level harder to edit.

Official references: [CharacterBody2D](https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html), [2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html), [AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html), [CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html).
