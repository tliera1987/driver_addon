import bpy

def apply_transformations(driver_settings, shape_key_animations, armature_name):
    armature = bpy.data.objects.get(armature_name)
    if not armature:
        print(f"Armature '{armature_name}' not found.")
        return
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    for setting in driver_settings:
        shape_key_name = setting["data_path"].split('"')[1]
        expression = setting["expression"]
        multiplier = float(expression.split('*')[1].strip())
        if expression.strip().startswith('-'):
            multiplier = -multiplier

        for variable in setting["variables"]:
            bone_name = variable["data_path"].split('"')[1]
            axis_index = int(variable["data_path"].split('[')[-1][0])
            bone = armature.pose.bones.get(bone_name)
            if not bone:
                print(f"Bone '{bone_name}' not found.")
                continue

            if shape_key_name in shape_key_animations:
                for frame, shape_key_value in enumerate(shape_key_animations[shape_key_name], start=1):
                    calculated_value = shape_key_value / multiplier
                    bone.location[axis_index] = calculated_value
                    bone.keyframe_insert(data_path='location', index=axis_index, frame=frame)
