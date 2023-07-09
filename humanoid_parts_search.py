from typing import Optional
import bpy  # type: ignore
from .humanoid_parts_properties import PROP_NAMES


def camel(src: str) -> str:
    tokens = src.split("_")
    return "".join([t[0].upper() + t[1:] for t in tokens])


def get_obj_name(prop: str) -> Optional[str]:
    name = f"_{camel(prop)}"
    if prop.startswith("left_"):
        name = "_" + name[5:] + ".L"
    elif prop.startswith("right_"):
        name = "_" + name[6:] + ".R"
    if name in bpy.data.objects:
        return name


class HumanoidPartsSearch(bpy.types.Operator):
    bl_idname = "humanoid_parts.search"
    bl_label = "Search humanoid parts"
    bl_description = "Search humanoid parts by name"
    bl_options = {"REGISTER", "UNDO"}
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return isinstance(context.active_object.data, bpy.types.Armature)

    def execute(self, context):
        armature = context.active_object.data

        for prop in PROP_NAMES:
            name = get_obj_name(prop)
            print(prop, name)
            if name and name in bpy.data.objects:
                o = bpy.data.objects[name]
                setattr(armature.humanoid_parts, prop, o)

        return {"FINISHED"}


def register():
    print(__name__)
    bpy.utils.register_class(HumanoidPartsSearch)


def unregister():
    print(__name__)
    bpy.utils.unregister_class(HumanoidPartsSearch)
