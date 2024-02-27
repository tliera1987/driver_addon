bl_info = {
    "name": "My Custom Addon",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Your Name",
    "description": "A brief description of the addon.",
}

import bpy
import json

from .bone_action import apply_transformations

# JSON 파일 로드
def load_json_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# 파일 경로
driver_settings_path = "/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_01.json"
shape_key_animations_path = "/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_v02_testanimation_shape_keys.json"

# 데이터 로드
driver_settings = load_json_data(driver_settings_path)
shape_key_animations = load_json_data(shape_key_animations_path)

class boneactionOperator(bpy.types.Operator):
    bl_idname = "object.apply_transformations"
    bl_label = "bone apply_transformation"

    #실행
    def execute(self, context): 
        armature_name = "face_ctrl_animator"
        apply_transformations(driver_settings, shape_key_animations, armature_name)
        return {'FINISHED'}

class ApplyPanel(bpy.types.Panel):
    bl_label = "shape to bone"
    bl_idname = "driver"
    bl_space_type = 'VIEW_3D'  # 3D 뷰포트로 변경
    bl_region_type = 'UI'      # UI 영역으로 변경
    bl_category = 'test_test'   # 원하는 탭 이름 지정

    # UI 그리기
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, 'driver_settings_path', text="driver")
        layout.prop(scene, 'shape_key_animations_path', text="shape_anim")
        layout.operator("bone_action", text="bone_action")

# 클래스 등록
def register():
    bpy.utils.register_class(boneactionOperator)
    bpy.utils.register_class(ApplyPanel)

# 클래스 등록 해제
def unregister():
    bpy.utils.unregister_class(boneactionOperator)
    bpy.utils.unregister_class(ApplyPanel)

if __name__ == "__main__":
    register()