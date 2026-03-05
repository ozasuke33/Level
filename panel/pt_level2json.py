import bpy

class UI_PT_level2json(bpy.types.Panel):
    bl_idname = "UI_PT_level2json"
    bl_label = "level2json"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level"

    def draw(self, context):
        layout = self.layout

        layout.operator("level.level2json")