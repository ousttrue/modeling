import bpy  # type: ignore
from typing import cast
from mathutils import Vector  # type: ignore


def disassemble(
    mesh_obj: bpy.types.Object, armature_obj: bpy.types.Object, bone
) -> bool:
    bone_matrix = bone.matrix.inverted()
    bone_name = bone.name

    # separate all descendants
    bones = []

    def traverse(b):
        bones.append(b)
        for child in b.children:
            traverse(child)

    traverse(bone)

    groups = [
        mesh_obj.vertex_groups[bone.name]
        for bone in bones
        if bone.name in mesh_obj.vertex_groups
    ]
    if not groups:
        print(f"no vertex group")
        return False
    group_indices = [g.index for g in groups]

    #
    # select
    #
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")
    # obj.data.vertices[0].select = True

    new_verts = []
    mesh = cast(bpy.types.Mesh, mesh_obj.data)
    for v in mesh.vertices:
        for g in v.groups:
            if g.group in group_indices:
                new_verts.append(v)
                v.select = True

    print(f"{len(new_verts)} / {len(mesh.vertices)}")

    bpy.ops.object.mode_set(mode="EDIT")

    #
    # separate
    #
    bpy.ops.mesh.separate(type="SELECTED")
    bpy.ops.object.mode_set(mode="OBJECT")
    mod = bpy.context.selected_objects[-1]

    #
    # mod separated
    #
    mod.name = bone_name
    mod.matrix_basis = bone_matrix
    bpy.context.view_layer.objects.active = mod
    # apply bone.matrix inverse
    bpy.ops.object.mode_set(mode="EDIT")

    return True


class HumanoidPartsDisassemble(bpy.types.Operator):
    bl_idname = "humanoid_parts.disassemble"
    bl_label = "Disassemble humanoid parts"
    bl_options = {"REGISTER", "UNDO"}
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        if context.active_bone:
            for s in context.selected_objects:
                if isinstance(s.data, bpy.types.Mesh):
                    return True

    def execute(self, context):
        armature = context.active_object
        bone = context.active_bone
        mesh = None
        for o in context.selected_objects:
            if isinstance(o.data, bpy.types.Mesh):
                mesh = o
                break
        if mesh:
            if disassemble(mesh, armature, bone):
                return {"FINISHED"}

        return {"CANCELLED"}


def register():
    print(__name__)
    bpy.utils.register_class(HumanoidPartsDisassemble)

    def menu_fn(self, context):
        self.layout.operator(HumanoidPartsDisassemble.bl_idname, icon="MOD_PHYSICS")

    bpy.types.TOPBAR_MT_blender_system.append(menu_fn)


def unregister():
    print(__name__)
    bpy.utils.unregister_class(HumanoidPartsDisassemble)
