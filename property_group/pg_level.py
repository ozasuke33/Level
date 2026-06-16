import bpy


class PropertyGroup_level(bpy.types.PropertyGroup):

    godot_path: bpy.props.StringProperty(name="Godot Exe", subtype="FILE_PATH")

    project_path: bpy.props.StringProperty(
        name="Project Path",
        default=bpy.app.tempdir,
        subtype="DIR_PATH",
        options={"PATH_SUPPORTS_BLEND_RELATIVE"},
    )
