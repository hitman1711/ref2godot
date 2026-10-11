extends CharacterBody2D

@export_range(1.0, 1200.0, 1.0) var move_speed: float = 220.0
@export_range(1.0, 10000.0, 1.0) var acceleration: float = 1800.0


func _physics_process(delta: float) -> void:
	var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = velocity.move_toward(direction * move_speed, acceleration * delta)
	move_and_slide()
