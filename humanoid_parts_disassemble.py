import bpy  # type: ignore
from mathutils import Vector  # type: ignore


class HumanoidPartsDisassemble(bpy.types.Operator):
    bl_idname = "humanoid_parts.disassemble"
    bl_label = "Disassemble humanoid parts"
    bl_options = {"REGISTER", "UNDO"}
    bl_context = "object"

    # @classmethod
    # def poll(cls, context):
    #     return context.mode == "OBJECT"

    def execute(self, context):
        self.report({"INFO"}, "disassemble")

        return {"FINISHED"}


# EnumPropertyで表示したい項目リストを作成する関数
def location_list_fn(scene, context):
    items = [("3D_CURSOR", "3Dカーソル", "3Dカーソル上に配置します"), ("ORIGIN", "原点", "原点に配置します")]
    items.extend([("OBJ_" + o.name, o.name, "オブジェクトに配置します") for o in bpy.data.objects])

    return items


class ReplicateObject(bpy.types.Operator):

    bl_idname = "object.replicate_object"
    bl_label = "選択オブジェクトの複製"
    bl_description = "選択中のオブジェクトを複製します"
    bl_options = {"REGISTER", "UNDO"}

    location: bpy.props.EnumProperty(  # type: ignore
        name="配置位置", description="複製したオブジェクトの配置位置", items=location_list_fn
    )
    scale: bpy.props.FloatVectorProperty(  # type: ignore
        name="拡大率",
        description="複製したオブジェクトの拡大率を設定します",
        default=(1.0, 1.0, 1.0),
        subtype="XYZ",
        unit="LENGTH",
    )
    rotation: bpy.props.FloatVectorProperty(  # type: ignore
        name="回転角度",
        description="複製したオブジェクトの回転角度を設定します",
        default=(0.0, 0.0, 0.0),
        subtype="AXISANGLE",
        unit="ROTATION",
    )
    offset: bpy.props.FloatVectorProperty(  # type: ignore
        name="オフセット",
        description="複製したオブジェクトの配置位置からのオフセットを設定します",
        default=(0.0, 0.0, 0.0),
        subtype="TRANSLATION",
        unit="LENGTH",
    )

    def execute(self, context):
        # bpy.ops.object.duplicate()実行後に複製オブジェクトが選択されるため、
        # 選択中のオブジェクトを保存
        # context.active_object.name：選択中のオブジェクトの名前
        src_obj_name = context.active_object.name
        # bpy.ops.object.duplicate()：オブジェクトの複製
        bpy.ops.object.duplicate()
        active_obj = context.active_object

        # 複製したオブジェクトを配置位置に移動
        # context.active_object.location：選択中のオブジェクトの位置
        if self.location == "3D_CURSOR":
            # context.scene.cursor_location：3Dカーソルの位置
            # Shallow copyを避けるため、copy()によるDeep copyを実行
            active_obj.location = context.scene.cursor_location.copy()
        elif self.location == "ORIGIN":
            active_obj.location = Vector((0.0, 0.0, 0.0))
        elif self.location[0:4] == "OBJ_":
            # bpy.data.objects：配置されているオブジェクトのリスト
            objs = bpy.data.objects
            active_obj.location = objs[self.location[4:]].location.copy()

        # 複製したオブジェクトの拡大率を設定
        # context.active_object.scale：選択中のオブジェクトの拡大率
        active_obj.scale.x = active_obj.scale.x * self.scale[0]
        active_obj.scale.y = active_obj.scale.y * self.scale[1]
        active_obj.scale.z = active_obj.scale.z * self.scale[2]

        # 複製したオブジェクトの回転角度を設定
        # context.active_object.rotation_euler：選択中のオブジェクトの回転角度
        #                                      （ラジアン）
        rot_euler = active_obj.rotation_euler
        active_obj.rotation_euler.x = rot_euler.x + self.rotation[0]
        active_obj.rotation_euler.y = rot_euler.y + self.rotation[1]
        active_obj.rotation_euler.z = rot_euler.z + self.rotation[2]

        # 複製したオブジェクトの最終位置を設定
        active_obj.location = active_obj.location + Vector(self.offset)

        self.report({"INFO"}, "サンプル2-4: 「%s」を複製しました。" % (src_obj_name))
        print("サンプル2-4: オペレーション「%s」が実行されました。" % (self.bl_idname))

        return {"FINISHED"}


def register():
    bpy.utils.register_class(HumanoidPartsDisassemble)
    bpy.utils.register_class(ReplicateObject)

    def menu_fn(self, context):
        self.layout.operator(ReplicateObject.bl_idname)

    bpy.types.VIEW3D_MT_object.append(menu_fn)
    # bpy.types.Mesh.disassemble_target = bpy.props.PointerProperty(
    #     type=bpy.types.Armature
    # )

    # bpy.types.Mesh.disassemble_target_head = bpy.props.StringProperty(
    #     type=bpy.types.Armature
    # )

    # bpy.types.Mesh.disassemble_target_tail = bpy.props.StringProperty(
    #     type=bpy.types.Armature
    # )


def unregister():
    bpy.utils.unregister_class(HumanoidPartsDisassemble)
    bpy.utils.unregister_class(ReplicateObject)
