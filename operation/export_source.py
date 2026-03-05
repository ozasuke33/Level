import bpy

import pathlib


class OBJECT_OT_export_source(bpy.types.Operator):
    bl_idname = "level.export_source"
    bl_label = "export_source"
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

        self.path = str(pathlib.Path(bpy.path.abspath(self.path)) / "Source")

        sources = bpy.data.collections["Source"].all_objects

        bpy.ops.object.select_all(action="DESELECT")
        for obj in sources:
            obj.select_set(True)

        bpy.ops.gaops.batch_export(export_format="GLTF_SEPARATE", path=self.path)

        return {"FINISHED"}
