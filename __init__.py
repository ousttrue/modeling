bl_info = {
    "name": "HumanoidParts",
    "blender": (3, 5, 0),
    # "category": "Rigging",
}

import sys

if "bpy" in locals():
    import importlib

    # print(sys.modules.keys())

    def reload(module_name: str):
        module_name = f"{__name__}.{module_name}"
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            print(f"no reload: {module_name}")

    reload("humanoid_parts_properties")
    reload("humanoid_parts_panels")
    reload("humanoid_parts_search")
    reload("humanoid_parts_assemble")
    reload("humanoid_parts_disassemble")

import bpy  # type: ignore

from . import humanoid_parts_properties
from . import humanoid_parts_search
from . import humanoid_parts_assemble
from . import humanoid_parts_panels
from . import humanoid_parts_disassemble

modules = [
    humanoid_parts_properties,
    humanoid_parts_search,
    humanoid_parts_assemble,
    humanoid_parts_panels,
    humanoid_parts_disassemble,
]


def register():
    for m in modules:
        m.register()


def unregister():
    for m in modules:
        m.unregister()


if __name__ == "__main__":
    register()
