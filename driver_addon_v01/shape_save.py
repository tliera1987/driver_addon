import bpy
import json

def export_shape_key_animation(obj, filepath):
    shape_keys_data = {}
    if obj and obj.data.shape_keys and obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
        key_blocks = obj.data.shape_keys.key_blocks
        action = obj.data.shape_keys.animation_data.action
        for shape_key in key_blocks:
            if shape_key.name != "Basis":
                shape_keys_data[shape_key.name] = []
        frame_start = int(action.frame_range[0])
        frame_end = int(action.frame_range[1])
        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)
            for shape_key in key_blocks:
                if shape_key.name != "Basis":
                    value_rounded = round(shape_key.value, 6)
                    shape_keys_data[shape_key.name].append(value_rounded)
    json_data = json.dumps(shape_keys_data, indent=4)

    with open(filepath, 'w') as file:
        file.write(json_data)
    print(f"Data exported to {filepath}")
