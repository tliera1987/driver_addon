import bpy
import json

def save_shape_keys_as_json(obj, json_file_path):
    """주어진 오브젝트의 쉐입키를 JSON 파일로 저장합니다."""
    # 결과를 저장할 딕셔너리를 초기화합니다.
    shape_keys_data = {}

    # 쉐입키를 확인하고 데이터를 추출합니다.
    if obj and obj.data.shape_keys:
        for key_block in obj.data.shape_keys.key_blocks:
            if key_block.name != 'Basis':
                shape_keys_data[key_block.name] = []

        # 애니메이션의 시작과 끝 프레임을 기준으로 각 프레임의 쉐입키 값을 읽습니다.
        scn = bpy.context.scene
        for frame in range(scn.frame_start, scn.frame_end + 1):
            scn.frame_set(frame)
            for key_block in obj.data.shape_keys.key_blocks:
                if key_block.name != 'Basis':
                    shape_keys_data[key_block.name].append(round(key_block.value, 3))

    # JSON 데이터를 파일로 저장합니다.
    with open(json_file_path, 'w') as file:
        json.dump(shape_keys_data, file, indent=4)

    print(f"쉐입키 데이터가 '{json_file_path}'에 저장되었습니다.")

# 스크립트 실행
json_path = bpy.path.abspath('//shape_keys_animation.json')
save_shape_keys_as_json(bpy.context.active_object, json_path)
