import bpy
import json

# JSON 파일 경로 설정
file_path = '/path/to/your/shape_keys_animation.json'

# JSON 파일 로드
with open(file_path, 'r') as file:
    shape_keys_data = json.load(file)

# 'con' 오브젝트 선택
con_object = bpy.data.objects["con"]

# 모든 쉐입키 애니메이션 값 처리
for shape_key_name, animation_values in shape_keys_data.items():
    # 각 쉐입키에 대해 프레임별로 애니메이션 키 프레임 설정
    for frame_number, value in enumerate(animation_values, start=1):
        # 위치 Z 값 설정
        con_object.location.z = value
        # 키 프레임 삽입
        con_object.keyframe_insert(data_path="location", index=2, frame=frame_number)
        print(f"Set keyframe for {shape_key_name} at frame {frame_number} with value {value}")
