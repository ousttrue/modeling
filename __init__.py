bl_info = {
    "name": "HumanoidParts",
    "blender": (3, 5, 0),
    # "category": "Rigging",
}


if "bpy" in locals():
    import importlib

    importlib.reload(humanoid_parts_properties)  # type: ignore
    importlib.reload(humanoid_parts_panels)  # type: ignore
    importlib.reload(humanoid_parts_search)  # type:ignore
    importlib.reload(humanoid_parts_assemble)  # type:ignore
    importlib.reload(humanoid_parts_disassemble)  # type:ignore

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
