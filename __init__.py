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

import bpy  # type: ignore

from .humanoid_parts_properties import HumanoidProperties
from .humanoid_parts_search import HumanoidPartsSearch
from .humanoid_parts_assemble import HumanoidPartsAssemble
from .humanoid_parts_panels import HumanoidPartsAssemblePanel

classes = [
    HumanoidProperties,
    HumanoidPartsSearch,
    HumanoidPartsAssemble,
    HumanoidPartsAssemblePanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Armature.humanoid_parts = bpy.props.PointerProperty(
        type=HumanoidProperties
    )
    # bpy.types.Scene.humanoid_parts_collection = bpy.props.PointerProperty(
    #     type=bpy.types.Collection
    # )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
