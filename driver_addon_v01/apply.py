import bpy

def convert_controller_to_shape_key_animation(context):
    scene = context.scene
    max_frame = 0

    for obj in scene.objects:
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    if keyframe_point.co.x > max_frame:
                        max_frame = keyframe_point.co.x

    frame = scene.frame_start
    while frame <= max_frame:
        scene.frame_set(frame)
        obj = context.active_object
        if obj and obj.data.shape_keys:
            for fcurve in obj.data.shape_keys.animation_data.drivers:
                obj.data.shape_keys.keyframe_insert(fcurve.data_path)
        frame += 1
