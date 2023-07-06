import bpy  # type: ignore
import mathutils  # type: ignore
from .humanoid_parts_properties import PROP_NAMES


def get_vertex(mesh_obj, vg_index):
    for v in mesh_obj.data.vertices:
        for vg in v.groups:
            if vg.group == vg_index:
                return v


def enumerate_joints(armature_obj, mesh_obj):
    for i, vg in enumerate(mesh_obj.vertex_groups):
        for b in armature_obj.data.bones:
            name = b.name
            if name.endswith(".L") or name.endswith(".R"):
                name = name[:-2]
            if vg.name == name:
                # print(f'found {name}')
                yield name, get_vertex(mesh_obj, i)
                break


def move_recursive(bone, delta):
    bone.head += delta
    if len(bone.children) == 0:
        bone.tail += delta
    else:
        for child in bone.children:
            move_recursive(child, delta)


def fit_parent_bone(parent, obj):
    # if not parent:
    parent = bpy.data.objects["Humanoid"]
    obj.parent = parent
    obj.parent_type = "BONE"
    obj.parent_bone = obj.name[1:]

    if parent and obj.parent_type == "BONE":
        bone = parent.data.bones[obj.parent_bone]
        print(bone)
        length = (bone.tail - bone.head).length
        if obj.name.endswith(".R"):
            obj.scale = (-length, length, length)
        else:
            obj.scale = (length, length, length)
        obj.location = (0, -length, 0)
        # print(obj, parent, obj.parent_type, )

        try:
            backup = bpy.context.view_layer.objects.active
            bpy.context.view_layer.objects.active = parent
            bpy.ops.object.mode_set(mode="EDIT")

            for name_with_vertex in enumerate_joints(parent, obj):
                name, vertex = name_with_vertex
                local_tail_position = vertex.co
                if obj.name.endswith(".L"):
                    name += ".L"
                elif obj.name.endswith(".R"):
                    name += ".R"

                edit_bone = parent.data.edit_bones[obj.parent_bone]

                new_pos = (
                    edit_bone.matrix
                    @ mathutils.Matrix.LocRotScale(None, None, obj.scale)
                    @ local_tail_position
                )

                bone = parent.data.edit_bones[name]
                delta = new_pos - bone.head
                print(delta)
                # TODO: move all descendants by delta
                move_recursive(bone, delta)
                # parent.data.edit_bones[name].head = new_pos
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.context.view_layer.objects.active = backup


class HumanoidPartsAssemble(bpy.types.Operator):
    bl_idname = "humanoid_parts.assemble"
    bl_label = "Assemble humanoid parts"
    bl_options = {"REGISTER", "UNDO"}
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return isinstance(context.active_object.data, bpy.types.Armature)

    def execute(self, context):
        armature = context.active_object.data

        for prop in PROP_NAMES:
            o = getattr(armature.humanoid_parts, prop)
            if o:
                fit_parent_bone(context.active_object, o)

        return {"FINISHED"}
