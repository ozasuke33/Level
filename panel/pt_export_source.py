import bpy

class UI_PT_export_source(bpy.types.Panel):
    bl_idname = "UI_PT_export_source"
    bl_label = "export source"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level"

    def draw(self, context):
        layout = self.layout

        layout.operator("level.export_source")