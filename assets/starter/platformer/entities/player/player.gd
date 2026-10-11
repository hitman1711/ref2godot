extends CharacterBody2D

@export var move_speed: float = 260.0
@export var acceleration: float = 1800.0
@export var gravity: float = 1200.0
@export var jump_speed: float = 480.0
@export var coyote_seconds: float = 0.1
@export var jump_buffer_seconds: float = 0.12
@export var fall_reset_y: float = 720.0

var coyote_left: float = 0.0
var buffer_left: float = 0.0


func _physics_process(delta: float) -> void:
	coyote_left = coyote_seconds if is_on_floor() else maxf(0.0, coyote_left - delta)
	buffer_left = maxf(0.0, buffer_left - delta)
	if Input.is_action_just_pressed("jump"):
		buffer_left = jump_buffer_seconds
	if not is_on_floor():
		velocity.y += gravity * delta
	if buffer_left > 0.0 and coyote_left > 0.0:
		velocity.y = -jump_speed
		buffer_left = 0.0
		coyote_left = 0.0
	if Input.is_action_just_released("jump") and velocity.y < 0.0:
		velocity.y *= 0.5
	var direction := Input.get_axis("move_left", "move_right")
	velocity.x = move_toward(velocity.x, direction * move_speed, acceleration * delta)
	move_and_slide()
	if global_position.y > fall_reset_y:
		get_tree().call_deferred("reload_current_scene")
