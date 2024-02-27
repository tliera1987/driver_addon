import bpy

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
