bl_info = {
    "name": "Level",
    "author": "ozasuke",
    "description": "Level",
    "blender": (5, 0, 0),
    "version": (0, 1, 0),
    "location": "3D Vieport > Sidebar",
    "warning": "",
    "category": "Object",
}

import bpy

from . import _refresh_

_refresh_.reload_modules()

from .operation.export_source import *
from .operation.level2json import *
from .panel.pt_export_source import *
from .panel.pt_level2json import *

classess = [
    OBJECT_OT_export_source,
    OBJECT_OT_level2json,
    UI_PT_export_source,
    UI_PT_level2json
]

def register():
    for cls in classess:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classess):
        bpy.utils.unregister_class(cls)
