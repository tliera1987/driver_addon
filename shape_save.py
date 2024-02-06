import bpy
import json
import os

# 현재 활성화된 오브젝트를 가져옵니다.
obj = bpy.context.active_object

# 결과를 저장할 딕셔너리입니다.
shape_keys_data = {}

# 오브젝트에 쉐입키와 애니메이션 데이터가 있는지 확인합니다.
if obj and obj.data.shape_keys and obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
    key_blocks = obj.data.shape_keys.key_blocks
    action = obj.data.shape_keys.animation_data.action

    # 각 쉐입키에 대해 프레임별 값을 저장할 딕셔너리를 초기화합니다.
    for shape_key in key_blocks:
        if shape_key.name != "Basis":  # "Basis" 쉐입키는 제외합니다.
            shape_keys_data[shape_key.name] = []

    # 애니메이션 액션의 시작과 끝 프레임을 계산합니다.
    frame_start = int(action.frame_range[0])
    frame_end = int(action.frame_range[1])

    # 각 프레임에 대해 반복합니다.
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)

        # 각 쉐입키에 대해 현재 프레임의 값을 저장합니다.
        for shape_key in key_blocks:
            if shape_key.name != "Basis":
                # 여기에서 값을 반올림합니다. 소수점 세 자리까지만 저장합니다.
                value_rounded = round(shape_key.value, 3)
                shape_keys_data[shape_key.name].append(value_rounded)

# JSON으로 변환합니다.
json_data = json.dumps(shape_keys_data, indent=4)

# 현재 블렌더 파일 경로와 파일 이름을 가져옵니다.
blend_file_path = bpy.path.abspath('//')
blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend', '')
json_file_path = os.path.join(blend_file_path, f"{blend_file_name}_shape_keys.json")

# 파일로 저장합니다.
with open(json_file_path, 'w') as file:
    file.write(json_data)

print(f"Data exported to {json_file_path}")
