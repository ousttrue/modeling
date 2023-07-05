import bpy  # type: ignore


class HumanoidPartsAssemblePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_HumanoidPparts"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HumanoidParts"
    bl_label = "Assemble"

    @classmethod
    def poll(cls, context):
        return isinstance(context.active_object.data, bpy.types.Armature)

    def draw_bone(self, armature: bpy.types.Armature, bone: str):
        self.layout.prop(armature.humanoid_parts, bone)

    def draw_bone_lr(self, armature: bpy.types.Armature, bone: str):
        split = self.layout.split(factor=0.24)
        split.label(text=f"{bone}:")
        split.column().prop(armature.humanoid_parts, f"left_{bone}", text="")
        split.column().prop(armature.humanoid_parts, f"right_{bone}", text="")

    def draw(self, context):
        armature = context.active_object.data

        self.layout.prop(context.scene, "humanoid_parts_collection")

        self.layout.label(text="Bones")

        self.draw_bone(armature, "hips")
        self.draw_bone(armature, "spine")
        self.draw_bone(armature, "chest")
        self.draw_bone(armature, "neck")
        self.draw_bone(armature, "head")
        self.draw_bone_lr(armature, "shoulder")
        self.draw_bone_lr(armature, "upper_arm")
        self.draw_bone_lr(armature, "lower_arm")
        self.draw_bone_lr(armature, "hand")
        self.draw_bone_lr(armature, "upper_leg")
        self.draw_bone_lr(armature, "lower_leg")
        self.draw_bone_lr(armature, "foot")
        self.draw_bone_lr(armature, "toes")

        self.layout.label(text="Fingers")

        self.draw_bone_lr(armature, "thumb_metacarpal")
        self.draw_bone_lr(armature, "thumb_proximal")
        self.draw_bone_lr(armature, "thumb_distal")
        self.draw_bone_lr(armature, "index_proximal")
        self.draw_bone_lr(armature, "index_intermediate")
        self.draw_bone_lr(armature, "index_distal")
        self.draw_bone_lr(armature, "middle_proximal")
        self.draw_bone_lr(armature, "middle_intermediate")
        self.draw_bone_lr(armature, "middle_distal")
        self.draw_bone_lr(armature, "ring_proximal")
        self.draw_bone_lr(armature, "ring_intermediate")
        self.draw_bone_lr(armature, "ring_distal")
        self.draw_bone_lr(armature, "little_proximal")
        self.draw_bone_lr(armature, "little_intermediate")
        self.draw_bone_lr(armature, "little_distal")