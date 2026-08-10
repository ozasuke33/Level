import bpy
import bpy_extras

import pathlib
import json
import math
import subprocess
import os


def idprop_to_python(value):
    if isinstance(value, bpy.types.ID):
        return value.name
    if hasattr(value, "to_list"):
        return list(value)
    if hasattr(value, "keys"):
        return {k: idprop_to_python(value[k]) for k in value.keys()}
    if isinstance(value, list):
        return [idprop_to_python(v) for v in value]
    return value


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
                dict["matrix"] = [v for row in i.matrix_local for v in row]
                props = {k: idprop_to_python(i[k]) for k in i.keys() if k != "_RNA_UI"}
                if props:
                    dict["custom_properties"] = props
                level["objects"].append(dict)
            level_export["level"] = level
        else:
            self.report({"ERROR"}, "No level has been selected.")
            return {"FINISHED"}

        pathlib.Path(bpy.path.abspath(self.path)).mkdir(exist_ok=True)
        filename = str(pathlib.Path(bpy.path.abspath(self.path)) / (c.name + ".json"))
        with open(filename, "w") as file:
            json.dump(level_export, file, indent=4)

        script_name = str(
            pathlib.Path(os.path.dirname(__file__)) / "load_level_json.gd"
        )

        subprocess.Popen(
            [
                context.window_manager.Level.godot_path,
                "--headless",
                "--path",
                context.window_manager.Level.project_path,
                "--script",
                script_name,
                "--quit",
                "--",
                c.name,
            ]
        )

        return {"FINISHED"}
