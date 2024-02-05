import bpy
import json

# 현재 활성화된 오브젝트를 가져옵니다.
obj = bpy.context.active_object

# 결과를 저장할 딕셔너리입니다.
shape_keys_data = {}

# 오브젝트에 쉐입키가 있는지 확인합니다.
if obj and obj.data.shape_keys:
    key_blocks = obj.data.shape_keys.key_blocks
    shape_keys_data = {kb.name: [] for kb in key_blocks if kb.name != 'Basis'}

    # 애니메이션의 시작과 끝 프레임을 구합니다.
    scn = bpy.context.scene
    frame_start = scn.frame_start
    frame_end = scn.frame_end

    # 각 프레임에 대해 쉐입키의 값을 읽습니다.
    for frame in range(frame_start, frame_end + 1):
        scn.frame_set(frame)  # 프레임을 설정합니다.
        # 각 쉐입키의 값을 저장합니다.
        for kb in key_blocks:
            if kb.name != 'Basis':
                shape_keys_data[kb.name].append({'frame': frame, 'value': kb.value})

# JSON 파일로 결과를 저장합니다.
json_path = bpy.path.abspath('//shape_keys_animation.json')
with open(json_path, 'w') as json_file:
    json.dump(shape_keys_data, json_file, indent=4)

print(f"'{json_path}'에 쉐입키 애니메이션 데이터를 저장했습니다.")
