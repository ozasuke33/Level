extends SceneTree

func blender_to_godot(m: Array) -> Transform3D:
	# Blenderの行列（行優先）をそのままTransform3Dに
	var t_blender = Transform3D(
		Basis(
			Vector3(m[0], m[4], m[8]), # 列0
			Vector3(m[1], m[5], m[9]), # 列1
			Vector3(m[2], m[6], m[10]) # 列2
		),
		Vector3(m[3], m[7], m[11]) # origin
	)

	# Blender(右手系,Z-up) → Godot(右手系,Y-up)
	const P := Transform3D(
		Basis(
			Vector3(1, 0, 0),
			Vector3(0, 0, -1),
			Vector3(0, 1, 0)
		),
		Vector3.ZERO
	)

	return P * t_blender * P.inverse()

func set_owner_recursive(node, owner):
	if node != owner:
		node.owner = owner
	for c in node.get_children():
		set_owner_recursive(c, owner)

func _init():
	var name = OS.get_cmdline_user_args()[0]
	var file_path = "res://Level/" + name + ".json"
	var file = FileAccess.open(file_path, FileAccess.READ)
	var content = file.get_as_text()
	file.close()
	var json = JSON.new()
	json.parse(content)
	var data = json.data

	var level = data["level"]
	var l = Node3D.new()
	l.name = level["level_name"]

	var nodes = {}
	var parent_name = {}

	for obj in level["objects"]:
		var n = Node3D.new()
		n.name = obj["object_name"]
		n.transform = blender_to_godot(obj["matrix"])

		var gltf: PackedScene = load("res://" + "Source/" + obj["instance_name"] + ".gltf")
		var inst = gltf.instantiate()
		inst.transform = Transform3D.IDENTITY
		n.add_child(inst)
		nodes[obj["object_name"]] = n
		parent_name[obj["object_name"]] = obj["parent_name"]

	for k in nodes:
		var n = nodes[k]
		if parent_name[k] != "":
			var parent = nodes[parent_name[k]]
			parent.add_child(n)
			n.owner = parent
		else:
			l.add_child(n)
			n.owner = l

	set_owner_recursive(l, l)

	var scene = PackedScene.new()

	scene.pack(l)

	ResourceSaver.save(scene, "res://Level/" + name + ".tscn")

	quit()
