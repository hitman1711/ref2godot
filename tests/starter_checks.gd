extends SceneTree
## Real engine tests: fresh-process serialization plus controller/progression behavior.

var failures: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func _option(key: String, fallback: String = "") -> String:
	var args := OS.get_cmdline_user_args()
	var index := args.find(key)
	return args[index + 1] if index >= 0 and index + 1 < args.size() else fallback


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)


func _wait_frames(count: int) -> void:
	for frame: int in range(count):
		await physics_frame


func _release() -> void:
	for action: String in ["move_left", "move_right", "move_up", "move_down", "jump"]:
		Input.action_release(action)


func _run() -> void:
	var phase := _option("--phase", "gameplay")
	if phase == "save":
		var packed := load("res://levels/level_01.tscn") as PackedScene
		var level := packed.instantiate(PackedScene.GEN_EDIT_STATE_INSTANCE)
		(level.get_node("PlayerSpawn") as Marker2D).position = Vector2(144, 270)
		(level.get_node("Pickups/Diamond01") as Node2D).position = Vector2(300, 150)
		level.get_node("Player").set("move_speed", 321.0)
		var saved := PackedScene.new()
		_expect(saved.pack(level) == OK, "Packing the edited scene failed")
		_expect(ResourceSaver.save(saved, "res://qa/edited.tscn") == OK, "Saving the edited scene failed")
		level.free()
	elif phase == "verify":
		var packed := load("res://qa/edited.tscn") as PackedScene
		var level := packed.instantiate()
		_expect((level.get_node("PlayerSpawn") as Marker2D).position == Vector2(144, 270), "Spawn edit was lost")
		_expect((level.get_node("Pickups/Diamond01") as Node2D).position == Vector2(300, 150), "Placement edit was lost")
		_expect(level.get_node("Player").get("move_speed") == 321.0, "Inspector override was lost")
		_expect(level.get_node("Terrain").get_child_count() >= 4, "Saved terrain was lost")
		root.add_child(level)
		current_scene = level
		await _wait_frames(2)
		_expect((level.get_node("Player") as Node2D).global_position.distance_to(Vector2(144, 270)) < 1.0, "Runtime ignored edited spawn")
	else:
		await _gameplay()
	print("REF2GODOT_TEST " + JSON.stringify({"phase": phase, "failures": failures}))
	quit(0 if failures.is_empty() else 1)


func _gameplay() -> void:
	var packed := load("res://levels/level_01.tscn") as PackedScene
	var level := packed.instantiate()
	root.add_child(level)
	current_scene = level
	await _wait_frames(12)
	var player := level.get_node("Player") as CharacterBody2D
	var before := player.global_position
	Input.action_press("move_right")
	await _wait_frames(30)
	Input.action_release("move_right")
	_expect(player.global_position.x > before.x + 50.0, "Normal input did not move the player")
	if _option("--genre") == "platformer":
		# Move back into open space; the movement check ended beneath a solid ledge.
		player.global_position = before
		player.velocity = Vector2.ZERO
		await _wait_frames(12)
		var ground_y := player.global_position.y
		Input.action_press("jump")
		await _wait_frames(10)
		_expect(player.global_position.y < ground_y - 25.0, "Jump did not lift the player")
		Input.action_release("jump")
		await _wait_frames(90)
		_expect(player.is_on_floor(), "Player did not land on saved collision")
	else:
		Input.action_press("move_right")
		await _wait_frames(150)
		Input.action_release("move_right")
		_expect(player.global_position.x < 375.0, "Player passed through the authored obstacle")
	# Trigger coverage is intentionally separate from ordinary-input movement tests.
	for pickup: Node2D in level.get_node("Pickups").get_children():
		player.global_position = pickup.global_position
		player.velocity = Vector2.ZERO
		await _wait_frames(8)
	_expect(level.get("collected") == level.get("total"), "Pickup signals/count did not complete")
	player.global_position = (level.get_node("Exit") as Node2D).global_position
	player.velocity = Vector2.ZERO
	await _wait_frames(12)
	_expect(current_scene != level, "Completing the first level did not transition")
	_expect(current_scene.scene_file_path == "res://levels/level_02.tscn", "Wrong next level")
	var final_level := current_scene
	player = final_level.get_node("Player") as CharacterBody2D
	for pickup: Node2D in final_level.get_node("Pickups").get_children():
		player.global_position = pickup.global_position
		player.velocity = Vector2.ZERO
		await _wait_frames(8)
	player.global_position = (final_level.get_node("Exit") as Node2D).global_position
	player.velocity = Vector2.ZERO
	await _wait_frames(10)
	_expect(bool(final_level.get("completed")), "Final completion was not recorded")
	_expect(not player.is_physics_processing(), "Completion did not stop the player")
	_release()
