from importlib import reload
import sys
import bpy

from .operation import export_source
from .operation import level2json

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    
    reload(sys.modules[__name__])
    reload(export_source)
    reload(level2json)