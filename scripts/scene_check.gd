extends SceneTree
## Engine-level resource loading plus bounded ready/physics smoke tests.

var failures: Array[String] = []
var scene_paths: Array[String] = []
var tested: Array[String] = []


func _initialize() -> void:
	call_deferred("_check")


func _option(key: String, fallback: String = "") -> String:
	var args := OS.get_cmdline_user_args()
	var index := args.find(key)
	return args[index + 1] if index >= 0 and index + 1 < args.size() else fallback


func _scan(path: String) -> void:
	var directory := DirAccess.open(path)
	if directory == null:
		failures.append("Cannot read " + path)
		return
	directory.list_dir_begin()
	var entry := directory.get_next()
	while not entry.is_empty():
		var child := path.path_join(entry)
		if not entry.begins_with("."):
			if directory.current_is_dir():
				if entry != "qa" and not FileAccess.file_exists(child.path_join(".gdignore")):
					_scan(child)
			elif entry.get_extension() in ["tscn", "tres", "gd", "gdshader"]:
				var resource := ResourceLoader.load(child)
				if resource == null:
					failures.append("Cannot load " + child)
				elif resource is PackedScene:
					var node: Node = resource.instantiate()
					if node == null:
						failures.append("Cannot instantiate " + child)
					else:
						node.free()
					scene_paths.append(child)
		entry = directory.get_next()
	directory.list_dir_end()


func _check() -> void:
	_scan("res://")
	var levels: Array[String] = []
	var requested := _option("--scene")
	if not requested.is_empty():
		levels.append(requested)
	elif FileAccess.file_exists("res://ref2godot.json"):
		var data: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://ref2godot.json"))
		if not data is Dictionary or not data.get("levels") is Array:
			failures.append("ref2godot.json must have a levels array")
		else:
			for entry: Variant in data["levels"]:
				if entry is String:
					levels.append(entry)
				else:
					failures.append("Level inventory entry is not a string")
	else:
		var main_scene: String = ProjectSettings.get_setting("application/run/main_scene", "")
		if not main_scene.is_empty():
			levels.append(main_scene)
		failures.append("Missing ref2godot.json level inventory; main scene alone cannot verify all levels")
	if levels.is_empty():
		failures.append("No levels to smoke test")
	var frames := maxi(1, int(_option("--frames", "12")))
	var seen: Array[String] = []
	for path: String in levels:
		if not path.begins_with("res://") or not path.ends_with(".tscn") or ".." in path.trim_prefix("res://").split("/"):
			failures.append("Level must be a project-local res:// .tscn: " + path)
			continue
		if path in seen:
			failures.append("Duplicate level inventory entry: " + path)
			continue
		seen.append(path)
		var packed := ResourceLoader.load(path) as PackedScene
		if packed == null:
			failures.append("Level is not a PackedScene: " + path)
			continue
		var level := packed.instantiate()
		if level == null:
			failures.append("Cannot instantiate level: " + path)
			continue
		if level.get_child_count() == 0:
			failures.append("Level has no saved children; author the layout in .tscn: " + path)
		root.add_child(level)
		current_scene = level
		for frame: int in range(frames):
			await physics_frame
		if is_instance_valid(level):
			level.queue_free()
			await process_frame
		else:
			failures.append("Level freed itself during smoke test: " + path)
		current_scene = null
		tested.append(path)
	print("REF2GODOT_CHECK " + JSON.stringify({"scenes_loaded": scene_paths.size(), "levels_tested": tested, "failures": failures}))
	quit(0 if failures.is_empty() else 1)
