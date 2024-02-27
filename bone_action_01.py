import bpy
import json

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

def apply_transformations(driver_settings, shape_key_animations, armature_name):
    armature = bpy.data.objects[armature_name]
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    for setting in driver_settings:
        shape_key_name = setting["data_path"].split('"')[1]
        expression = setting["expression"]
        multiplier = float(expression.split('*')[1].strip())
        # 'var'의 부호를 확인하고, 적절한 역산을 적용합니다.
        if expression.strip().startswith('-'):
            multiplier = -multiplier

        for variable in setting["variables"]:
            bone_name = variable["data_path"].split('"')[1]
            axis_index = int(variable["data_path"].split('[')[-1][0])
            bone = armature.pose.bones[bone_name]

            if shape_key_name in shape_key_animations:
                for frame, shape_key_value in enumerate(shape_key_animations[shape_key_name], start=1):
                    # 역산 적용
                    calculated_value = shape_key_value / multiplier

                    # 본 위치 업데이트 및 키 프레임 설정
                    bone.location[axis_index] = calculated_value
                    bone.keyframe_insert(data_path='location', index=axis_index, frame=frame)


# 스크립트 실행
apply_transformations(driver_settings, shape_key_animations, "face_ctrl_animator")
