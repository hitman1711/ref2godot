# Editable scene authoring

## Scene contract

An authored level is a saved `PackedScene`, not a runtime builder disguised as a scene. Typical 2D content:

```text
Level01 (Node2D + level rules/exported settings)
  Background (sprites/parallax)
  Terrain (TileMapLayer or placed StaticBody2D scene instances)
  Props (placed reusable scenes)
  Actors (placed player/enemy/NPC scenes)
  Spawns (Marker2D nodes or saved encounter scenes)
  Objectives (Area2D/interaction scenes)
  Lighting (lights, occluders, ambient settings)
  HUD (instanced CanvasLayer scene)
```

Use suitable names/types for the actual genre; this tree is not a required universal architecture. Each layout, tile cell, collision shape, trigger, spawn, and objective must survive closing and reopening the editor. Expose inspector properties such as speed, damage, encounter resources, dialogue, camera limits, and next-level scene. Do not hide the layout behind runtime coordinate arrays, external JSON, or `_draw()`.

Reusable entity scenes keep visuals, collision, animation, and behavior together. Instances are movable/duplicable in the level editor. Prefer exported overrides for designer variation; modify the reusable source scene for shared changes. Avoid making every nested child editable unnecessarily. Shared Resources can affect all instances: use a local-to-scene resource or duplicate it when an instance needs independent runtime state.

## Authoring options

1. **Direct text scenes:** write valid Godot 4 `format=3` `.tscn` with declared external/sub-resources and valid parent paths. Resource IDs must be unique in that file. Use `res://` paths; let the editor assign UIDs. Do not invent `uid://` identifiers or manually populate `.godot` caches.
2. **Editor/MCP:** build/edit the scene through available tools, explicitly save it, then inspect the saved disk scene and run the engine checks. An unsaved Remote tree is not a deliverable.
3. **Godot authoring script:** use Godot APIs to construct/pack a scene, especially for tiles, animations, and navigation where engine serialization avoids fragile text. Script construction is an **authoring/baking** step, not normal game startup.

## Ownership while baking

`add_child()` alone does not serialize a child. Set the appropriate scene owner after attaching each authored node. For new ordinary descendants, that is normally the scene root:

```gdscript
extends SceneTree

func _initialize() -> void:
	var level := Node2D.new()
	level.name = "AuthoredLevel"
	var spawn := Marker2D.new()
	spawn.name = "PlayerSpawn"
	level.add_child(spawn)
	spawn.owner = level
	spawn.position = Vector2(160, 240)
	var packed := PackedScene.new()
	var error := packed.pack(level)
	if error == OK:
		error = ResourceSaver.save(packed, "res://levels/authored_level.tscn")
	level.free()
	quit(0 if error == OK else 1)
```

For an instanced reusable scene, assign the instance root's owner to the level; preserve the instance's own child ownership. Inspect the resulting file to ensure it remains an instance rather than unnecessarily flattening its internals. For entirely new subtrees, assign ownership to their authored descendants. Persistent groups must be persisted (`add_to_group(name, true)`) when authoring through APIs.

Reopen the saved scene and check actual node count, resource references, properties, and transforms. Owner omissions can silently save an incomplete but syntactically valid scene.

## Tile levels

For Godot 4.3+, use one `TileMapLayer` per meaningful layer and a shared saved `.tres` TileSet. Include atlas textures, terrain sets, collision and navigation definitions as needed. Paint cells in the editor or use an offline Godot bake script with `set_cell`/terrain APIs, then pack/save. Do not reconstruct cells in `_ready()` or invent binary `tile_map_data` manually. World-to-cell queries use `local_to_map(to_local(world_position))`; cell centers use `to_global(map_to_local(cell))`.

Prefer editable collision shapes and bake navigation in Godot where required. A pretty map without valid collision/navigation is not a finished level. Verify reachable areas in the actual game; a navigation polygon alone does not prove the player can finish.

## Edit preservation and procedural games

Saved `.tscn` content is the source of truth after initial authoring. A later generator pass must produce new files, a reviewed diff, or an explicitly requested rebake. Never automatically rebake at runtime, import, or every skill invocation. Persist procedural seeds/settings in scene resources and deliver baked starting maps/chunks that a designer can open. Runtime roguelike generation may remain part of the requested game, but keep editable room templates and spawner/encounter definitions; explain which content is generated and which scene edits affect it.

Track all scoped levels in `ref2godot.json` (`levels`: array of `res://…tscn` paths). This is an inventory for tooling, **not** the layout source. Keep inventory and progression synchronized when a designer duplicates or renames a level. Custom projects may use their existing registry; reflect those paths in the inventory for the supplied checker.

Official references: [PackedScene](https://docs.godotengine.org/en/stable/classes/class_packedscene.html), [Node.owner](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-property-owner), [ResourceSaver](https://docs.godotengine.org/en/stable/classes/class_resourcesaver.html), [exported properties](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html), [TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html). Use version-matched docs when the installed engine differs from stable.
