from typing import Optional
import bpy  # type: ignore
from .humanoid_parts_properties import PROP_NAMES


def camel(src: str) -> str:
    tokens = src.split("_")
    return "".join([t[0].upper() + t[1:] for t in tokens])


def start_with(name, prefix):
    if name.startswith(prefix) and name[len(prefix) :] in bpy.data.objects:
        return name[len(prefix) :]


FINGER_MAP = {
    "left_thumb_metacarpal": "Finger0",
    "left_thumb_proximal": "Finger1",
    "left_thumb_distal": "Finger2",
    "left_index_proximal": "Finger0",
    "left_index_intermediate": "Finger1",
    "left_index_distal": "Finger2",
    "left_middle_proximal": "Finger0",
    "left_middle_intermediate": "Finger1",
    "left_middle_distal": "Finger2",
    "left_ring_proximal": "Finger0",
    "left_ring_intermediate": "Finger1",
    "left_ring_distal": "Finger2",
    "left_little_proximal": "Finger0",
    "left_little_intermediate": "Finger1",
    "left_little_distal": "Finger2",
    "right_thumb_metacarpal": "Finger0",
    "right_thumb_proximal": "Finger1",
    "right_thumb_distal": "Finger2",
    "right_index_proximal": "Finger0",
    "right_index_intermediate": "Finger1",
    "right_index_distal": "Finger2",
    "right_middle_proximal": "Finger0",
    "right_middle_intermediate": "Finger1",
    "right_middle_distal": "Finger2",
    "right_ring_proximal": "Finger0",
    "right_ring_intermediate": "Finger1",
    "right_ring_distal": "Finger2",
    "right_little_proximal": "Finger0",
    "right_little_intermediate": "Finger1",
    "right_little_distal": "Finger2",
}


def get_obj_name(prop: str) -> Optional[str]:
    finger_name = FINGER_MAP.get(prop)
    if finger_name:
        return finger_name

    name = f"{camel(prop)}"
    if name in bpy.data.objects:
        return name

    for prefix in [
        "Left",
        "Right",
    ]:
        new_name = start_with(name, prefix)
        if new_name:
            return new_name


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
