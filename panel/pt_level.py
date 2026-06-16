import bpy
import pathlib


class UI_PT_level(bpy.types.Panel):
    bl_idname = "UI_PT_level"
    bl_label = "level"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.window_manager.Level, "godot_path")
        layout.prop(context.window_manager.Level, "project_path")

        op = layout.operator("level.export_source", icon="EXPORT")
        op.path = context.window_manager.Level.project_path

        op = layout.operator("level.level2json", icon="EXPORT")
        op.path = str(
            pathlib.Path(bpy.path.abspath(context.window_manager.Level.project_path))
            / "Level"
        )
