extends Node2D
## Level rules use saved scene children; there is no runtime layout reconstruction.

@export var level_title: String = "Level"
@export_file("*.tscn") var next_level: String = ""

var collected: int = 0
var total: int = 0
var completed: bool = false

@onready var player: CharacterBody2D = $Player
@onready var spawn: Marker2D = $PlayerSpawn
@onready var hud: CanvasLayer = $HUD


func _ready() -> void:
	player.global_position = spawn.global_position
	for pickup: Node in $Pickups.get_children():
		if pickup.has_signal("collected"):
			total += 1
			pickup.connect("collected", _on_pickup)
	$Exit.connect("entered", _on_exit)
	_update_hud()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("restart"):
		get_tree().call_deferred("reload_current_scene")


func _on_pickup() -> void:
	collected += 1
	_update_hud()


func _update_hud() -> void:
	hud.call("set_status", "%s  •  %d / %d diamonds  •  R: restart" % [level_title, collected, total])


func _on_exit() -> void:
	if completed:
		return
	if collected < total:
		hud.call("set_status", "Collect all diamonds before leaving (%d / %d)" % [collected, total])
		return
	completed = true
	if next_level.is_empty():
		player.set_physics_process(false)
		hud.call("set_status", "All levels complete!  •  R: replay this level")
	else:
		get_tree().call_deferred("change_scene_to_file", next_level)
