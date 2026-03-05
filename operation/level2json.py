import bpy
import bpy_extras

import pathlib
import json
import math


class OBJECT_OT_level2json(bpy.types.Operator):
    bl_idname = "level.level2json"
    bl_label = "level2json"
    bl_options = {"REGISTER"}

    path: bpy.props.StringProperty(
        name="Export Path",
        default=bpy.app.tempdir,
        subtype="DIR_PATH",
        options={"PATH_SUPPORTS_BLEND_RELATIVE"},
    )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):

        if self.path == "":
            self.path = bpy.app.tempdir
        if self.path.startswith("//") and not bpy.data.is_saved:
            self.path = bpy.app.tempdir

        level_export = {}
        level_export["format"] = 1.0
        level_export["level"] = {}

        c = context.collection
        if c.name.startswith("Level"):
            level = {}
            level["level_name"] = c.name
            level["objects"] = []
            for i in c.all_objects:
                dict = {}
                dict["object_name"] = i.name
                dict["instance_name"] = i.data.name
                dict["parent_name"] = ""
                if i.parent:
                    dict["parent_name"] = i.parent.name
                dict["location_xyz"] = (i.location.x, i.location.z, i.location.y * -1)
                dict["rotation_euler_xyz"] = (
                    i.rotation_euler.x,
                    i.rotation_euler.z,
                    i.rotation_euler.y * -1,
                )
                dict["scale_xyz"] = (i.scale.x, i.scale.z, i.scale.y)
                level["objects"].append(dict)
            level_export["level"] = level

        filename = str(pathlib.Path(bpy.path.abspath(self.path)) / (c.name + ".json"))
        with open(filename, "w") as file:
            json.dump(level_export, file, indent=4)

        return {"FINISHED"}
