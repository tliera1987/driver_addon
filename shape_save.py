import bpy
import json
import os

# 현재 활성화된 오브젝트를 가져옵니다
obj = bpy.context.active_object

# 결과를 저장할 딕셔너리
shape_keys_data = {}

# 오브젝트에 쉐입키와 애니메이션 데이터가 있는지 확인합니다
if obj and obj.data.shape_keys and obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
    key_blocks = obj.data.shape_keys.key_blocks
    action = obj.data.shape_keys.animation_data.action

    # "Basis"를 제외한 쉐입키 이름을 나열합니다
    shape_key_names = [shape_key.name for shape_key in key_blocks if shape_key.name != "Basis"]
    shape_keys_data['shape_key_names'] = shape_key_names

    # 애니메이션 액션의 시작과 끝 프레임을 계산합니다
    frame_start = int(action.frame_range[0])
    frame_end = int(action.frame_range[1])
    
    # 각 쉐입키의 키프레임 값들을 저장할 리스트를 생성합니다
    shape_keys_values = []

    # 각 쉐입키에 대한 키프레임 값들을 저장합니다
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        keyframe_values = []

        # "Basis"를 제외한 쉐입키 값들을 계산합니다
        for shape_key in key_blocks:
            if shape_key.name != "Basis":
                value = round(shape_key.value, 3)
                keyframe_values.append(value)

        shape_keys_values.append(keyframe_values)
        
    # 키프레임 값들을 딕셔너리에 추가합니다
    shape_keys_data['shape_keys_values'] = shape_keys_values

# JSON으로 변환하기 전에 쉐입키 목록과 키프레임 데이터 사이에 줄바꿈을 추가합니다
json_data = json.dumps(shape_keys_data).replace('],', '],\n')

# 현재 블렌더 파일 경로와 파일 이름을 가져옵니다
blend_file_path = bpy.path.abspath('//')
blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend', '')
json_file_path = os.path.join(blend_file_path, f"{blend_file_name}_shape_keys.json")

# 파일로 저장
with open(json_file_path, 'w') as file:
    file.write(json_data)

print(f"Data exported to {json_file_path}")
