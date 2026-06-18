extends SceneTree

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
		n.position[0] = obj["location_xyz"][0]
		n.position[1] = obj["location_xyz"][1]
		n.position[2] = obj["location_xyz"][2]
		n.rotation[0] = obj["rotation_euler_xyz"][0]
		n.rotation[1] = obj["rotation_euler_xyz"][1]
		n.rotation[2] = obj["rotation_euler_xyz"][2]
		n.scale[0] = obj["scale_xyz"][0]
		n.scale[1] = obj["scale_xyz"][1]
		n.scale[2] = obj["scale_xyz"][2]
		var gltf: PackedScene = load("res://" + "Source/" + obj["instance_name"] + ".gltf")
		var inst = gltf.instantiate()
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
