extends SceneTree
## Render a scene with optional action replay; requires a real rendering backend.


func _initialize() -> void:
	call_deferred("_capture")


func _option(key: String, fallback: String = "") -> String:
	var args := OS.get_cmdline_user_args()
	var index := args.find(key)
	return args[index + 1] if index >= 0 and index + 1 < args.size() else fallback


func _capture() -> void:
	if DisplayServer.get_name() == "headless":
		push_error("Rendered capture needs a display; headless smoke tests cannot prove appearance.")
		quit(1)
		return
	var scene: String = _option("--scene", ProjectSettings.get_setting("application/run/main_scene", ""))
	var packed := ResourceLoader.load(scene) as PackedScene
	if packed == null:
		push_error("Cannot load capture scene: " + scene)
		quit(1)
		return
	var events: Array = []
	var replay := _option("--actions")
	if not replay.is_empty():
		var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(replay))
		if not data is Array:
			push_error("Replay must be a JSON array")
			quit(1)
			return
		events = data
		for event: Variant in events:
			if not event is Dictionary or not event.get("frame") is float or not event.get("action") is String or not event.get("pressed") is bool:
				push_error("Replay events need frame (integer >= 0), action (Input Map name), and pressed (boolean)")
				quit(1)
				return
			if float(event["frame"]) < 0 or float(event["frame"]) != floor(float(event["frame"])) or not InputMap.has_action(event["action"]):
				push_error("Invalid replay frame or unknown Input Map action")
				quit(1)
				return
	var level := packed.instantiate()
	root.add_child(level)
	current_scene = level
	var frames := maxi(1, int(_option("--frames", "90")))
	for frame: int in range(frames):
		for event: Dictionary in events:
			if int(event["frame"]) == frame:
				if event["pressed"]:
					Input.action_press(event["action"])
				else:
					Input.action_release(event["action"])
		await physics_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var error := image.save_png(_option("--out"))
	print("REF2GODOT_CAPTURE " + JSON.stringify({"scene": scene, "frames": frames, "error": error, "out": _option("--out")}))
	quit(0 if error == OK else 1)
